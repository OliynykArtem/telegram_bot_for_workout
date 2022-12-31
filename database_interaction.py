from connect_to_database import connection


class Bot_functions:

    # The function performs autoincrement work for the id of any record in any table except the "user" table
    # Since autoincrement by default does not work correctly
    # Returns a new id
    def __create_new_id(self, table):
        with connection.cursor() as cursor:
            select_max_id = f"SELECT MAX(id) FROM {table}"
            cursor.execute(select_max_id)
            max_id = cursor.fetchone()[f'MAX(id)']

            if max_id is None:
                max_id = 0

            new_id = max_id + 1
            return new_id

    # If there is an entry in the "today" table with such arguments,
    # the function returns the id of the entry. If not, returns "None"
    def get_id_today(self, date, user_id):
        with connection.cursor() as cursor:
            select_id = f"SELECT id FROM today WHERE date = '{date}' AND user_id = '{user_id}'"
            cursor.execute(select_id)
            id_today = cursor.fetchone()
            if id_today is not None:
                return id_today['id']
            


    def __create_new_record_to_need(self, numbers_of_repetitions, id_today, exercise_name):
        id = self.__create_new_id('need')

        with connection.cursor() as cursor:
            insert = f"INSERT INTO need VALUES({id}, {numbers_of_repetitions}, {id_today}, '{exercise_name}')"
            cursor.execute(insert)

    def __create_new_record_to_today(self, date, user_id):
        id_today = self.__create_new_id('today')

        with connection.cursor() as cursor:
            create_id = f"INSERT INTO today VALUES({id_today}, '{date}', '{user_id}')"
            cursor.execute(create_id)

    def __create_new_record_to_one_set(self, numbers_of_repetitions, id_today, exercise_name):
        id = self.__create_new_id('one_set')

        with connection.cursor() as cursor:
            insert = f"INSERT INTO one_set VALUES({id}, {numbers_of_repetitions}, {id_today}, '{exercise_name}')"
            cursor.execute(insert)

    def __create_or_update_record_to_done(self, numbers_of_repetitions, id_today, exercise_name):
        with connection.cursor() as cursor:
            select_id = f"SELECT id FROM done WHERE exercise_name = '{exercise_name}' AND today_id = {id_today}"
            cursor.execute(select_id)
            id = cursor.fetchone()
            if id is None:
                id = self.__create_new_id('done')

                with connection.cursor() as cursor:
                    insert = f"INSERT INTO done VALUES({id}, {numbers_of_repetitions}, {id_today}, '{exercise_name}')"
                    cursor.execute(insert)
            else:
                id = id['id']

                with connection.cursor() as cursor:
                    select_numbers_of_repetitions = f"SELECT numbers_of_repetitions FROM done WHERE id = {id}"
                    cursor.execute(select_numbers_of_repetitions)

                    old_numbers_of_repetitions = cursor.fetchone()['numbers_of_repetitions']
                    new_numbers_of_repetitions = old_numbers_of_repetitions + numbers_of_repetitions

                    update = f"UPDATE done SET numbers_of_repetitions = {new_numbers_of_repetitions} WHERE id = {id}"
                    cursor.execute(update)



# Public def

    def is_available(self, table, cell_name, value):
        with connection.cursor() as cursor:
            select_value = f"SELECT EXISTS(SELECT {cell_name} FROM {table} WHERE {cell_name} = {value})"
            cursor.execute(select_value)
            result = cursor.fetchone()
            result = list(result.values())
            if result[0] == 1:
                return True
            else:
                return False

    def create_new_user(self, id, user_name):
        with connection.cursor() as cursor:
            insert = f"INSERT INTO user VALUES('{id}', '{user_name}')"
            cursor.execute(insert)


    def get_all_table_need_where_id_today(self, id_today):
        all_exercise_name = self.get_all_exercise()

        all_records_need_dict = {}
        with connection.cursor() as cursor:
            for exercise in all_exercise_name:
                select_need = f"SELECT exercise_name, numbers_of_repetitions FROM need WHERE today_id = '{id_today}' AND exercise_name = '{exercise}'"
                cursor.execute(select_need)
                record_from_need = cursor.fetchone()

                if record_from_need != 0 and record_from_need is not None:
                    all_records_need_dict[record_from_need['exercise_name']] = record_from_need['numbers_of_repetitions']
        return all_records_need_dict

    def get_all_table_done_where_id_today(self, id_today):
        all_exercise_name = self.get_all_exercise()

        all_records_done_dict = {}

        with connection.cursor() as cursor:
            for exercise in all_exercise_name:
                select_done = f"SELECT exercise_name, numbers_of_repetitions FROM done WHERE today_id = '{id_today}' AND exercise_name = '{exercise}'"
                cursor.execute(select_done)
                record_from_done = cursor.fetchone()

                if record_from_done != 0 and record_from_done is not None:
                    all_records_done_dict[record_from_done['exercise_name']] = record_from_done['numbers_of_repetitions']
        return all_records_done_dict

    def get_username_user(self, id):
        with connection.cursor() as cursor:
            select_user = f"SELECT username FROM user WHERE id = '{id}'"
            cursor.execute(select_user)
            username = cursor.fetchone()
            if username is not None:
                return username['username']

    def get_user_id(self, username):
        with connection.cursor() as cursor:
            select_user_id = f"SELECT id FROM user WHERE username = '{username}'"
            cursor.execute(select_user_id)
            user_id = cursor.fetchone()
            if user_id is not None:
                return user_id['id']


    def get_all_users(self):
        with connection.cursor() as cursor:
            select_all_username_from_user = "SELECT username FROM user"
            cursor.execute(select_all_username_from_user)
            all_username_dict = cursor.fetchall()
            if all_username_dict is not None:
                all_username_list = []
                for username in all_username_dict:
                    all_username_list.append(username['username'])
            return all_username_list

    def get_all_exercise(self):
        with connection.cursor() as cursor:
            select_all_exercise = "SELECT name FROM exercise"
            cursor.execute(select_all_exercise)
            all_exercise_dict = cursor.fetchall()
            if all_exercise_dict is not None:
                all_exercise_list = []
                for exercise in all_exercise_dict:
                    all_exercise_list.append(exercise['name'])
            return all_exercise_list

    def get_all_record_type(self):
        with connection.cursor() as cursor:
            select_all_record_type = f"SELECT name FROM record_type"
            cursor.execute(select_all_record_type)
            all_record_type_dict = cursor.fetchall()
            if all_record_type_dict is not None:
                all_record_type_list = []
                for record_type in all_record_type_dict:
                    all_record_type_list.append(record_type['name'])
            return all_record_type_list


    def get_all_records_from_user_where_exercise(self, exercise_name, user_id):
        all_record_type = self.get_all_record_type()

        i = 0
        with connection.cursor() as cursor:
            all_records = []

            for record_type in all_record_type:
                get_records = f"SELECT date, record_type_name, numbers_of_repetitions FROM record WHERE exercise_name = '{exercise_name}' AND record_type_name = '{record_type}' AND user_id = '{user_id}' AND numbers_of_repetitions = (SELECT MAX(numbers_of_repetitions) FROM record WHERE record_type_name = '{record_type}' AND exercise_name = '{exercise_name}' AND user_id = '{user_id}')"
                cursor.execute(get_records)
                record = cursor.fetchall()

                if len(record) != 0:

                    records = []

                    date = record[0].get('date')
                    records.append(str(date))

                    records.append(record[0].get('record_type_name'))

                    numbers_of_repetitions = record[0].get('numbers_of_repetitions')
                    records.append(str(numbers_of_repetitions))

                    all_records.append(records)

                    i = i + 1
            return all_records


    def add_record(self, date, exercise_name, number_of_repetitions, record_type_name, user_id):
        id = self.__create_new_id('record')

        print(id, date, exercise_name, number_of_repetitions, record_type_name, user_id)
        with connection.cursor() as cursor:
            insert = f"INSERT INTO record VALUES({id}, '{date}', {number_of_repetitions}, '{user_id}', '{record_type_name}', '{exercise_name}')"
            cursor.execute(insert)

    def add_exercise_to_be_completed(self, user_id, date, exercise_name, numbers_of_repetitions):
        id_today = self.get_id_today(date, user_id)

        if id_today is None:
            self.__create_new_record_to_today(date, user_id)
            id_today = self.get_id_today(date, user_id)

        self.__create_new_record_to_need(numbers_of_repetitions, id_today, exercise_name)

    def add_completed_exercise_in_one_set(self, user_id, date, exercise_name, number_of_repetitions):
        id_today = self.get_id_today(date, user_id)

        if id_today is None:
            self.__create_new_record_to_today(date, user_id)
            id_today = self.get_id_today(date, user_id)

        self.__create_new_record_to_one_set(number_of_repetitions, id_today, exercise_name)
        self.__create_or_update_record_to_done(number_of_repetitions, id_today, exercise_name)


# Public def admin

    def add_exercise(self, name):
        with connection.cursor() as cursor:
            insert = f"INSERT INTO exercise VALUES('{name}')"
            cursor.execute(insert)

    def add_record_type(self, name):
        with connection.cursor() as cursor:
            insert = f"INSERT INTO record_type VALUES('{name}')"
            cursor.execute(insert)

    def remove_exercise(self, name):
        with connection.cursor() as cursor:
            insert = f"DELETE FROM exercise WHERE name = '{name}'"
            cursor.execute(insert)

    def remove_record_type(self, name):
        with connection.cursor() as cursor:
            insert = f"DELETE FROM record_type WHERE name = '{name}'"
            cursor.execute(insert)

