from flask import flash 
from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from pprint import pprint
import re
PHONE_REGEX = re.compile(r'^\d{3}-\d{3}-\d{4}$')


class Facility:

    def __init__(self, data):
        self.id = data['id']
        self.facility_name = data['facility_name']
        self.contact = data['contact']
        self.phone_number = data['phone_number']
        self.location = data['location']
        self.distance_from_I70 = data['distance_from_I70']
        self.amenities = data['amenities']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None


    @staticmethod
    def form_is_valid(form_data):
# this method validates the facility form
        is_valid = True
# text validator
        # is it even there?
        if len(form_data['facility_name'].strip()) == 0:
            flash("Please enter the name of the facility.")
            is_valid = False
        # if it is there this will check to make sure it's not <3
        elif len(form_data['facility_name'].strip()) <3:
            flash("Facility name must be at least three characters.")
            is_valid = False
# text validator
        if len(form_data['contact'].strip()) == 0:
            flash("Please enter a contact person for the facility.")
            is_valid = False
        elif len(form_data['contact'].strip()) <3: 
            flash("Contact must be at least three characters.")
            is_valid = False

# phone number validator
        if len(form_data['phone_number'].strip()) == 0:
            flash("Please enter phone number.")
            is_valid = False
        elif not PHONE_REGEX.match(form_data['phone_number']):
                flash("Invalid phone number.")
                is_valid = False
                
# text validator
        if len(form_data['location'].strip()) == 0:
            flash("Please enter the city and state where the facility is located.")
            is_valid = False
        elif len(form_data['location'].strip()) <3:
            flash("Location must be at least 3 characters.")
            is_valid = False

# radio button validator
        if "distance_from_I70" not in form_data:
            pprint("radio button not checked")
            is_valid = False
            flash("Please select yes or no.")
        elif form_data["distance_from_I70"] not in ["0", "1"]:
            is_valid = False
            flash("Invalid option.")

# text validator
        if len(form_data['amenities'].strip()) == 0:
            flash("Please enter the amenities the facility offers (hay, bedding, buckets, turnout, etc.).")
            is_valid = False
        elif len(form_data['amenities'].strip()) <3:
            flash("Amenities must be at least three characters.")
            is_valid = False

        # if the form is filled out correctly then it will be returned as valid 
        return is_valid

# # date validator
#         if len(form_data["location"]) == 0:

#             flash("Please enter location.")
#             is_valid = False
#         else:
#             try:
#                 datetime.strptime(form_data["location"], "%Y-%m-%d")
#             except:
#                 flash("Invalid date_column.")
#                 is_valid = False
        



    @classmethod
    def find_all(cls):
# this method finds all facilities
        query = "SELECT * FROM facilities;"
        list_of_dicts = connectToMySQL("solo_project").query_db(query)
        pprint(list_of_dicts)
        facilities = []

        for each_dict in list_of_dicts:
            facility = facility(each_dict)
            facilities.append(facility)
            
        return facilities 


    @classmethod
    def find_all_with_users(cls):
# this method finds all the facilities with users in the database
        query = """
        SELECT * FROM facilities
        JOIN users
        ON facilities.user_id = users.id; 
        """
        list_of_dicts = connectToMySQL("solo_project").query_db(query)
        pprint(list_of_dicts)
        facilities = []

        for each_dict in list_of_dicts:
            facility = Facility(each_dict) 
            user_data = {
                "id": each_dict["users.id"],
                "first_name": each_dict["first_name"],
                "last_name":each_dict["last_name"],
                "email": each_dict["email"],
                "password": each_dict["password"],
                "created_at": each_dict["users.created_at"],
                "updated_at": each_dict["users.updated_at"],
            } 
            user = User(user_data)
            facility.user = user
            facilities.append(facility)

        return facilities  


    @classmethod
    def create(cls, form_data):
# this method creates a record of the new facility from a form
        query = """
        INSERT INTO facilities
        (facility_name, contact, phone_number, location, distance_from_I70, amenities, user_id)
        VALUES
        (%(facility_name)s, %(contact)s, %(phone_number)s, %(location)s, %(distance_from_I70)s, %(amenities)s, %(user_id)s);
        """
        facility_id = connectToMySQL("solo_project").query_db(query, form_data)
        return facility_id


    @classmethod
    def find_by_id_with_user(cls, facility_id):
#finds one facility by id and the user that uploaded it in the database
        query = """
        SELECT * FROM facilities
        JOIN users
        ON facilities.user_id = users.id
        WHERE facilities.id = %(facility_id)s; 
        """
        data = {"facility_id": facility_id}
        list_of_dicts = connectToMySQL("solo_project").query_db(query, data)
        pprint(list_of_dicts)

        if len(list_of_dicts) == 0:
            return None

        facility = Facility(list_of_dicts[0])
        user_data = {
            "id": list_of_dicts[0]["users.id"],
            "first_name": list_of_dicts[0]["first_name"],
            "last_name": list_of_dicts[0]["last_name"],
            "email": list_of_dicts[0]["email"],
            "password": list_of_dicts[0]["password"],
            "created_at": list_of_dicts[0]["users.created_at"],
            "updated_at": list_of_dicts[0]["users.updated_at"],
        }
        facility.user = User(user_data)
        return facility


    @classmethod
    def update(cls, form_data):
# this method updates the facility in the database from the form 
        query = """
        UPDATE facilities
        SET
        facility_name = %(facility_name)s, 
        contact = %(contact)s, 
        phone_number = %(phone_number)s,
        location = %(location)s,
        distance_from_I70 = %(distance_from_I70)s,
        amenities = %(amenities)s
        WHERE id = %(facility_id)s;
        """
        connectToMySQL("solo_project").query_db(query, form_data)
        # calling this method implicitely returns none, this shows it explicitly
        return     


    @classmethod
    def delete(cls, facility_id):
# this method deletes a facility in the database by it's id
        query = "DELETE FROM facilities WHERE id = %(facility_id)s;"
        data = {"facility_id": facility_id}
        connectToMySQL("solo_project").query_db(query, data)
        return


    @classmethod
    def find_by_id(cls, facility_id):
# this method finds one facility by it's id in the database
        query = "SELECT * FROM facilities WHERE id = %(facility_id)s;"
        data = {"facility_id": facility_id}
        list_of_dicts = connectToMySQL("solo_project").query_db(query, data)
        pprint(list_of_dicts)

        if len(list_of_dicts) == 0:
            return None
        
        facility = facility(list_of_dicts[0])
        for each_dict in list_of_dicts:
            if each_dict["user.id"] != None:
                user_data = {
                    "id": each_dict["facility.id"],
                    "name": each_dict["first_name"],
                    "last_name": each_dict["last_name"],
                    "email": each_dict["email"],
                    "password": each_dict["password"],
                    "created_at": each_dict["facility.created_at"],
                    "updated_at": each_dict["facility.updated_at"],
                    }
                user = user.User(user_data)
        return facility


#     @classmethod
#     def count_by_title(cls, title):
# # this method counts the number of facilities by title
#         query = """
#         SELECT COUNT(name) as "count"
#         FROM facilities
#         WHERE name = %(name)s;
#         """
#         data = {"name": name}
#         list_of_dicts = connectToMySQL("solo_project").query_db(query, data)
#         pprint(list_of_dicts)
#         return list_of_dicts[0]["count"]


#     @classmethod
#     def find_by_user_id(cls, user_id):
# # this method finds a user by user_id
#         query = """SELECT * FROM users WHERE id = %(user_id)s;"""
#         data = {"user_id": user_id}
#         list_of_dicts = connectToMySQL("solo_project").query_db(query, data)
#         if len(list_of_dicts) == 0:
#             return None
        
#         facility = facility(list_of_dicts[0])
#         user_data = {
#             "id" = list_of_dicts["id"],
#             "first_name" = list_of_dicts["first_name"],
#             "last_name" = list_of_dicts["last_name"],
#             "email" = list_of_dicts["email"],
#             "password" = list_of_dicts["password"],
#             "created_at" = list_of_dicts["created_at"],
#             "updated_at" = list_of_dicts["updated_at"],    
#         }
#         facility.user = User(user_data)
#         return facility

