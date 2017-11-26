import MySQLdb
import json
from urllib2 import urlopen
from datetime import datetime
from daemon import runner

api_url = "https://track-well.bubbleapps.io/api/1.1/obj/"
api_token = '3335e18ca33eb3d9fc436a272bb9c6fb'


def query(sql):
    """
        Return the query result of sql
        For SELECT statement return a list
        For all others return lastrowid

    """
    global conn
    conn = MySQLdb.connect(user='ua822168_track_well',
                    passwd='track_well_@dmin',
                    host='66.70.233.161',
                    db='ua822168_track_well')

    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

        if sql.strip().startswith("SELECT"):
            result = cursor.fetchall()
        else:
            result = cursor.lastrowid
        cursor.close()
    finally:
        conn.close()

    return result


def send_api_request(tableName=None, cursor= None):
    # final_url = (api_url + tableName + "?" + "constraints=" + json_array + "&sort_field=Created%20Date&descending=false&cursor=" + str(
    #         cursorIndex) + "&api_token=" + api_token)

    final_url = (api_url + tableName + "?descending=false&cursor=" + str(cursor)+"&api_token=" + api_token)
    try:
        data = urlopen(str(final_url)).read()
        return json.loads(data)
    except:
        pass


def insert_user_data(tbl, cursor):
    results = send_api_request(str(tbl), cursor)
    for data in results['response']['results']:
        cursor +=1
        id = data['_id']

        get_sql = "SELECT id FROM user WHERE id='%s'" % str(id) # Check if a user already exist
        if not query(get_sql):
            admin_yn = str(data['admin_yn']) if 'admin_yn' in data else 'False'
            alcohol_yn = str(data['alcohol_yn']) if 'alcohol_yn' in data else 'False'
            anon_code = str(data['anon_code']) if 'anon_code' in data else ''
            bio_sex = str(data['bio_sex']) if 'bio_sex' in data else ''
            caffeine_yn = str(data['caffeine_yn']) if 'caffeine_yn' in data else 'False'
            display_name = data['display_name'] if 'display_name' in data else ''
            height_cm = str(data['height_cm']) if 'height_cm' in data else '0'
            married_yn = str(data['married_yn']) if 'married_yn' in data else 'False'
            menstruation_yn = str(data['menstruation_yn']) if 'menstruation_yn' in data else 'False'
            picture = data['picture'] if 'picture' in data else ''
            poll_hide_yn = str(data['poll_hide_yn']) if 'poll_hide_yn' in data else 'False'
            pregnant_yn = str(data['pregnant_yn']) if 'pregnant_yn' in data else 'False'
            real_name = str(data['real_name'].encode('ascii','ignore').strip()) if 'real_name' in data else ''
            smoke_yn = str(data['smoke_yn']) if 'smoke_yn' in data else 'False'
            usual_activity = str(data['usual_activity']) if 'usual_activity' in data else ''
            usual_conditions = str(data['usual_conditions']) if 'usual_conditions' in data else ''
            usual_diet = str(data['usual_diet']) if 'usual_diet' in data else ''
            usual_medications = str(data['usual_medications']) if 'usual_medications' in data else ''
            address = data['location']['address'] if 'location' in data else ''
            lat = str(data['location']['lat']) if 'location' in data else ''
            lng = str(data['location']['lng']) if 'location' in data else ''


            sql = """
                INSERT INTO user
                (
                    id,
                    admin_yn,
                    alcohol_yn,
                    anon_code,
                    bio_sex,
                    caffeine_yn,
                    display_name,
                    height_cm,
                    married_yn,
                    menstruation_yn,
                    picture,
                    poll_hide_yn,
                    pregnant_yn,
                    real_name,
                    smoke_yn,
                    usual_activity,
                    usual_conditions,
                    usual_diet,
                    usual_medications,
                    address,
                    lat,
                    lng
                )
                VALUES(
                    '""" + id + """',
                    """ + admin_yn + """,
                    """ + alcohol_yn + """,
                    '""" + anon_code + """',
                    '""" + bio_sex + """',
                    """ + caffeine_yn + """,
                    '""" + display_name.replace("'", "\\'") + """',
                    """ + height_cm + """,
                    """ + married_yn + """,
                    """ + menstruation_yn + """,
                    '""" + picture +"""',
                    """ + poll_hide_yn + """,
                    """ + pregnant_yn  + """,
                    '""" + real_name.replace("'", "\\'") + """',
                    """ + smoke_yn + """,
                    '""" + usual_activity.replace("'", "\\'") + """',
                    '""" + usual_conditions.replace("'", "\\'") + """',
                    '""" + usual_diet.replace("'", "\\'") + """',
                    '""" + usual_medications.replace("'", "\\'") + """',
                    '""" + address.replace("'", "\\'") + """',
                    '""" + lat + """',
                    '""" + lng + """'
                )
            """

            query(sql)
    if cursor < results['response']['remaining'] :
        insert_user_data(tbl, cursor)


def insert_entry_data(tbl, cursor):
    results = send_api_request(str(tbl), cursor)
    for data in results['response']['results']:
        cursor += 1
        id = data['_id']
        get_sql = "SELECT id FROM entry WHERE id='%s'" % id  # Check if a preset already exist
        if not query(get_sql):
            age_yrs = str(data['age_yrs']) if 'age_yrs' in data else 'False'
            alcohol_yn = str(data['alcohol_yn']) if 'alcohol_yn' in data else 'False'
            bio_sex = str(data['bio_sex']) if 'bio_sex' in data else ''
            caffeine_yn = str(data['caffeine_yn']) if 'caffeine_yn' in data else 'False'
            chosen_datetime = str(data['chosen_datetime'].split("T")[0]) if 'chosen_datetime' in data else ''
            height_cm = str(data['height_cm']) if 'height_cm' in data else ''
            image = str(data['image']) if 'image' in data else ''
            image_name = str(data['image_name']) if 'image_name' in data else ''
            address = str(data['address']) if 'address' in data else ''
            lat = str(data['lat']) if 'lat' in data else ''
            lng = str(data['lng']) if 'lng' in data else ''
            married_yn = str(data['married_yn']) if 'married_yn' in data else 'False'
            menstruation_yn = str(data['menstruation_yn']) if 'menstruation_yn' in data else 'False'
            pregnant_yn = str(data['pregnant_yn']) if 'pregnant_yn' in data else 'False'
            preset_array_amount = str(data['preset_array_amount']) if 'preset_array_amount' in data else '0'
            preset_array_duplicated_yn = str(data['preset_array_duplicated_yn']) if 'preset_array_duplicated_yn' in data else 'False'
            preset_array_text = str(data['preset_array_text']) if 'preset_array_text' in data else ''
            smoke_yn = str(data['smoke_yn']) if 'smoke_yn' in data else 'False'
            text = str(data['text']) if 'text' in data else ''
            tmplt_day_max = str(data['tmplt_day_max'].split("T")[0]) if 'tmplt_day_max' in data else str(datetime.now().date())
            tmplt_day_min = str(data['tmplt_day_min'].split("T")[0]) if 'tmplt_day_min' in data else str(datetime.now().date())
            usual_activity = str(data['usual_activity']) if 'usual_activity' in data else ''
            usual_conditions = str(data['usual_conditions']) if 'usual_conditions' in data else ''
            usual_diet = str(data['usual_diet']) if 'usual_diet' in data else ''
            usual_medication = str(data['usual_medication']) if 'usual_medication' in data else ''
            chosen_user_id = str(data['chosen_user']) if 'chosen_user' in data else ''
            preset_array_id = str(data['preset_array']) if 'preset_array' in data else ''
            preset_array_protocol_id = str(data['preset_array_protocol']) if 'preset_array_protocol' in data else ''
            preset_just_id = str(data['preset_just']) if 'preset_just' in data else ''
            protocol_list_id = str(data['protocol_list'][0]) if 'protocol_list' in data else ''
            tmplt_preset_id = str(data['tmplt_preset']) if 'tmplt_preset' in data else ''

    #         sql = """
    #             INSERT INTO track_well.entry
    #             (
    #                 id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
    #                 preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
    #                 preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
    #             )
    #             VALUES
    #             (
    #                 '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
    #                 '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
    #                 """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
    #                 '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'",
    #                                                                                                         "\\'") + """', '""" + usual_conditions.replace(
    # "'", "\\'") + """',
    #                 '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', IF(chosen_user_id == '': NULL, '""" + chosen_user_id + """'), IF(preset_array_id == '', NULL, '""" + preset_array_id + """'),
    #                 IF(preset_array_protocol_id == '': NULL, '""" + preset_array_protocol_id + """'), IF(protocol_list_id == '', '""" + preset_just_id + """',NULL), IF(protocol_list_id == '', NULL,'"""+protocol_list_id+"""') , '""" + tmplt_preset_id + """'
    #             )"""

            if chosen_user_id and preset_array_protocol_id and preset_array_id and preset_just_id and protocol_list_id and tmplt_preset_id:
                sql = """
                    INSERT INTO entry
                    (
                        id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
                        preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
                        preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
                    )
                    VALUES
                    (
                        '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
                        '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat +"""', '""" + lng + """', """ + married_yn  + """, """ + menstruation_yn + """,
                        """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
                        '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
                        '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'", "\\'") + """', '""" + chosen_user_id + """', '""" + preset_array_id + """',
                        '""" + preset_array_protocol_id + """', '""" + preset_just_id + """', '""" + protocol_list_id + """', '""" + tmplt_preset_id + """'
                    )"""
            elif not chosen_user_id and preset_array_id and not preset_array_protocol_id and preset_just_id and not protocol_list_id and not tmplt_preset_id:
                sql = """
                    INSERT INTO entry
                    (
                        id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
                        preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
                        preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
                    )
                    VALUES
                    (
                        '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
                        '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
                        """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
                        '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
                        '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'", "\\'") + """', NULL, '""" + preset_array_id + """',
                        NULL, '""" + preset_just_id + """', NULL, NULL
                    )"""
            elif chosen_user_id and preset_array_id and not preset_array_protocol_id and preset_just_id and protocol_list_id and tmplt_preset_id:
                sql = """
                    INSERT INTO entry
                    (
                        id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
                        preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
                        preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
                    )
                    VALUES
                    (
                        '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
                        '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
                        """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
                        '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
                        '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'", "\\'") + """', '""" + chosen_user_id + """', '""" + preset_array_id + """',
                        NULL, '""" + preset_just_id + """', '""" + protocol_list_id + """', '""" + tmplt_preset_id + """'
                    )"""
            elif chosen_user_id and preset_array_id and preset_array_protocol_id and preset_just_id and not protocol_list_id and not tmplt_preset_id:
                sql = """
                    INSERT INTO entry
                    (
                        id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
                        preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
                        preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
                    )
                    VALUES
                    (
                        '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
                        '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
                        """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
                        '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
                        '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'", "\\'") + """', '""" + chosen_user_id + """', '""" + preset_array_id + """',
                        '""" + preset_array_protocol_id + """', '""" + preset_just_id + """', NULL, NULL
                    )"""
            # elif chosen_user_id  and not preset_array_id and preset_array_protocol_id and preset_just_id and protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'", "\\'") + """', '""" + chosen_user_id + """', NULL,
            #             '""" + preset_array_protocol_id + """', '""" + preset_just_id + """', '""" + protocol_list_id + """', '""" + tmplt_preset_id + """'
            #         )"""
            #
            # elif chosen_user_id and preset_array_id and not preset_array_protocol_id and preset_just_id and protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', '""" + chosen_user_id + """', '""" + preset_array_id + """',
            #             NULL, '""" + preset_just_id + """', '""" + protocol_list_id + """', '""" + tmplt_preset_id + """'
            #         )"""
            # elif chosen_user_id and preset_array_id and preset_array_protocol_id and not preset_just_id and protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', '""" + chosen_user_id + """', '""" + preset_array_id + """',
            #             '""" + preset_array_protocol_id + """', NULL, '""" + protocol_list_id + """', '""" + tmplt_preset_id + """'
            #         )"""
            # elif chosen_user_id and preset_array_id and preset_array_protocol_id and preset_just_id and not protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', '""" + chosen_user_id + """', '""" + preset_array_id + """',
            #             '""" + preset_array_protocol_id + """', '""" + preset_just_id + """', NULL, '""" + tmplt_preset_id + """'
            #         )"""
            # elif chosen_user_id and preset_array_id and preset_array_protocol_id and preset_just_id and protocol_list_id and not tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', '""" + chosen_user_id + """', '""" + preset_array_id + """',
            #             '""" + preset_array_protocol_id + """', '""" + preset_just_id + """', '""" + protocol_list_id + """', NULL
            #         )"""
            # elif not chosen_user_id and not preset_array_id and preset_array_protocol_id and preset_just_id and protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', NULL, NULL,
            #             '""" + preset_array_protocol_id + """', '""" + preset_just_id + """', '""" + protocol_list_id + """', '""" + tmplt_preset_id + """'
            #         )"""
            # elif not chosen_user_id and preset_array_id and not preset_array_protocol_id and preset_just_id and protocol_list_id and not tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', NULL, '""" + preset_array_id + """',
            #             NULL, '""" + preset_just_id + """', '""" + protocol_list_id + """', '""" + tmplt_preset_id + """'
            #         )"""
            # elif not chosen_user_id and preset_array_id and preset_array_protocol_id and not preset_just_id and protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', NULL, '""" + preset_array_id + """',
            #             '""" + preset_array_protocol_id + """', NULL, '""" + protocol_list_id + """', '""" + tmplt_preset_id + """'
            #         )"""
            # elif not chosen_user_id and preset_array_id and preset_array_protocol_id and preset_just_id and not protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', NULL, '""" + preset_array_id + """',
            #             '""" + preset_array_protocol_id + """', '""" + preset_just_id + """', NULL, '""" + tmplt_preset_id + """'
            #         )"""
            # elif not chosen_user_id and preset_array_id and preset_array_protocol_id and preset_just_id and protocol_list_id and not tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', NULL, '""" + preset_array_id + """',
            #             '""" + preset_array_protocol_id + """', '""" + preset_just_id + """', '""" + protocol_list_id + """', NULL
            #         )"""
            # elif chosen_user_id and not preset_array_id and not preset_array_protocol_id and preset_just_id and protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', '""" + chosen_user_id + """', NULL,
            #             NULL, '""" + preset_just_id + """', '""" + protocol_list_id + """', '""" + tmplt_preset_id + """'
            #         )"""
            # elif chosen_user_id and not preset_array_id and preset_array_protocol_id and not preset_just_id and protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', '""" + chosen_user_id + """', NULL,
            #             '""" + preset_array_protocol_id + """', NULL, '""" + protocol_list_id + """', '""" + tmplt_preset_id + """'
            #         )"""
            # elif chosen_user_id and not preset_array_id and preset_array_protocol_id and preset_just_id and not protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', '""" + chosen_user_id + """', NULL,
            #             '""" + preset_array_protocol_id + """', '""" + preset_just_id + """', NULL, '""" + tmplt_preset_id + """'
            #         )"""
            # elif chosen_user_id and not preset_array_id and preset_array_protocol_id and preset_just_id and protocol_list_id and not tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', '""" + chosen_user_id + """', NULL,
            #             '""" + preset_array_protocol_id + """', '""" + preset_just_id + """', '""" + protocol_list_id + """', NULL
            #         )"""
            # elif chosen_user_id and preset_array_id and not preset_array_protocol_id and not preset_just_id and protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', '""" + chosen_user_id + """', '""" + preset_array_id + """',
            #             NULL, NULL, '""" + protocol_list_id + """', '""" + tmplt_preset_id + """'
            #         )"""
            # elif chosen_user_id and preset_array_id and not preset_array_protocol_id and preset_just_id and not protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', '""" + chosen_user_id + """', '""" + preset_array_id + """',
            #             NULL, '""" + preset_just_id + """', NULL, '""" + tmplt_preset_id + """'
            #         )"""
            # elif chosen_user_id and preset_array_id and not preset_array_protocol_id and preset_just_id and protocol_list_id and not tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', '""" + chosen_user_id + """', '""" + preset_array_id + """',
            #             NULL, '""" + preset_just_id + """', '""" + protocol_list_id + """', NULL
            #         )"""
            # elif chosen_user_id and preset_array_id and preset_array_protocol_id and not preset_just_id and not protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', '""" + chosen_user_id + """', '""" + preset_array_id + """',
            #             '""" + preset_array_protocol_id + """', NULL, NULL, '""" + tmplt_preset_id + """'
            #         )"""
            # elif chosen_user_id and preset_array_id and preset_array_protocol_id and not preset_just_id and protocol_list_id and not tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', '""" + chosen_user_id + """', '""" + preset_array_id + """',
            #             '""" + preset_array_protocol_id + """', NULL, '""" + protocol_list_id + """', NULL
            #         )"""
            # elif not chosen_user_id and not preset_array_id and not preset_array_protocol_id and preset_just_id and protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', NULL, NULL,
            #             NULL, '""" + preset_just_id + """', '""" + protocol_list_id + """', '""" + tmplt_preset_id + """'
            #         )"""
            # elif not chosen_user_id and not preset_array_id and preset_array_protocol_id and not preset_just_id and protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', NULL, NULL,
            #             '""" + preset_array_protocol_id + """', NULL, '""" + protocol_list_id + """', '""" + tmplt_preset_id + """'
            #         )"""
            # elif not chosen_user_id and not preset_array_id and preset_array_protocol_id and preset_just_id and not protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', NULL, NULL,
            #             '""" + preset_array_protocol_id + """', '""" + preset_just_id + """', NULL, '""" + tmplt_preset_id + """'
            #         )"""
            # elif not chosen_user_id and not preset_array_id and preset_array_protocol_id and preset_just_id and protocol_list_id and not tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', NULL, NULL,
            #             '""" + preset_array_protocol_id + """', '""" + preset_just_id + """', '""" + protocol_list_id + """', NULL
            #         )"""
            # elif chosen_user_id and not preset_array_id and not preset_array_protocol_id and not preset_just_id and protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', '""" + chosen_user_id + """', NULL,
            #             NULL, NULL, '""" + protocol_list_id + """', '""" + tmplt_preset_id + """'
            #         )"""
            # elif chosen_user_id and not preset_array_id and not preset_array_protocol_id and preset_just_id and not protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', '""" + chosen_user_id + """', NULL,
            #             NULL, '""" + preset_just_id + """', NULL, '""" + tmplt_preset_id + """'
            #         )"""
            # elif chosen_user_id and not preset_array_id and not preset_array_protocol_id and preset_just_id and protocol_list_id and not tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', '""" + chosen_user_id + """', NULL,
            #             NULL, '""" + preset_just_id + """', '""" + protocol_list_id + """', NULL
            #         )"""
            # elif chosen_user_id and preset_array_id and not preset_array_protocol_id and not preset_just_id and not protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', '""" + chosen_user_id + """', NULL,
            #             NULL, '""" + preset_just_id + """', NULL, '""" + tmplt_preset_id + """'
            #         )"""
            # elif chosen_user_id and preset_array_id and not preset_array_protocol_id and not preset_just_id and protocol_list_id and not tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', '""" + chosen_user_id + """', NULL,
            #             NULL, '""" + preset_just_id + """', '""" + protocol_list_id + """', NULL
            #         )"""
            # elif not chosen_user_id and not preset_array_id and not preset_array_protocol_id and not preset_just_id and protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', NULL, NULL,
            #             NULL, NULL, '""" + protocol_list_id + """', '""" + tmplt_preset_id + """'
            #         )"""
            # elif not chosen_user_id and not preset_array_id and not preset_array_protocol_id and preset_just_id and not protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', NULL, NULL,
            #             NULL, '""" + preset_just_id + """', NULL, '""" + tmplt_preset_id + """'
            #         )"""
            # elif not chosen_user_id and not preset_array_id and not preset_array_protocol_id and preset_just_id and protocol_list_id and not tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', NULL, NULL,
            #             NULL, '""" + preset_just_id + """', '""" + protocol_list_id + """', NULL
            #         )"""
            # elif chosen_user_id and not preset_array_id and not preset_array_protocol_id and not preset_just_id and not protocol_list_id and tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', '""" + chosen_user_id + """', NULL,
            #             NULL, NULL, NULL, '""" + tmplt_preset_id + """'
            #         )"""
            # elif chosen_user_id and not preset_array_id and not preset_array_protocol_id and not preset_just_id and protocol_list_id and not tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', '""" + chosen_user_id + """', NULL,
            #             NULL, NULL, '""" + protocol_list_id + """', NULL
            #         )"""
            # elif chosen_user_id and preset_array_id and not preset_array_protocol_id and not preset_just_id and not protocol_list_id and not tmplt_preset_id:
            #     sql = """
            #         INSERT INTO track_well.entry
            #         (
            #             id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
            #             preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
            #             preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
            #         )
            #         VALUES
            #         (
            #             '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
            #             '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
            #             """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
            #             '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
            #             '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', '""" + chosen_user_id + """', '""" + preset_array_id + """',
            #             NULL, NULL, NULL, NULL
            #         )"""
            else:
                sql = """
                    INSERT INTO entry
                    (
                        id, age_yrs, alcohol_yn, bio_sex, caffeine_yn, chosen_datetime, height_cm, image, image_name, address, lat, lng, married_yn, menstruation_yn, pregnant_yn, preset_array_amount,
                        preset_array_duplicated_yn, preset_array_text, smoke_yn, text, tmplt_day_max, tmplt_day_min, usual_activity, usual_conditions, usual_diet, usual_medication, chosen_user_id,
                        preset_array_id, preset_array_protocol_id, preset_just_id, protocol_list_id, tmplt_preset_id
                    )
                    VALUES
                    (
                        '""" + id + """', """ + age_yrs + """, """ + alcohol_yn + """, '""" + bio_sex + """', """ + caffeine_yn + """, '""" + chosen_datetime + """', '""" + height_cm + """',
                        '""" + image + """', '""" + image_name + """', '""" + address + """', '""" + lat + """', '""" + lng + """', """ + married_yn + """, """ + menstruation_yn + """,
                        """ + pregnant_yn + """, '""" + preset_array_amount + """', """ + preset_array_duplicated_yn + """, '""" + preset_array_text + """', """ + smoke_yn + """, '""" + text + """',
                        '""" + tmplt_day_max + """', '""" + tmplt_day_min + """', '""" + usual_activity.replace("'", "\\'") + """', '""" + usual_conditions.replace("'", "\\'") + """',
                        '""" + usual_diet.replace("'", "\\'") + """', '""" + usual_medication.replace("'","\\'") + """', NULL, NULL, NULL, NULL, NULL, NULL
                    )"""


            query(sql)
    if cursor < results['response']['remaining'] :
        insert_entry_data(tbl, cursor)


def insert_preset_data(tbl, cursor):
    results = send_api_request(str(tbl), cursor)
    for data in results['response']['results']:
        cursor += 1
        id = data['_id']
        get_sql = "SELECT id FROM preset WHERE id='%s'" % id  # Check if a preset already exist
        if not query(get_sql):
            description = str(data['description'].encode('ascii','ignore').strip()) if data['description'] else str(data['description']) if 'description' in data and  data['description'] != None else ''
            display_name = str(data['display_name'].encode('ascii','ignore').strip()) if data['display_name'] else str(data['display_name']) if 'display_name' in data else ''
            exclude_sex = str(data['exclude_sex']) if 'exclude_sex' in data else ''
            figure = str(data['figure']) if 'figure' in data else ''
            help_link_text = str(data['help_link_text']) if 'help_link_text' in data else ''
            help_link_url = str(data['help_link_url']) if 'help_link_url' in data else ''
            protocol_dependent_yn = str(data['protocol_dependent_yn']) if 'protocol_dependent_yn' in data else 'False'
            question = str(data['question']) if 'question' in data else ''
            short_display_name = str(data['short_display_name'].encode('ascii','ignore').strip()) if data['short_display_name'] else str(data['short_display_name']) if 'short_display_name' in data else ''
            tags = str(data['tags']) if 'tags' in data else ''
            type = str(data['type']) if 'type' in data else ''
            unit = str(data['unit']) if 'unit' in data else ''
            unit_abbr = str(data['unit_abbr'].encode('ascii','ignore').strip()) if data['unit_abbr'] else str(data['unit_abbr']) if 'unit_abbr' in data else ''

            sql = """
                INSERT INTO preset
                (
                    id,
                    description,
                    display_name,
                    exclude_sex,
                    figure,
                    help_link_text,
                    help_link_url,
                    protocol_dependent_yn,
                    question,
                    short_display_name,
                    tags,
                    type,
                    unit,
                    unit_abbr
                )
                VALUES(
                    '""" + id + """',
                    '""" + description.replace("'", "\\'") + """',
                    '""" + display_name.replace("'", "\\'") + """',
                    '""" + exclude_sex + """',
                    '""" + figure + """',
                    '""" + help_link_text + """',
                    '""" + help_link_url + """',
                    """ + protocol_dependent_yn + """,
                    '""" + question + """',
                    '""" + short_display_name + """',
                    '""" + tags + """',
                    '""" + type + """',
                    '""" + unit + """',
                    '""" + unit_abbr + """'
                )
            """

            query(sql)
    if cursor < results['response']['remaining'] :
        insert_preset_data(tbl, cursor)

def insert_preset_array_data(tbl, cursor):
    results = send_api_request(str(tbl), cursor)
    for data in results['response']['results']:
        cursor += 1
        id = data['_id']
        get_sql = "SELECT id FROM preset_array WHERE id='%s'" % id  # Check if a preset already exist
        if not query(get_sql):
            amount = str(data['amount']) if 'amount' in data else '0'
            text = str(data['text'].encode('ascii','ignore').strip()) if data['text'] else str(data['text']) if 'text' in data else ''
            preset_id = str(data['preset']) if 'preset' in data else ''
            protocol_id = str(data['protocol']) if 'protocol' in data else ''

            if preset_id and protocol_id:
                sql = """INSERT INTO preset_array(id, amount, text, preset_id,  protocol_id)
                                    VALUES('"""+id+"""',
                                           '"""+amount+"""',
                                           '"""+text.replace("'", "\\'")+"""',
                                           '"""+preset_id+"""',
                                           '"""+protocol_id+"""'
                                           )"""
            elif preset_id and not protocol_id:
                sql = """INSERT INTO preset_array(id, amount, text, preset_id,  protocol_id)
                                    VALUES('""" + id + """',
                                           '""" + amount + """',
                                           '""" + text.replace("'", "\\'") + """',
                                           '""" + preset_id + """',
                                           Null
                                           )"""
            elif not preset_id and protocol_id:
                sql = """INSERT INTO preset_array(id, amount, text, preset_id,  protocol_id)
                                    VALUES('""" + id + """',
                                           '""" + amount + """',
                                           '""" + text.replace("'", "\\'") + """',
                                           Null,
                                           '"""+protocol_id+"""'
                                           )"""
            else:
                sql = """INSERT INTO preset_array(id, amount, text, preset_id,  protocol_id)
                                    VALUES('""" + id + """',
                                           '""" + amount + """',
                                           '""" + text.replace("'", "\\'") + """',
                                           Null,
                                           Null
                                           )"""

            query(sql)
    if cursor < results['response']['remaining'] :
        insert_preset_array_data(tbl, cursor)


def insert_protocol_data(tbl, cursor):
    results = send_api_request(str(tbl), cursor)
    for data in results['response']['results']:
        cursor += 1
        id = data['_id']
        get_sql = "SELECT id FROM protocol WHERE id='%s'" % id  # Check if a preset already exist
        if not query(get_sql):
            contact_email = str(data['contact_email']) if 'contact_email' in data else ''
            contact_name = str(data['contact_name']) if 'contact_name' in data else ''
            description =  str(data['description_200ch'].encode('ascii','ignore').strip()) if data['description_200ch'] else str(data['description_200ch']) if 'description_200ch' in data else ''
            display_name = str(data['display_name']) if 'display_name' in data else ''
            duration_days = str(data['duration_days']) if 'duration_days' in data else ''
            hypothesis = str(data['help_link_url']) if 'help_link_url' in data else ''
            video_youtube = str(data['video_youtube']) if 'video_youtube' in data else ''

            sql = """
                INSERT INTO protocol
                (
                    id,
                    contact_email,
                    contact_name,
                    description,
                    display_name,
                    duration_days,
                    hypothesis,
                    video_youtube
                )
                VALUES(
                    '""" + id + """',
                    '""" + contact_email + """',
                    '""" + contact_name + """',
                    '""" + description + """',
                    '""" + display_name + """',
                    '""" + duration_days + """',
                    '""" + hypothesis + """',
                    '""" + video_youtube + """'
                )
            """

            query(sql)
    if cursor < results['response']['remaining'] :
        insert_protocol_data(tbl, cursor)

def insert_protocol_array_data(tbl, cursor):
    results = send_api_request(str(tbl), cursor)
    for data in results['response']['results']:
        cursor += 1
        id = data['_id']
        get_sql = "SELECT id FROM protocol_array WHERE id='%s'" % id  # Check if a preset already exist
        if not query(get_sql):
            actual_end_date = str(data['actual_end_date'].split("T")[0]) if 'actual_end_date' in data else ''
            planned_end_date = str(data['planned_end_date'].split("T")[0]) if 'planned_end_date' in data else ''
            scheduled_api_id = str(data['scheduled_api_id'].encode('ascii','ignore').strip()) if data['scheduled_api_id'] else str(data['scheduled_api_id']) if 'scheduled_api_id' in data else ''
            start_date = str(data['start_date'].split("T")[0]) if 'start_date' in data else ''
            tmplt_made_count = str(data['tmplt_made_count']) if 'tmplt_made_count' in data else '0'
            protocol_id = str(data['protocol']) if 'protocol' in data else ''

            sql = """
                INSERT INTO protocol_array
                (
                    id,
                    actual_end_date,
                    planned_end_date,
                    scheduled_api_id,
                    start_date,
                    tmplt_made_count,
                    protocol_id
                )
                VALUES(
                    '""" + id + """',
                    '""" + actual_end_date + """',
                    '""" + planned_end_date + """',
                    '""" + scheduled_api_id + """',
                    '""" + start_date + """',
                    """ + tmplt_made_count + """,
                    '""" + protocol_id + """'
                )
            """

            query(sql)
    if cursor < results['response']['remaining'] :
        insert_protocol_array_data(tbl, cursor)

def insert_scale_option_data(tbl, cursor):
    results = send_api_request(str(tbl), cursor)
    for data in results['response']['results']:
        cursor += 1
        id = data['_id']
        get_sql = "SELECT id FROM scale_option WHERE id='%s'" % id  # Check if a preset already exist
        if not query(get_sql):
            label = str(data['label']) if 'label' in data else ''
            value = str(data['value']) if 'value' in data else 0

            sql = """
                INSERT INTO scale_option
                (
                    id,
                    label,
                    value
                )
                VALUES(
                    '""" + id + """',
                    '""" + label + """',
                    '""" + value + """'
                )
            """

            query(sql)

    if cursor < results['response']['remaining'] :
        insert_protocol_array_data(tbl, cursor)
#
# if __name__ == "__main__":
#     tableList = ["user", "scale_option", "preset", "protocol" "preset_array", "protocol_array",
#                   "entry"]
#     for tbl in tableList:
#         if tbl == 'user':
#             insert_user_data(str(tbl), 0)
#         elif tbl == 'entry':
#             insert_entry_data(str(tbl), 0)
#         elif tbl == 'preset':
#             insert_preset_data(str(tbl), 0)
#         elif tbl == 'preset_array':
#             insert_preset_array_data(str(tbl), 2780)
#         elif tbl == 'protocol':
#             insert_protocol_data(str(tbl), 0)
#         elif tbl == 'protocol_array':
#             insert_protocol_array_data(str(tbl), 0)
#         elif tbl == 'scale_option':
#             insert_scale_option_data(str(tbl), 0)


def run_cron_job():
    tableList = ["user", "scale_option", "preset", "protocol" "preset_array", "protocol_array",
                 "entry"]
    for tbl in tableList:
        print '>>>>>>>>>>>>>>>>>>>>>'
        if tbl == 'user':
            insert_user_data(str(tbl), 0)
        elif tbl == 'entry':
            insert_entry_data(str(tbl), 0)
        elif tbl == 'preset':
            insert_preset_data(str(tbl), 0)
        elif tbl == 'preset_array':
            insert_preset_array_data(str(tbl), 4327)
        elif tbl == 'protocol':
            insert_protocol_data(str(tbl), 0)
        elif tbl == 'protocol_array':
            insert_protocol_array_data(str(tbl), 0)
        elif tbl == 'scale_option':
            insert_scale_option_data(str(tbl), 0)

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/trackwell.pid'
        self.pidfile_timeout = 5
    def run(self):
        run_cron_job()


app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()