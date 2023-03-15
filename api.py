from flask import Flask, jsonify, request
from flask import Response
from werkzeug.exceptions import BadRequestKeyError
from ecom_my_target import MyTargetEcomru
from flasgger import Swagger, swag_from
from config import Configuration
from get_token import get_token
import logger
# from db_work import put_query
import psycopg2
from sqlalchemy import create_engine
import os


logger = logger.init_logger()

host = os.environ.get('ECOMRU_PG_HOST', None)
port = os.environ.get('ECOMRU_PG_PORT', None)
ssl_mode = os.environ.get('ECOMRU_PG_SSL_MODE', None)
db_name = os.environ.get('ECOMRU_PG_DB_NAME', None)
user = os.environ.get('ECOMRU_PG_USER', None)
password = os.environ.get('ECOMRU_PG_PASSWORD', None)
target_session_attrs = 'read-write'

# host = 'localhost'
# port = '5432'
# db_name = 'postgres'
# user = 'postgres'
# password = ' '

db_params = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
engine = create_engine(db_params)

app = Flask(__name__)
app.config.from_object(Configuration)
app.config['SWAGGER'] = {"title": "GTCOM-MyTargetAPI", "uiversion": 3}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json()",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/",
}

swagger = Swagger(app, config=swagger_config)


class HttpError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


def to_boolean(x):
    if x == "true":
        return True
    elif x == "false":
        return False
    else:
        return None


@app.after_request
def apply_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "content-type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST"
    return response


@app.route('/mytarget/getcampaigns', methods=['POST'])
@swag_from("swagger_conf/get_campaigns.yml")
def get_campaigns():
    """Получить список существующих рекламных кампаний"""

    try:
        json_file = request.get_json(force=False)

        client_id = json_file["client_id"]
        access_token = get_token(client_id=client_id, json_file=json_file, engine=engine, logger=logger)

        mt = MyTargetEcomru(client_id=client_id, access_token=access_token)

        res = mt.get_campaigns()

        # print(res, type(res))

        if res["code"] == 200:
            logger.info(f"get campaigns: 200")
            return jsonify(res["res"])
        else:
            logger.error(f"""get campaigns: {res["code"]}""")
            return jsonify(res)

    except BadRequestKeyError:
        logger.error("get campaigns: BadRequest")
        return Response(None, 400)

    except KeyError:
        logger.error("get campaigns: KeyError")
        return Response(None, 400)

    except BaseException as ex:
        logger.error(f'get campaigns: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/mytarget/getcampaigninfo', methods=['POST'])
@swag_from("swagger_conf/get_campaign_info.yml")
def get_campaign_info():
    """Получить информацию о кампании"""

    try:
        json_file = request.get_json(force=False)

        client_id = json_file["client_id"]
        access_token = get_token(client_id=client_id, json_file=json_file, engine=engine, logger=logger)

        mt = MyTargetEcomru(client_id=client_id, access_token=access_token)

        campaign_id = json_file["campaign_id"]

        res = mt.get_campaign_info(campaign_id)

        if res.status_code == 200:
            logger.info(f"get campaign info: 200")
            return jsonify(res.json())
        else:
            logger.error(f"get campaign info: {res.status_code}")
            return jsonify(res.json())

    except BadRequestKeyError:
        logger.error("get campaign info: BadRequest")
        return Response(None, 400)

    except KeyError:
        logger.error("get campaign info: KeyError")
        return Response(None, 400)

    except BaseException as ex:
        logger.error(f'get campaign info: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/mytarget/getpackages', methods=['POST'])
@swag_from("swagger_conf/get_packages.yml")
def get_packages():
    """Получить информацию о пакетах"""

    try:
        json_file = request.get_json(force=False)

        client_id = json_file["client_id"]
        access_token = get_token(client_id=client_id, json_file=json_file, engine=engine, logger=logger)

        mt = MyTargetEcomru(client_id=client_id, access_token=access_token)

        res = mt.get_packages()

        if res.status_code == 200:
            logger.info(f"get packages: 200")
            return jsonify(res.json())
        else:
            logger.error(f"get packages: {res.status_code}")
            return jsonify(res.json())

    except BadRequestKeyError:
        logger.error("get packages: BadRequest")
        return Response(None, 400)

    except KeyError:
        logger.error("get packages: KeyError")
        return Response(None, 400)

    except BaseException as ex:
        logger.error(f'get packages: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/mytarget/getbannerformats', methods=['POST'])
@swag_from("swagger_conf/get_banner_formats.yml")
def get_banner_formats():
    """Получить информацию о баннерных форматах"""

    try:
        json_file = request.get_json(force=False)

        client_id = json_file["client_id"]
        access_token = get_token(client_id=client_id, json_file=json_file, engine=engine, logger=logger)

        mt = MyTargetEcomru(client_id=client_id, access_token=access_token)

        res = mt.get_banner_formats()

        if res.status_code == 200:
            logger.info(f"get banner formats: 200")
            return jsonify(res.json())
        else:
            logger.error(f"get banner formats: {res.status_code}")
            return jsonify(res.json())

    except BadRequestKeyError:
        logger.error("get banner formats: BadRequest")
        return Response(None, 400)

    except KeyError:
        logger.error("get banner formats: KeyError")
        return Response(None, 400)

    except BaseException as ex:
        logger.error(f'get banner formats: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/mytarget/getpadstrees', methods=['POST'])
@swag_from("swagger_conf/get_pads_trees.yml")
def get_pads_trees():
    """
    Получить информацию о деревьях площадок, используемых в таргетинге на места размещений (pads) при создании кампаний
    """

    try:
        json_file = request.get_json(force=False)

        client_id = json_file["client_id"]
        access_token = get_token(client_id=client_id, json_file=json_file, engine=engine, logger=logger)

        mt = MyTargetEcomru(client_id=client_id, access_token=access_token)

        res = mt.get_pads_trees()

        if res.status_code == 200:
            logger.info(f"get pads trees: 200")
            return jsonify(res.json())
        else:
            logger.error(f"get pads trees: {res.status_code}")
            return jsonify(res.json())

    except BadRequestKeyError:
        logger.error("get pads trees: BadRequest")
        return Response(None, 400)

    except KeyError:
        logger.error("get pads trees: KeyError")
        return Response(None, 400)

    except BaseException as ex:
        logger.error(f'get pads trees: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/mytarget/getbannerpatterns', methods=['POST'])
@swag_from("swagger_conf/get_banner_patterns.yml")
def get_banner_patterns():
    """
    Получить реестр паттернов
    """

    try:
        json_file = request.get_json(force=False)

        client_id = json_file["client_id"]
        access_token = get_token(client_id=client_id, json_file=json_file, engine=engine, logger=logger)

        mt = MyTargetEcomru(client_id=client_id, access_token=access_token)

        res = mt.get_banner_patterns()

        if res.status_code == 200:
            logger.info(f"get banner patterns: 200")
            return jsonify(res.json())
        else:
            logger.error(f"get banner patterns: {res.status_code}")
            return jsonify(res.json())

    except BadRequestKeyError:
        logger.error("get banner patterns: BadRequest")
        return Response(None, 400)

    except KeyError:
        logger.error("get banner patterns: KeyError")
        return Response(None, 400)

    except BaseException as ex:
        logger.error(f'get banner patterns: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/mytarget/getbanners', methods=['POST'])
@swag_from("swagger_conf/get_banners.yml")
def get_banners():
    """Получить список всех рекламных объявлений пользователя"""

    try:
        json_file = request.get_json(force=False)

        client_id = json_file["client_id"]
        access_token = get_token(client_id=client_id, json_file=json_file, engine=engine, logger=logger)

        mt = MyTargetEcomru(client_id=client_id, access_token=access_token)

        res = mt.get_banners()

        if res["code"] == 200:
            logger.info(f"get campaigns: 200")
            return jsonify(res["res"])
        else:
            logger.error(f"""get campaigns: {res["code"]}""")
            return jsonify(res)

    except BadRequestKeyError:
        logger.error("get banners: BadRequest")
        return Response(None, 400)

    except KeyError:
        logger.error("get banners: KeyError")
        return Response(None, 400)

    except BaseException as ex:
        logger.error(f'get banners: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/mytarget/addcampaign', methods=['POST'])
@swag_from("swagger_conf/add_campaign.yml")
def add_campaign():
    """Создать кампанию"""

    try:
        json_file = request.get_json(force=False)

        client_id = json_file["client_id"]
        access_token = get_token(client_id=client_id, json_file=json_file, engine=engine, logger=logger)

        mt = MyTargetEcomru(client_id=client_id, access_token=access_token)

        t_age_list = json_file.get("t_age_list", None)
        t_age_expand = to_boolean(json_file.get("t_age_expand", None))
        t_birthday_days_after = json_file.get("t_birthday_days_after", None)
        t_birthday_days_before = json_file.get("t_birthday_days_before", None)
        t_fulltime_flags = json_file.get("t_fulltime_flags", None)
        t_fulltime_fri = json_file.get("t_fulltime_fri", None)
        t_fulltime_mon = json_file.get("t_fulltime_mon", None)
        t_fulltime_sat = json_file.get("t_fulltime_sat", None)
        t_fulltime_sun = json_file.get("t_fulltime_sun", None)
        t_fulltime_thu = json_file.get("t_fulltime_thu", None)
        t_fulltime_tue = json_file.get("t_fulltime_tue", None)
        t_fulltime_wed = json_file.get("t_fulltime_wed", None)
        t_geo_regions = json_file.get("t_geo_regions", None)
        t_geo_local_type = json_file.get("t_geo_local_type", None)
        t_geo_local_visit_type = json_file.get("t_geo_local_visit_type", None)
        t_geo_local_addresses = json_file.get("t_geo_local_addresses", None)
        t_geo_local_labels = json_file.get("t_geo_local_labels", None)
        t_geo_local_lats = json_file.get("t_geo_local_lats", None)
        t_geo_local_lngs = json_file.get("t_geo_local_lngs", None)
        t_geo_local_rads = json_file.get("t_geo_local_rads", None)
        t_group_members = json_file.get("t_group_members", None)
        t_interests = json_file.get("t_interests", None)
        t_interests_soc_dem = json_file.get("t_interests_soc_dem", None)
        t_interests_stable = json_file.get("t_interests_stable", None)
        t_mobile_apps = json_file.get("t_mobile_apps", None)
        t_mobile_operation_systems = json_file.get("t_mobile_operation_systems", None)
        t_mobile_operators = json_file.get("t_mobile_operators", None)
        t_mobile_prefix = json_file.get("t_mobile_prefix", None)
        t_mobile_types = json_file.get("t_mobile_types", None)
        t_mobile_vendors = json_file.get("t_mobile_vendors", None)
        t_pad_category_android = json_file.get("t_pad_category_android", None)
        t_pad_category_ios = json_file.get("t_pad_category_ios", None)
        t_pads = json_file.get("t_pads", None)
        t_regions = json_file.get("t_regions", None)
        t_segments = json_file.get("t_segments", None)
        t_sex = json_file.get("t_sex", None)
        t_sk_ad_network_app_url_id = json_file.get("t_sk_ad_network_app_url_id", None)
        t_sk_ad_network_mobile_operation_systems_ids = json_file.get("t_sk_ad_network_mobile_operation_systems_ids",
                                                                     None)

        targetings = mt.targetings(t_age_list, t_age_expand, t_birthday_days_after, t_birthday_days_before,
                                   t_fulltime_flags, t_fulltime_fri, t_fulltime_mon, t_fulltime_sat, t_fulltime_sun,
                                   t_fulltime_thu, t_fulltime_tue, t_fulltime_wed, t_geo_regions, t_geo_local_type,
                                   t_geo_local_visit_type, t_geo_local_addresses, t_geo_local_labels, t_geo_local_lats,
                                   t_geo_local_lngs, t_geo_local_rads, t_group_members, t_interests,
                                   t_interests_soc_dem, t_interests_stable, t_mobile_apps, t_mobile_operation_systems,
                                   t_mobile_operators, t_mobile_prefix, t_mobile_types, t_mobile_vendors,
                                   t_pad_category_android, t_pad_category_ios, t_pads, t_regions, t_segments, t_sex,
                                   t_sk_ad_network_app_url_id, t_sk_ad_network_mobile_operation_systems_ids)

        if targetings is None:
            logger.error("add campaign: targeting params incorrect")
            return jsonify({'error': 'targeting params incorrect'})
        else:

            name = json_file["name"]
            package_id = json_file["package_id"]
            objective = json_file.get("objective", None)
            age_restrictions = json_file.get("age_restrictions", None)
            audit_pixels_urls = json_file.get("audit_pixels_urls", None)
            audit_pixels_roles = json_file.get("audit_pixels_roles", None)
            autobidding_mode = json_file.get("autobidding_mode", None)
            banner_uniq_shows_limit = json_file.get("banner_uniq_shows_limit", None)
            banners = json_file.get("banners", None)
            budget_limit = json_file.get("budget_limit", None)
            budget_limit_day = json_file.get("budget_limit_day", None)
            date_end = json_file.get("date_end", None)
            date_start = json_file.get("date_start", None)
            dynamic_banners_use_storelink = to_boolean(json_file.get("dynamic_banners_use_storelink", None))
            dynamic_without_remarketing = to_boolean(json_file.get("dynamic_without_remarketing", None))
            enable_offline_goals = to_boolean(json_file.get("enable_offline_goals", None))
            enable_utm = to_boolean(json_file.get("enable_utm", None))
            language = json_file.get("language", None)
            marketplace_app_client_id = json_file.get("marketplace_app_client_id", None)
            max_price = json_file.get("max_price", None)
            mixing = json_file.get("mixing", None)
            price = json_file.get("price", None)
            priced_goal_name = json_file.get("priced_goal_name", None)
            priced_goal_source_id = json_file.get("priced_goal_source_id", None)
            pricelist_id = json_file.get("pricelist_id", None)
            social = to_boolean(json_file.get("social", None))
            status = json_file.get("status", None)
            uniq_shows_limit = json_file.get("uniq_shows_limit", None)
            uniq_shows_period = json_file.get("uniq_shows_period", None)
            utm = json_file.get("utm", None)

            res = mt.add_campaign(name, package_id, objective, age_restrictions, audit_pixels_urls, audit_pixels_roles,
                                  autobidding_mode, banner_uniq_shows_limit, banners, budget_limit, budget_limit_day,
                                  date_end, date_start, dynamic_banners_use_storelink, dynamic_without_remarketing,
                                  enable_offline_goals, enable_utm, language, marketplace_app_client_id, max_price,
                                  mixing, price, priced_goal_name, priced_goal_source_id, pricelist_id, social, status,
                                  targetings, uniq_shows_limit, uniq_shows_period, utm)

            # put_query(json_file=json_file, table_name='mytarget_add_campaigns', result=res, engine=engine, logger=logger)

            if res.status_code == 200 or res.status_code == 204:
                logger.info(f"add campaign: {res.status_code}")
                return jsonify(res.json())
            elif res.status_code == 400 or res.status_code == 401:
                logger.info(f"add campaign: {res.status_code}")
                return jsonify({'error': res.json(), 'status_code': res.status_code})
            elif res is None:
                logger.error("add campaign: incorrect input params")
                return jsonify({'error': "add campaign: incorrect input params"})
            else:
                logger.error(f"add campaign: mytarget api error {res.status_code}")
                return jsonify({'error': 'mytarget api error', 'code': f"{res.status_code}"})


    except BadRequestKeyError:
        logger.error("add campaign: BadRequest")
        return Response(None, 400)

    except KeyError:
        logger.error("add campaign: KeyError")
        return Response(None, 400)

    except BaseException as ex:
        logger.error(f'add campaign: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/mytarget/updatecampaign', methods=['POST'])
@swag_from("swagger_conf/update_campaign.yml")
def update_campaign():
    """Редактировать кампанию"""

    try:
        json_file = request.get_json(force=False)

        client_id = json_file["client_id"]
        access_token = get_token(client_id=client_id, json_file=json_file, engine=engine, logger=logger)

        mt = MyTargetEcomru(client_id=client_id, access_token=access_token)

        campaign_id = json_file["campaign_id"]

        t_age_list = json_file.get("t_age_list", None)
        t_age_expand = to_boolean(json_file.get("t_age_expand", None))
        t_birthday_days_after = json_file.get("t_birthday_days_after", None)
        t_birthday_days_before = json_file.get("t_birthday_days_before", None)
        t_fulltime_flags = json_file.get("t_fulltime_flags", None)
        t_fulltime_fri = json_file.get("t_fulltime_fri", None)
        t_fulltime_mon = json_file.get("t_fulltime_mon", None)
        t_fulltime_sat = json_file.get("t_fulltime_sat", None)
        t_fulltime_sun = json_file.get("t_fulltime_sun", None)
        t_fulltime_thu = json_file.get("t_fulltime_thu", None)
        t_fulltime_tue = json_file.get("t_fulltime_tue", None)
        t_fulltime_wed = json_file.get("t_fulltime_wed", None)
        t_geo_regions = json_file.get("t_geo_regions", None)
        t_geo_local_type = json_file.get("t_geo_local_type", None)
        t_geo_local_visit_type = json_file.get("t_geo_local_visit_type", None)
        t_geo_local_addresses = json_file.get("t_geo_local_addresses", None)
        t_geo_local_labels = json_file.get("t_geo_local_labels", None)
        t_geo_local_lats = json_file.get("t_geo_local_lats", None)
        t_geo_local_lngs = json_file.get("t_geo_local_lngs", None)
        t_geo_local_rads = json_file.get("t_geo_local_rads", None)
        t_group_members = json_file.get("t_group_members", None)
        t_interests = json_file.get("t_interests", None)
        t_interests_soc_dem = json_file.get("t_interests_soc_dem", None)
        t_interests_stable = json_file.get("t_interests_stable", None)
        t_mobile_apps = json_file.get("t_mobile_apps", None)
        t_mobile_operation_systems = json_file.get("t_mobile_operation_systems", None)
        t_mobile_operators = json_file.get("t_mobile_operators", None)
        t_mobile_prefix = json_file.get("t_mobile_prefix", None)
        t_mobile_types = json_file.get("t_mobile_types", None)
        t_mobile_vendors = json_file.get("t_mobile_vendors", None)
        t_pad_category_android = json_file.get("t_pad_category_android", None)
        t_pad_category_ios = json_file.get("t_pad_category_ios", None)
        t_pads = json_file.get("t_pads", None)
        t_regions = json_file.get("t_regions", None)
        t_segments = json_file.get("t_segments", None)
        t_sex = json_file.get("t_sex", None)
        t_sk_ad_network_app_url_id = json_file.get("t_sk_ad_network_app_url_id", None)
        t_sk_ad_network_mobile_operation_systems_ids = json_file.get("t_sk_ad_network_mobile_operation_systems_ids",
                                                                     None)

        targetings = mt.targetings(t_age_list, t_age_expand, t_birthday_days_after, t_birthday_days_before,
                                   t_fulltime_flags, t_fulltime_fri, t_fulltime_mon, t_fulltime_sat, t_fulltime_sun,
                                   t_fulltime_thu, t_fulltime_tue, t_fulltime_wed, t_geo_regions, t_geo_local_type,
                                   t_geo_local_visit_type, t_geo_local_addresses, t_geo_local_labels, t_geo_local_lats,
                                   t_geo_local_lngs, t_geo_local_rads, t_group_members, t_interests,
                                   t_interests_soc_dem, t_interests_stable, t_mobile_apps, t_mobile_operation_systems,
                                   t_mobile_operators, t_mobile_prefix, t_mobile_types, t_mobile_vendors,
                                   t_pad_category_android, t_pad_category_ios, t_pads, t_regions, t_segments, t_sex,
                                   t_sk_ad_network_app_url_id, t_sk_ad_network_mobile_operation_systems_ids)

        if targetings is None:
            logger.error("update campaign: targeting params incorrect")
            return jsonify({'error': 'targeting params incorrect'})
        elif len(targetings) == 0:
            targetings = None
        else:
            pass

        name = json_file.get("name", None)
        package_id = json_file.get("package_id", None)
        objective = json_file.get("objective", None)
        age_restrictions = json_file.get("age_restrictions", None)
        audit_pixels_urls = json_file.get("audit_pixels_urls", None)
        audit_pixels_roles = json_file.get("audit_pixels_roles", None)
        autobidding_mode = json_file.get("autobidding_mode", None)
        banner_uniq_shows_limit = json_file.get("banner_uniq_shows_limit", None)
        budget_limit = json_file.get("budget_limit", None)
        budget_limit_day = json_file.get("budget_limit_day", None)
        date_end = json_file.get("date_end", None)
        date_start = json_file.get("date_start", None)
        dynamic_banners_use_storelink = to_boolean(json_file.get("dynamic_banners_use_storelink", None))
        dynamic_without_remarketing = to_boolean(json_file.get("dynamic_without_remarketing", None))
        enable_offline_goals = to_boolean(json_file.get("enable_offline_goals", None))
        enable_utm = to_boolean(json_file.get("enable_utm", None))
        language = json_file.get("language", None)
        marketplace_app_client_id = json_file.get("marketplace_app_client_id", None)
        max_price = json_file.get("max_price", None)
        mixing = json_file.get("mixing", None)
        price = json_file.get("price", None)
        priced_goal_name = json_file.get("priced_goal_name", None)
        priced_goal_source_id = json_file.get("priced_goal_source_id", None)
        pricelist_id = json_file.get("pricelist_id", None)
        social = to_boolean(json_file.get("social", None))
        status = json_file.get("status", None)
        uniq_shows_limit = json_file.get("uniq_shows_limit", None)
        uniq_shows_period = json_file.get("uniq_shows_period", None)
        utm = json_file.get("utm", None)

        res = mt.update_campaign(campaign_id, name, package_id, objective, age_restrictions, audit_pixels_urls,
                                 audit_pixels_roles, autobidding_mode, banner_uniq_shows_limit, budget_limit,
                                 budget_limit_day, date_end, date_start, dynamic_banners_use_storelink,
                                 dynamic_without_remarketing, enable_offline_goals, enable_utm, language,
                                 marketplace_app_client_id, max_price, mixing, price, priced_goal_name,
                                 priced_goal_source_id, pricelist_id, social, status, targetings, uniq_shows_limit,
                                 uniq_shows_period, utm)

        # put_query(json_file=json_file, table_name='mytarget_add_campaigns', result=res, engine=engine, logger=logger)

        if res.status_code == 200 or res.status_code == 204:
            logger.info(f"update campaign: {res.status_code}")
            return jsonify({'code': res.status_code})
        elif res.status_code == 400 or res.status_code == 401:
            logger.info(f"update campaign: {res.status_code}")
            return jsonify({'error': res.json(), 'status_code': res.status_code})
        # elif res is None:
        #     logger.error("add campaign: incorrect input params")
        #     return jsonify({'error': "add campaign: incorrect input params"})
        else:
            logger.error(f"update campaign: mytarget api error {res.status_code}")
            return jsonify({'error': 'mytarget api error', 'code': f"{res.status_code}"})

    except BadRequestKeyError:
        logger.error("update campaign: BadRequest")
        return Response(None, 400)

    except KeyError:
        logger.error("update campaign: KeyError")
        return Response(None, 400)

    except BaseException as ex:
        logger.error(f'update campaign: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/mytarget/deletecampaign', methods=['POST'])
@swag_from("swagger_conf/delete_campaign.yml")
def delete_campaign():
    """Удалить кампанию"""

    try:
        json_file = request.get_json(force=False)

        client_id = json_file["client_id"]
        access_token = get_token(client_id=client_id, json_file=json_file, engine=engine, logger=logger)

        mt = MyTargetEcomru(client_id=client_id, access_token=access_token)

        campaign_id = json_file["campaign_id"]

        res = mt.delete_campaign(campaign_id)

        if res.status_code == 200 or res.status_code == 204:
            logger.info(f"delete campaign: {res.status_code}")
            return jsonify({'code': res.status_code})
        elif res.status_code == 400 or res.status_code == 401:
            logger.info(f"delete campaign: {res.status_code}")
            return jsonify({'error': res.json(), 'status_code': res.status_code})
        else:
            logger.error(f"delete campaign: mytarget api error {res.status_code}")
            return jsonify({'error': 'mytarget api error', 'code': f"{res.status_code}"})

    except BadRequestKeyError:
        logger.error("delete campaign: BadRequest")
        return Response(None, 400)

    except KeyError:
        logger.error("delete campaign: KeyError")
        return Response(None, 400)

    except BaseException as ex:
        logger.error(f'delete campaign: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/mytarget/addbanner', methods=['POST'])
@swag_from("swagger_conf/add_banner.yml")
def add_banner():
    """Создать объявление внутри кампании"""

    try:
        json_file = request.get_json(force=False)

        client_id = json_file["client_id"]
        access_token = get_token(client_id=client_id, json_file=json_file, engine=engine, logger=logger)

        mt = MyTargetEcomru(client_id=client_id, access_token=access_token)

        campaign_id = json_file["campaign_id"]

        content_icon_id = json_file.get("content_icon_id", None)
        content_overlay_id = json_file.get("content_overlay_id", None)
        content_video_id = json_file.get("content_video_id", None)
        content_super_video_id = json_file.get("content_super_video_id", None)
        content_header_image_id = json_file.get("content_header_image_id", None)
        content_slide_image_id = json_file.get("content_slide_image_id", None)
        content_slides_images_ids = json_file.get("content_slides_images_ids", None)
        content_image_id = json_file.get("content_image_id", None)
        content_promo_image_id = json_file.get("content_promo_image_id", None)
        content_background_image_id = json_file.get("content_background_image_id", None)
        content_icon_square_id = json_file.get("content_icon_square_id", None)
        content_image_vertical_id = json_file.get("content_image_vertical_id", None)
        content_promo_image_vertical_id = json_file.get("content_promo_image_vertical_id", None)
        content_logo_image_id = json_file.get("content_logo_image_id", None)
        content_logo_id = json_file.get("content_logo_id", None)
        content_tpl_background_image_id = json_file.get("content_tpl_background_image_id", None)
        content_tpl_background_image_300_id = json_file.get("content_tpl_background_image_300_id", None)
        content_cover_id = json_file.get("content_cover_id", None)
        content_audio_id = json_file.get("content_audio_id", None)
        content_mail_main_id = json_file.get("content_mail_main_id", None)
        content_vk_feed_id = json_file.get("content_vk_feed_id", None)
        urls_primary_id = json_file.get("urls_primary_id", None)
        urls_header_click_id = json_file.get("urls_header_click_id", None)
        urls_slide_clicks_ids = json_file.get("urls_slide_clicks_ids", None)
        urls_slide_deeplinks_ids = json_file.get("urls_slide_deeplinks_ids", None)
        urls_ok_id = json_file.get("urls_ok_id", None)
        urls_vk_id = json_file.get("urls_vk_id", None)
        urls_links_ids = json_file.get("urls_links_ids", None)
        urls_link1_id = json_file.get("urls_link1_id", None)
        urls_deeplink_url_id = json_file.get("urls_deeplink_url_id", None)
        urls_android_store_url_id = json_file.get("urls_android_store_url_id", None)
        urls_android_tracking_url_id = json_file.get("urls_android_tracking_url_id", None)
        urls_android_url_id = json_file.get("urls_android_url_id", None)
        urls_ios_store_url_id = json_file.get("urls_ios_store_url_id", None)
        urls_ios_tracking_url_id = json_file.get("urls_ios_tracking_url_id", None)
        urls_ios_url_id = json_file.get("urls_ios_url_id", None)
        urls_shopitem_url_id = json_file.get("urls_shopitem_url_id", None)
        urls_slide_click_id = json_file.get("urls_slide_click_id", None)
        urls_logo_link_id = json_file.get("urls_logo_link_id", None)
        textblocks_primary_text = json_file.get("textblocks_primary_text", None)
        textblocks_primary_title = json_file.get("textblocks_primary_title", None)
        textblocks_header_text = json_file.get("textblocks_header_text", None)
        textblocks_header_title = json_file.get("textblocks_header_title", None)
        textblocks_header_button_text = json_file.get("textblocks_header_button_text", None)
        textblocks_slides_texts = json_file.get("textblocks_slides_texts", None)
        textblocks_slides_titles = json_file.get("textblocks_slides_titles", None)
        textblocks_about_company_text = json_file.get("textblocks_about_company_text", None)
        textblocks_slide_text = json_file.get("textblocks_slide_text", None)
        textblocks_slide_title = json_file.get("textblocks_slide_title", None)
        textblocks_slide_button_text = json_file.get("textblocks_slide_button_text", None)
        textblocks_button_title_text = json_file.get("textblocks_button_title_text", None)
        textblocks_link_title_text = json_file.get("textblocks_link_title_text", None)
        textblocks_billboard_video_text = json_file.get("textblocks_billboard_video_text", None)
        textblocks_position_text = json_file.get("textblocks_position_text", None)
        textblocks_tags_text = json_file.get("textblocks_tags_text", None)
        textblocks_selection_text = json_file.get("textblocks_selection_text", None)
        products_appearance_name = json_file.get("products_appearance_name", None)
        products_appearance_price = json_file.get("products_appearance_price", None)
        products_appearance_button = json_file.get("products_appearance_button", None)
        products_appearance_button_bg = json_file.get("products_appearance_button_bg", None)
        products_appearance_borders_inside = json_file.get("products_appearance_borders_inside", None)
        products_appearance_border = json_file.get("products_appearance_border", None)
        products_appearance_logo_bg = json_file.get("products_appearance_logo_bg", None)
        products_appearance_banner_bg = json_file.get("products_appearance_banner_bg", None)
        products_appearance_title = json_file.get("products_appearance_title", None)
        products_zoom = to_boolean(json_file.get("products_zoom", None))
        products_template_type = json_file.get("products_template_type", None)
        call_to_action = json_file.get("call_to_action", None)
        deeplink = json_file.get("deeplink", None)
        name = json_file.get("name", None)
        status = json_file.get("status", None)
        video_params_autoplay = to_boolean(json_file.get("video_params_autoplay", None))
        video_params_height = json_file.get("video_params_height", None)
        video_params_loop = to_boolean(json_file.get("video_params_loop", None))
        video_params_over_video = to_boolean(json_file.get("video_params_over_video", None))
        video_params_sound_delay = to_boolean(json_file.get("video_params_sound_delay", None))
        video_params_video_x = json_file.get("video_params_video_x", None)
        video_params_video_y = json_file.get("video_params_video_y", None)
        video_params_width = json_file.get("video_params_width", None)

        res = mt.add_banner(campaign_id,
                            content_icon_id,
                            content_overlay_id,
                            content_video_id,
                            content_super_video_id,
                            content_header_image_id,
                            content_slide_image_id,
                            content_slides_images_ids,
                            content_image_id,
                            content_promo_image_id,
                            content_background_image_id,
                            content_icon_square_id,
                            content_image_vertical_id,
                            content_promo_image_vertical_id,
                            content_logo_image_id,
                            content_logo_id,
                            content_tpl_background_image_id,
                            content_tpl_background_image_300_id,
                            content_cover_id,
                            content_audio_id,
                            content_mail_main_id,
                            content_vk_feed_id,
                            urls_primary_id,
                            urls_header_click_id,
                            urls_slide_clicks_ids,
                            urls_slide_deeplinks_ids,
                            urls_ok_id,
                            urls_vk_id,
                            urls_links_ids,
                            urls_link1_id,
                            urls_deeplink_url_id,
                            urls_android_store_url_id,
                            urls_android_tracking_url_id,
                            urls_android_url_id,
                            urls_ios_store_url_id,
                            urls_ios_tracking_url_id,
                            urls_ios_url_id,
                            urls_shopitem_url_id,
                            urls_slide_click_id,
                            urls_logo_link_id,
                            textblocks_primary_text,
                            textblocks_primary_title,
                            textblocks_header_text,
                            textblocks_header_title,
                            textblocks_header_button_text,
                            textblocks_slides_texts,
                            textblocks_slides_titles,
                            textblocks_about_company_text,
                            textblocks_slide_text,
                            textblocks_slide_title,
                            textblocks_slide_button_text,
                            textblocks_button_title_text,
                            textblocks_link_title_text,
                            textblocks_billboard_video_text,
                            textblocks_position_text,
                            textblocks_tags_text,
                            textblocks_selection_text,
                            products_appearance_name,
                            products_appearance_price,
                            products_appearance_button,
                            products_appearance_button_bg,
                            products_appearance_borders_inside,
                            products_appearance_border,
                            products_appearance_logo_bg,
                            products_appearance_banner_bg,
                            products_appearance_title,
                            products_zoom,
                            products_template_type,
                            call_to_action,
                            deeplink,
                            name,
                            status,
                            video_params_autoplay,
                            video_params_height,
                            video_params_loop,
                            video_params_over_video,
                            video_params_sound_delay,
                            video_params_video_x,
                            video_params_video_y,
                            video_params_width)

        # put_query(json_file=json_file, table_name='mytarget_add_banners', result=res, engine=engine, logger=logger)

        if res.status_code == 200 or res.status_code == 204:
            logger.info(f"add banner: {res.status_code}")
            return jsonify(res.json())
        elif res.status_code == 400 or res.status_code == 401:
            logger.info(f"add banner: {res.status_code}")
            return jsonify({'error': res.json(), 'status_code': res.status_code})
        else:
            logger.error(f"add banner: mytarget api error {res.status_code}")
            return jsonify({'error': 'mytarget api error', 'code': f"{res.status_code}"})

    except BadRequestKeyError:
        logger.error("add banner: BadRequest")
        return Response(None, 400)

    except KeyError:
        logger.error("add banner: KeyError")
        return Response(None, 400)

    except BaseException as ex:
        logger.error(f'add banner: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/mytarget/addurl', methods=['POST'])
@swag_from("swagger_conf/add_url.yml")
def add_url():
    """Создать url и отправить его на проверку"""

    try:
        json_file = request.get_json(force=False)

        client_id = json_file["client_id"]
        access_token = get_token(client_id=client_id, json_file=json_file, engine=engine, logger=logger)

        mt = MyTargetEcomru(client_id=client_id, access_token=access_token)

        url = json_file["url"]

        res = mt.add_url(url)

        if res.status_code == 200 or res.status_code == 201:
            logger.info(f"add url: {res.status_code}")
            return jsonify(res.json())
        elif res.status_code == 400 or res.status_code == 401:
            logger.info(f"add url: {res.status_code}")
            return jsonify({'error': res.json(), 'status_code': res.status_code, 'message': 'Ошибка валидации'})
        else:
            logger.error(f"add url: mytarget api error {res.status_code}")
            return jsonify({'error': 'mytarget api error', 'code': f"{res.status_code}"})

    except BadRequestKeyError:
        logger.error("add url: BadRequest")
        return Response(None, 400)

    except KeyError:
        logger.error("add url: KeyError")
        return Response(None, 400)

    except BaseException as ex:
        logger.error(f'add url: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/mytarget/readurls', methods=['POST'])
@swag_from("swagger_conf/read_urls.yml")
def read_urls():
    """Получить данные о рекламируемых ссылках"""

    try:
        json_file = request.get_json(force=False)

        client_id = json_file["client_id"]
        access_token = get_token(client_id=client_id, json_file=json_file, engine=engine, logger=logger)

        mt = MyTargetEcomru(client_id=client_id, access_token=access_token)

        urls = json_file["urls"]

        res = mt.read_urls(urls)

        if res.status_code == 200 or res.status_code == 201:
            logger.info(f"read urls: {res.status_code}")
            return jsonify(res.json())
        elif res.status_code == 400 or res.status_code == 401:
            logger.info(f"read urls: {res.status_code}")
            return jsonify({'error': res.json(), 'status_code': res.status_code})
        else:
            logger.error(f"read urls: mytarget api error {res.status_code}")
            return jsonify({'error': 'mytarget api error', 'code': f"{res.status_code}"})

    except BadRequestKeyError:
        logger.error("read urls: BadRequest")
        return Response(None, 400)

    except KeyError:
        logger.error("read urls: KeyError")
        return Response(None, 400)

    except BaseException as ex:
        logger.error(f'read urls: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/mytarget/addcontent', methods=['POST'])
@swag_from("swagger_conf/add_content.yml")
def add_content():
    """Загрузить креативы"""

    try:
        json_file = request.get_json(force=False)

        client_id = json_file["client_id"]
        access_token = get_token(client_id=client_id, json_file=json_file, engine=engine, logger=logger)

        mt = MyTargetEcomru(client_id=client_id, access_token=access_token)

        content_type = json_file["content_type"]
        file_string = json_file["file_string"]
        filename = json_file["filename"]
        width = json_file.get("width", None)
        height = json_file.get("height", None)

        res = mt.add_content(content_type=content_type, file_string=file_string, filename=filename,
                             width=width, height=height)

        if res.status_code == 200 or res.status_code == 201:
            logger.info(f"add content: {res.status_code}")
            return jsonify(res.json())
        elif res.status_code == 400 or res.status_code == 401:
            logger.info(f"add content: {res.status_code}")
            return jsonify({'error': res.json(), 'status_code': res.status_code})
        else:
            logger.error(f"add content: mytarget api error {res.status_code}")
            return jsonify({'error': 'mytarget api error', 'code': f"{res.status_code}"})

    except BadRequestKeyError:
        logger.error("add content: BadRequest")
        return Response(None, 400)

    except KeyError:
        logger.error("add content: KeyError")
        return Response(None, 400)

    except BaseException as ex:
        logger.error(f'add content: {ex}')
        raise HttpError(400, f'{ex}')




