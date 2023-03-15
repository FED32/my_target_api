import requests
from requests.exceptions import ConnectionError
import pandas as pd
import numpy as np
import json
import base64


class MyTargetEcomru:
    def __init__(self, client_id,
                 client_secret=None,
                 access_token=None,
                 refresh_token=None,
                 # code=None,
                 # redirect_uri=None
                 ):

        self.client_id = client_id
        self.client_secret = client_secret

        # self.redirect_uri = redirect_uri

        self.host = "https://target.my.com"

        try:
            if access_token is not None:
                self.access_token = access_token
            elif refresh_token is not None:
                self.access_token = self.refresh_access_token(refresh_token)["access_token"]
            else:
                self.access_token = None
        except ConnectionError:
            print("Произошла ошибка соединения с сервером API.")
            self.access_token = None
        except:
            print("Произошла непредвиденная ошибка.")
            self.access_token = None

    def get_client_token(self, permanent="false"):
        """Метод для получения клиентского токена"""

        url = f"{self.host}/api/v2/oauth2/token.json"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = f"grant_type=client_credentials&client_id={self.client_id}&client_secret={self.client_secret}"

        if permanent == "true":
            body += "&permanent=true"

        res = requests.post(url=url, headers=headers, data=body)

        if res.status_code == 200:
            return res.json()
        elif res.status_code == 403:
            return res.json()
        else:
            return None

    def refresh_access_token(self, refresh_token):
        """Метод для обновления токена доступа"""

        url = f"{self.host}/api/v2/oauth2/token.json"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = f"grant_type=refresh_token&refresh_token={refresh_token}&client_id={self.client_id}&client_secret={self.client_secret}"

        res = requests.post(url=url, headers=headers, data=body)

        if res.status_code == 200:
            return res.json()
        else:
            return None

    # def get_auth_link(self, client_id):
    #     """Формирует ссылку для авторизации"""
    #
    #     f"/oauth2/authorize?response_type=code&client_id={client_id}&state={state}&scope={scopes}&redirect_uri={self.redirect_uri}"
    #
    def delete_tokens(self):
        """"""
        url = f"{self.host}/api/v2/oauth2/token/delete.json"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = f"client_id={self.client_id}&client_secret={self.client_secret}"

        return requests.post(url=url, headers=headers, data=body)

    def get_campaigns(self, limit=250):
        """
        Получить список существующих рекламных кампаний
        https://target.my.com/doc/api/ru/resource/Campaigns#/api/v2/campaigns.json
        описание полей: https://target.my.com/doc/api/ru/object/Campaign
        """

        fields = [
            'id', 'name', 'objective', 'package_id', 'status', 'targetings',
            'age_restrictions', 'audit_pixels', 'autobidding_mode', 'banner_uniq_shows_limit', 'banners',
            'budget_limit', 'budget_limit_day', 'created', 'date_end', 'date_start', 'delivery',
            'dynamic_banners_use_storelink', 'dynamic_without_remarketing', 'enable_offline_goals', 'enable_utm',
            'issues', 'language', 'marketplace_app_client_id', 'max_price', 'mixing', 'package_priced_event_type',
            'price', 'priced_goal', 'pricelist_id', 'sk_ad_campaign_id', 'social', 'uniq_shows_limit',
            'uniq_shows_period', 'updated', 'utm'
        ]

        headers = {"Authorization": f"Bearer {self.access_token}"}

        offset = 0
        result = []
        while True:
            url = f"{self.host}/api/v2/campaigns.json?limit={limit}&offset={offset}&fields={','.join(fields)}"
            res = requests.get(url=url, headers=headers)
            if res.status_code == 200:
                if len(res.json()["items"]) > 0:
                    result += res.json()["items"]
                    offset += limit
                else:
                    return {"res": result, "code": 200}
            else:
                print(res.text)
                return {"res": res.text, "code": res.status_code}

    def get_campaign_info(self, campaign_id: int):
        """Получить информацию о кампании"""

        fields = [
            'id', 'name', 'objective', 'package_id', 'status', 'targetings',
            'age_restrictions', 'audit_pixels', 'autobidding_mode', 'banner_uniq_shows_limit', 'banners',
            'budget_limit', 'budget_limit_day', 'created', 'date_end', 'date_start', 'delivery',
            'dynamic_banners_use_storelink', 'dynamic_without_remarketing', 'enable_offline_goals', 'enable_utm',
            'issues', 'language', 'marketplace_app_client_id', 'max_price', 'mixing', 'package_priced_event_type',
            'price', 'priced_goal', 'pricelist_id', 'sk_ad_campaign_id', 'social', 'uniq_shows_limit',
            'uniq_shows_period', 'updated', 'utm'
        ]

        headers = {"Authorization": f"Bearer {self.access_token}"}

        url = f"{self.host}/api/v2/campaigns/{campaign_id}.json?fields={','.join(fields)}"

        return requests.get(url=url, headers=headers)

    def get_packages(self):
        """
        Получить информацию о пакетах
        https://target.my.com/doc/api/ru/resource/Packages
        """

        url = f"{self.host}/api/v2/packages.json"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        return requests.get(url=url, headers=headers)

    def get_banners(self, limit=250):
        """
        Получить список всех рекламных объявлений пользователя
        https://target.my.com/doc/api/ru/resource/Banners#/api/v2/banners.json
        поля
        """

        fields = [
            "id", "name", "campaign_id",
            "call_to_action", "content", "created", "deeplink", "delivery", "issues", "moderation_reasons",
            "moderation_status", "products", "status", "textblocks", "updated", "urls", "user_can_request_remoderation",
            "video_params"
        ]

        headers = {"Authorization": f"Bearer {self.access_token}"}

        offset = 0
        result = []
        while True:
            url = f"{self.host}/api/v2/banners.json?limit={limit}&offset={offset}&fields={','.join(fields)}"
            res = requests.get(url=url, headers=headers)
            if res.status_code == 200:
                if len(res.json()["items"]) > 0:
                    result += res.json()["items"]
                    offset += limit
                else:
                    return {"res": result, "code": 200}
            else:
                print(res.text)
                return {"res": res.text, "code": res.status_code}

    def get_banner_formats(self):
        """
        Информация о баннерных форматах
        https://target.my.com/doc/api/ru/resource/BannerFormats
        """
        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = f"{self.host}/api/v2/banner_formats.json"
        return requests.get(url=url, headers=headers)

    def get_pads_trees(self):
        """
        Информация о деревьях площадок, используемых в таргетинге на места размещений (pads) при создании кампаний.
        https://target.my.com/doc/api/ru/resource/PadsTree
        """
        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = f"{self.host}/api/v2/pads_trees.json"
        return requests.get(url=url, headers=headers)

    def get_banner_patterns(self):
        """
        Реестр паттернов
        https://target.my.com/doc/api/ru/resource/BannerPatterns
        """

        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = f"{self.host}/api/v2/banner_patterns.json"
        return requests.get(url=url, headers=headers)

    @staticmethod
    def targetings(t_age_list: list[int] = None,
                   t_age_expand: bool = None,
                   t_birthday_days_after: int = None,
                   t_birthday_days_before: int = None,
                   t_fulltime_flags: list[str] = None,
                   t_fulltime_fri: list[int] = None,
                   t_fulltime_mon: list[int] = None,
                   t_fulltime_sat: list[int] = None,
                   t_fulltime_sun: list[int] = None,
                   t_fulltime_thu: list[int] = None,
                   t_fulltime_tue: list[int] = None,
                   t_fulltime_wed: list[int] = None,
                   t_geo_regions: list[int] = None,
                   t_geo_local_type: list[str] = None,
                   t_geo_local_visit_type: str = None,
                   t_geo_local_addresses: list[str] = None,
                   t_geo_local_labels: list[str] = None,
                   t_geo_local_lats: list[float] = None,
                   t_geo_local_lngs: list[float] = None,
                   t_geo_local_rads: list[int] = None,
                   t_group_members: str = None,
                   t_interests: list[int] = None,
                   t_interests_soc_dem: list[int] = None,
                   t_interests_stable: list[int] = None,
                   t_mobile_apps: str = None,
                   t_mobile_operation_systems: list[int] = None,
                   t_mobile_operators: list[int] = None,
                   t_mobile_prefix: list[int] = None,
                   t_mobile_types: list[int] = None,
                   t_mobile_vendors: list[int] = None,
                   t_pad_category_android: list[int] = None,
                   t_pad_category_ios: list[int] = None,
                   t_pads: list[int] = None,
                   t_regions: list[int] = None,
                   t_segments: list[int] = None,
                   t_sex: list[str] = None,
                   t_sk_ad_network_app_url_id: int = None,
                   t_sk_ad_network_mobile_operation_systems_ids: list[int] = None
                   ):
        """
        Таргетинги
        https://target.my.com/doc/api/ru/object/Targetings
        """

        result = dict()

        if t_age_list is not None:
            result.setdefault("age", {"age_list": t_age_list})
            if t_age_expand is not None:
                result["age"].setdefault("expand", t_age_expand)

        if t_birthday_days_after and t_birthday_days_before:
            result.setdefault("birthday", {"days_after": t_birthday_days_after, "days_before": t_birthday_days_before})

        fulltime = dict()
        if t_fulltime_flags is not None:
            fulltime.setdefault("flags", t_fulltime_flags)
        if t_fulltime_fri is not None:
            fulltime.setdefault("fri", t_fulltime_fri)
        if t_fulltime_mon is not None:
            fulltime.setdefault("mon", t_fulltime_mon)
        if t_fulltime_sat is not None:
            fulltime.setdefault("sat", t_fulltime_sat)
        if t_fulltime_sun is not None:
            fulltime.setdefault("sun", t_fulltime_sun)
        if t_fulltime_thu is not None:
            fulltime.setdefault("thu", t_fulltime_thu)
        if t_fulltime_tue is not None:
            fulltime.setdefault("tue", t_fulltime_thu)
        if t_fulltime_wed is not None:
            fulltime.setdefault("wed", t_fulltime_wed)
        if len(fulltime) > 0:
            result.setdefault("fulltime", fulltime)

        if t_geo_regions is not None:
            result.setdefault("geo", {})
            result["geo"].setdefault("regions", t_geo_regions)

        else:

            if t_geo_local_type is not None:
                result.setdefault("local_geo", {})
                result["local_geo"].setdefault("loc_type", t_geo_local_type)

            if t_geo_local_visit_type is not None:
                result.setdefault("local_geo", {})
                result["local_geo"].setdefault("visit_type", t_geo_local_visit_type)

            if t_geo_local_lats is not None and t_geo_local_lngs is not None and t_geo_local_rads is not None:
                if t_geo_local_addresses is not None and t_geo_local_labels is not None:
                    locations = [{"lat": a, "lng": b, "radius": c, "address": d, "label": e} for a, b, c, d, e in
                                 zip(t_geo_local_lats, t_geo_local_lngs, t_geo_local_rads, t_geo_local_addresses,
                                     t_geo_local_labels)]
                elif t_geo_local_addresses is not None and t_geo_local_labels is None:
                    locations = [{"lat": a, "lng": b, "radius": c, "address": d} for a, b, c, d in
                                 zip(t_geo_local_lats, t_geo_local_lngs, t_geo_local_rads, t_geo_local_addresses)]
                elif t_geo_local_addresses is None and t_geo_local_labels is not None:
                    locations = [{"lat": a, "lng": b, "radius": c, "label": d} for a, b, c, d in
                                 zip(t_geo_local_lats, t_geo_local_lngs, t_geo_local_rads, t_geo_local_labels)]
                else:
                    locations = [{"lat": a, "lng": b, "radius": c} for a, b, c in
                                 zip(t_geo_local_lats, t_geo_local_lngs, t_geo_local_rads)]

                result.setdefault("local_geo", {})
                result["local_geo"].setdefault("locations", locations)

        if t_group_members is not None:
            result.setdefault("group_members", t_group_members)

        if t_interests is not None:
            result.setdefault("interests", t_interests)

        if t_interests_soc_dem is not None:
            result.setdefault("interests_soc_dem", t_interests_soc_dem)

        if t_interests_stable is not None:
            result.setdefault("interests_stable", t_interests_stable)

        if t_mobile_apps is not None:
            result.setdefault("mobile_apps", t_mobile_apps)

        if t_mobile_operation_systems is not None:
            result.setdefault("mobile_operation_systems", t_mobile_operation_systems)

        if t_mobile_operators is not None:
            result.setdefault("mobile_operators", t_mobile_operators)

        if t_mobile_prefix is not None:
            result.setdefault("mobile_prefix", t_mobile_prefix)

        if t_mobile_types is not None:
            result.setdefault("mobile_types", t_mobile_types)

        if t_mobile_vendors is not None:
            result.setdefault("mobile_vendors", t_mobile_vendors)

        if t_pad_category_android is not None:
            result.setdefault("pad_category", {})
            result["pad_category"].setdefault("Android", t_pad_category_android)
        if t_pad_category_ios is not None:
            result.setdefault("pad_category", {})
            result["pad_category"].setdefault("iOS", t_pad_category_ios)

        if t_pads is not None:
            result.setdefault("pads", t_pads)

        if t_regions is not None:
            result.setdefault("regions", t_regions)

        if t_segments is not None:
            result.setdefault("segments", t_segments)

        if t_sex is not None:
            result.setdefault("sex", t_sex)

        if t_sk_ad_network_app_url_id is not None:
            result.setdefault("mobile_operation_systems_sk_ad_network", {})
            result["mobile_operation_systems_sk_ad_network"].setdefault("app_url_id", t_sk_ad_network_app_url_id)
        if t_sk_ad_network_mobile_operation_systems_ids is not None:
            result.setdefault("mobile_operation_systems_sk_ad_network", {})
            result["mobile_operation_systems_sk_ad_network"].setdefault("mobile_operation_systems_ids",
                                                                        t_sk_ad_network_mobile_operation_systems_ids)

        return result

    def add_campaign(self, name: str,
                     package_id: int,
                     objective: str = None,
                     age_restrictions: str = None,
                     audit_pixels_urls: list[str] = None,
                     audit_pixels_roles: list[str] = None,
                     autobidding_mode: str = None,
                     banner_uniq_shows_limit: int = None,
                     banners: list[dict] = None,
                     budget_limit: float = None,
                     budget_limit_day: float = None,
                     date_end: str = None,
                     date_start: str = None,
                     dynamic_banners_use_storelink: bool = None,
                     dynamic_without_remarketing: bool = None,
                     enable_offline_goals: bool = None,
                     enable_utm: bool = None,
                     language: str = None,
                     marketplace_app_client_id: str = None,
                     max_price: float = None,
                     mixing: str = None,
                     price: float = None,
                     priced_goal_name: str = None,
                     priced_goal_source_id: int = None,
                     pricelist_id: int = None,
                     social: bool = None,
                     status: str = None,
                     targetings: dict = None,
                     uniq_shows_limit: int = None,
                     uniq_shows_period: str = None,
                     utm: str = None
                     ):
        """
        Создать кампанию
        https://target.my.com/doc/api/ru/resource/Campaigns#/api/v2/campaigns.json
        поля: https://target.my.com/doc/api/ru/object/Campaign
        """

        url = f"{self.host}/api/v2/campaigns.json"

        headers = {
            # "Content-Type": "application/x-www-form-urlencoded",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        body = {
            "name": name,
            "package_id": package_id
        }

        if objective is not None:
            body.setdefault("objective", objective)

        if age_restrictions is not None:
            body.setdefault("age_restrictions", age_restrictions)

        if audit_pixels_urls is not None and audit_pixels_roles is not None:
            if len(audit_pixels_urls) == len(audit_pixels_roles):
                audit_pixels = [{'audit_pixel': a, 'role': b} for a, b in zip(audit_pixels_urls, audit_pixels_roles)]
                body.setdefault("audit_pixels", audit_pixels)
            else:
                print("incorrect audit pixels")
                return None

        if autobidding_mode is not None:
            body.setdefault("autobidding_mode", autobidding_mode)

        if banner_uniq_shows_limit is not None:
            body.setdefault("banner_uniq_shows_limit", banner_uniq_shows_limit)

        if banners is not None:
            body.setdefault("banners", banners)

        if budget_limit is not None:
            body.setdefault("budget_limit", budget_limit)

        if budget_limit_day is not None:
            body.setdefault("budget_limit_day", budget_limit_day)

        if date_end is not None:
            body.setdefault("date_end", date_end)

        if date_start is not None:
            body.setdefault("date_start", date_start)

        if dynamic_banners_use_storelink is not None:
            body.setdefault("dynamic_banners_use_storelink", dynamic_banners_use_storelink)

        if dynamic_without_remarketing is not None:
            body.setdefault("dynamic_without_remarketing", dynamic_without_remarketing)

        if enable_offline_goals is not None:
            body.setdefault("enable_offline_goals", enable_offline_goals)

        if enable_utm is not None:
            body.setdefault("enable_utm", enable_utm)

        if language is not None:
            body.setdefault("language", language)

        if marketplace_app_client_id is not None:
            body.setdefault("marketplace_app_client_id", marketplace_app_client_id)

        if max_price is not None:
            body.setdefault("max_price", max_price)

        if mixing is not None:
            body.setdefault("mixing", mixing)

        if price is not None:
            body.setdefault("price", price)

        if priced_goal_name is not None and priced_goal_source_id is not None:
            body.setdefault("priced_goal", {"name": priced_goal_name, "source_id": priced_goal_source_id})

        if pricelist_id is not None:
            body.setdefault("pricelist_id", pricelist_id)

        if social is not None:
            body.setdefault("social", social)

        if status is not None:
            body.setdefault("status", status)

        if targetings is not None:
            body.setdefault("targetings", targetings)

        if uniq_shows_limit is not None:
            body.setdefault("uniq_shows_limit", uniq_shows_limit)

        if uniq_shows_period is not None:
            body.setdefault("uniq_shows_period", uniq_shows_period)

        if utm is not None:
            body.setdefault("utm", utm)

        # body = f"name={name}&package_id={package_id}"
        # print(json.dumps(body))

        return requests.post(url=url, headers=headers, data=json.dumps(body))

    def update_campaign(self,
                        campaign_id: int,
                        name: str = None,
                        package_id: int = None,
                        objective: str = None,
                        age_restrictions: str = None,
                        audit_pixels_urls: list[str] = None,
                        audit_pixels_roles: list[str] = None,
                        autobidding_mode: str = None,
                        banner_uniq_shows_limit: int = None,
                        budget_limit: float = None,
                        budget_limit_day: float = None,
                        date_end: str = None,
                        date_start: str = None,
                        dynamic_banners_use_storelink: bool = None,
                        dynamic_without_remarketing: bool = None,
                        enable_offline_goals: bool = None,
                        enable_utm: bool = None,
                        language: str = None,
                        marketplace_app_client_id: str = None,
                        max_price: float = None,
                        mixing: str = None,
                        price: float = None,
                        priced_goal_name: str = None,
                        priced_goal_source_id: int = None,
                        pricelist_id: int = None,
                        social: bool = None,
                        status: str = None,
                        targetings: dict = None,
                        uniq_shows_limit: int = None,
                        uniq_shows_period: str = None,
                        utm: str = None):
        """
        Редактировать кампанию
        https://target.my.com/doc/api/ru/resource/Campaign
        """

        url = f"{self.host}/api/v2/campaigns/{campaign_id}.json"

        headers = {
            # "Content-Type": "application/x-www-form-urlencoded",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        body = dict()

        if name is not None:
            body.setdefault("name", name)

        if package_id is not None:
            body.setdefault("package_id", package_id)

        if objective is not None:
            body.setdefault("objective", objective)

        if age_restrictions is not None:
            body.setdefault("age_restrictions", age_restrictions)

        if audit_pixels_urls is not None and audit_pixels_roles is not None:
            if len(audit_pixels_urls) == len(audit_pixels_roles):
                audit_pixels = [{'audit_pixel': a, 'role': b} for a, b in zip(audit_pixels_urls, audit_pixels_roles)]
                body.setdefault("audit_pixels", audit_pixels)
            else:
                print("incorrect audit pixels")
                return None

        if autobidding_mode is not None:
            body.setdefault("autobidding_mode", autobidding_mode)

        if banner_uniq_shows_limit is not None:
            body.setdefault("banner_uniq_shows_limit", banner_uniq_shows_limit)

        if budget_limit is not None:
            body.setdefault("budget_limit", budget_limit)

        if budget_limit_day is not None:
            body.setdefault("budget_limit_day", budget_limit_day)

        if date_end is not None:
            body.setdefault("date_end", date_end)

        if date_start is not None:
            body.setdefault("date_start", date_start)

        if dynamic_banners_use_storelink is not None:
            body.setdefault("dynamic_banners_use_storelink", dynamic_banners_use_storelink)

        if dynamic_without_remarketing is not None:
            body.setdefault("dynamic_without_remarketing", dynamic_without_remarketing)

        if enable_offline_goals is not None:
            body.setdefault("enable_offline_goals", enable_offline_goals)

        if enable_utm is not None:
            body.setdefault("enable_utm", enable_utm)

        if language is not None:
            body.setdefault("language", language)

        if marketplace_app_client_id is not None:
            body.setdefault("marketplace_app_client_id", marketplace_app_client_id)

        if max_price is not None:
            body.setdefault("max_price", max_price)

        if mixing is not None:
            body.setdefault("mixing", mixing)

        if price is not None:
            body.setdefault("price", price)

        if priced_goal_name is not None and priced_goal_source_id is not None:
            body.setdefault("priced_goal", {"name": priced_goal_name, "source_id": priced_goal_source_id})

        if pricelist_id is not None:
            body.setdefault("pricelist_id", pricelist_id)

        if social is not None:
            body.setdefault("social", social)

        if status is not None:
            body.setdefault("status", status)

        if targetings is not None:
            body.setdefault("targetings", targetings)

        if uniq_shows_limit is not None:
            body.setdefault("uniq_shows_limit", uniq_shows_limit)

        if uniq_shows_period is not None:
            body.setdefault("uniq_shows_period", uniq_shows_period)

        if utm is not None:
            body.setdefault("utm", utm)

        return requests.post(url=url, headers=headers, data=json.dumps(body))

    def delete_campaign(self, campaign_id: int):
        """Удаление рекламной кампании"""

        url = f"{self.host}/api/v2/campaigns/{campaign_id}.json"

        headers = {
            # "Content-Type": "application/x-www-form-urlencoded",
            # "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        return requests.delete(url, headers=headers)

    def add_banner(self, campaign_id: int,
                   content_icon_id: int = None,
                   content_overlay_id: int = None,
                   content_video_id: int = None,
                   content_super_video_id: int = None,
                   content_header_image_id: int = None,
                   content_slide_image_id: int = None,
                   content_slides_images_ids: list[int] = None,
                   content_image_id: int = None,
                   content_promo_image_id: int = None,
                   # content_html5: dict = None,
                   content_background_image_id: int = None,
                   content_icon_square_id: int = None,
                   content_image_vertical_id: int = None,
                   content_promo_image_vertical_id: int = None,
                   content_logo_image_id: int = None,
                   content_logo_id: int = None,
                   content_tpl_background_image_id: int = None,
                   content_tpl_background_image_300_id: int = None,
                   content_cover_id: int = None,
                   content_audio_id: int = None,
                   # content_vpaid_button_title: str = None,
                   content_mail_main_id: int = None,
                   content_vk_feed_id: int = None,
                   urls_primary_id: int = None,
                   urls_header_click_id: int = None,
                   urls_slide_clicks_ids: list[int] = None,
                   urls_slide_deeplinks_ids: list[int] = None,
                   urls_ok_id: int = None,
                   urls_vk_id: int = None,
                   urls_links_ids: list[int] = None,
                   urls_link1_id: int = None,
                   urls_deeplink_url_id: int = None,
                   urls_android_store_url_id: int = None,
                   urls_android_tracking_url_id: int = None,
                   urls_android_url_id: int = None,
                   urls_ios_store_url_id: int = None,
                   urls_ios_tracking_url_id: int = None,
                   urls_ios_url_id: int = None,
                   urls_shopitem_url_id: int = None,
                   urls_slide_click_id: int = None,
                   urls_logo_link_id: int = None,
                   textblocks_primary_text: str = None,
                   textblocks_primary_title: str = None,
                   textblocks_header_text: str = None,
                   textblocks_header_title: str = None,
                   textblocks_header_button_text: str = None,
                   textblocks_slides_texts: list[str] = None,
                   textblocks_slides_titles: list[str] = None,
                   textblocks_about_company_text: str = None,
                   textblocks_slide_text: str = None,
                   textblocks_slide_title: str = None,
                   textblocks_slide_button_text: str = None,
                   textblocks_button_title_text: str = None,
                   textblocks_link_title_text: str = None,
                   textblocks_billboard_video_text: str = None,
                   textblocks_position_text: str = None,
                   textblocks_tags_text: str = None,
                   textblocks_selection_text: str = None,
                   products_appearance_name: str = None,
                   products_appearance_price: str = None,
                   products_appearance_button: str = None,
                   products_appearance_button_bg: str = None,
                   products_appearance_borders_inside: str = None,
                   products_appearance_border: str = None,
                   products_appearance_logo_bg: str = None,
                   products_appearance_banner_bg: str = None,
                   products_appearance_title: str = None,
                   products_zoom: bool = None,
                   products_template_type: str = None,
                   call_to_action: str = None,
                   deeplink: str = None,
                   name: str = None,
                   status: str = None,
                   video_params_autoplay: bool = None,
                   video_params_height: int = None,
                   video_params_loop: bool = None,
                   video_params_over_video: bool = None,
                   video_params_sound_delay: bool = None,
                   video_params_video_x: int = None,
                   video_params_video_y: int = None,
                   video_params_width: int = None
                   ):
        """
        Создать объявление внутри кампании
        https://target.my.com/doc/api/ru/resource/CampaignBanners
        https://target.my.com/doc/api/ru/object/Banner
        """

        url = f"{self.host}/api/v2/campaigns/{campaign_id}/banners.json"

        headers = {
            # "Content-Type": "application/x-www-form-urlencoded",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        body = dict()

        content = dict()
        urls = dict()
        textblocks = dict()
        products = dict()

        if content_icon_id is not None:
            content.setdefault("icon", {"id": content_icon_id})
        if content_overlay_id is not None:
            content.setdefault("overlay", {"id": content_overlay_id})
        if content_video_id is not None:
            content.setdefault("video", {"id": content_video_id})
        if content_super_video_id is not None:
            content.setdefault("super_video", {"id": content_super_video_id})
        if content_header_image_id is not None:
            content.setdefault("header_image", {"id": content_header_image_id})
        if content_slide_image_id is not None:
            content.setdefault("slide_image", {"id": content_slide_image_id})

        if content_slides_images_ids is not None:
            for n, image_id in enumerate(content_slides_images_ids, start=1):
                content.setdefault(f"slide_{n}_image", {"id": image_id})

        if content_image_id is not None:
            content.setdefault("image", {"id": content_image_id})
        if content_promo_image_id is not None:
            content.setdefault("promo_image", {"id": content_promo_image_id})
        if content_background_image_id is not None:
            content.setdefault("background_image", {"id": content_background_image_id})
        if content_icon_square_id is not None:
            content.setdefault("icon_square", {"id": content_icon_square_id})
        if content_image_vertical_id is not None:
            content.setdefault("image_vertical", {"id": content_image_vertical_id})
        if content_promo_image_vertical_id is not None:
            content.setdefault("promo_image_vertical", {"id": content_promo_image_vertical_id})
        if content_logo_image_id is not None:
            content.setdefault("logo_image", {"id": content_logo_image_id})
        if content_logo_id is not None:
            content.setdefault("logo", {"id": content_logo_id})
        if content_tpl_background_image_id is not None:
            content.setdefault("tpl_background_image", {"id": content_tpl_background_image_id})
        if content_tpl_background_image_300_id is not None:
            content.setdefault("tpl_background_image_300", {"id": content_tpl_background_image_300_id})
        if content_cover_id is not None:
            content.setdefault("cover", {"id": content_cover_id})
        if content_audio_id is not None:
            content.setdefault("audio", {"id": content_audio_id})
        if content_mail_main_id is not None:
            content.setdefault("mail_main", {"id": content_mail_main_id})
        if content_vk_feed_id is not None:
            content.setdefault("vk_feed", {"id": content_vk_feed_id})

        if len(content) > 0:
            body.setdefault("content", content)

        if urls_primary_id is not None:
            urls.setdefault("primary", {"id": urls_primary_id})
        if urls_header_click_id is not None:
            urls.setdefault("header_click", {"id": urls_header_click_id})

        if urls_slide_clicks_ids is not None:
            for n, click_id in enumerate(urls_slide_clicks_ids, start=1):
                urls.setdefault(f"slide_{n}_click", {"id": click_id})

        if urls_slide_deeplinks_ids is not None:
            for n, deeplink_id in enumerate(urls_slide_deeplinks_ids, start=1):
                urls.setdefault(f"slide_{n}_deeplink", {"id": deeplink_id})

        if urls_ok_id is not None:
            urls.setdefault("ok", {"id": urls_ok_id})
        if urls_vk_id is not None:
            urls.setdefault("vk", {"id": urls_vk_id})

        if urls_links_ids is not None:
            for n, link_id in enumerate(urls_links_ids, start=1):
                urls.setdefault(f"link_{n}", {"id": link_id})

        if urls_link1_id is not None:
            urls.setdefault("link1", {"id": urls_link1_id})
        if urls_deeplink_url_id is not None:
            urls.setdefault("deeplink_url", {"id": urls_deeplink_url_id})
        if urls_android_store_url_id is not None:
            urls.setdefault("android_store_url", {"id": urls_android_store_url_id})
        if urls_android_tracking_url_id is not None:
            urls.setdefault("android_tracking_url", {"id": urls_android_tracking_url_id})
        if urls_android_url_id is not None:
            urls.setdefault("android_url", {"id": urls_android_url_id})
        if urls_ios_store_url_id is not None:
            urls.setdefault("ios_store_url", {"id": urls_ios_store_url_id})
        if urls_ios_tracking_url_id is not None:
            urls.setdefault("ios_tracking_url", {"id": urls_ios_tracking_url_id})
        if urls_ios_url_id is not None:
            urls.setdefault("ios_url", {"id": urls_ios_url_id})
        if urls_shopitem_url_id is not None:
            urls.setdefault("shopitem_url", {"id": urls_shopitem_url_id})
        if urls_slide_click_id is not None:
            urls.setdefault("slide_click", {"id": urls_slide_click_id})
        if urls_logo_link_id is not None:
            urls.setdefault("logo_link", {"id": urls_logo_link_id})

        if len(urls) > 0:
            body.setdefault("urls", urls)

        if textblocks_primary_text is not None:
            textblocks.setdefault("primary", {})
            textblocks["primary"].setdefault("text", textblocks_primary_text)
        if textblocks_primary_title is not None:
            textblocks.setdefault("primary", {})
            textblocks["primary"].setdefault("title", textblocks_primary_title)
        if textblocks_header_text is not None:
            textblocks.setdefault("header", {})
            textblocks["header"].setdefault("text", textblocks_header_text)
        if textblocks_header_title is not None:
            textblocks.setdefault("header", {})
            textblocks["header"].setdefault("title", textblocks_header_title)
        if textblocks_header_button_text is not None:
            textblocks.setdefault("header_button", {"text": textblocks_header_button_text})

        if textblocks_slides_texts is not None:
            for n, slide_text in enumerate(textblocks_slides_texts, start=1):
                textblocks.setdefault(f"slide_{n}", {})
                textblocks[f"slide_{n}"].setdefault("text", slide_text)

        if textblocks_slides_titles is not None:
            for n, slide_title in enumerate(textblocks_slides_titles, start=1):
                textblocks.setdefault(f"slide_{n}", {})
                textblocks[f"slide_{n}"].setdefault("title", slide_title)

        if textblocks_about_company_text is not None:
            textblocks.setdefault("about_company", {"text": textblocks_about_company_text})
        if textblocks_slide_text is not None:
            textblocks.setdefault("slide", {})
            textblocks["slide"].setdefault("text", textblocks_slide_text)
        if textblocks_slide_title is not None:
            textblocks.setdefault("slide", {})
            textblocks["slide"].setdefault("title", textblocks_slide_title)
        if textblocks_slide_button_text is not None:
            textblocks.setdefault("slide_button", {"text": textblocks_slide_button_text})
        if textblocks_button_title_text is not None:
            textblocks.setdefault("button_title", {"text": textblocks_button_title_text})
        if textblocks_link_title_text is not None:
            textblocks.setdefault("link_title", {"title": textblocks_link_title_text})
        if textblocks_billboard_video_text is not None:
            textblocks.setdefault("billboard_video", {"text": textblocks_billboard_video_text})
        if textblocks_position_text is not None:
            textblocks.setdefault("position", {"text": textblocks_position_text})
        if textblocks_tags_text is not None:
            textblocks.setdefault("tags", {"text": textblocks_tags_text})
        if textblocks_selection_text is not None:
            textblocks.setdefault("selection", {"text": textblocks_selection_text})

        if len(textblocks) > 0:
            body.setdefault("textblocks", textblocks)

        appearance = dict()
        if products_appearance_name is not None:
            appearance.setdefault("name", products_appearance_name)
        if products_appearance_price is not None:
            appearance.setdefault("price", products_appearance_price)
        if products_appearance_button is not None:
            appearance.setdefault("button", products_appearance_button)
        if products_appearance_button_bg is not None:
            appearance.setdefault("button_bg", products_appearance_button_bg)
        if products_appearance_borders_inside is not None:
            appearance.setdefault("borders_inside", products_appearance_borders_inside)
        if products_appearance_border is not None:
            appearance.setdefault("border", products_appearance_border)
        if products_appearance_logo_bg is not None:
            appearance.setdefault("logo_bg", products_appearance_logo_bg)
        if products_appearance_banner_bg is not None:
            appearance.setdefault("banner_bg", products_appearance_banner_bg)
        if products_appearance_title is not None:
            appearance.setdefault("title", products_appearance_title)
        if len(appearance) > 0:
            products.setdefault("appearance", appearance)
            if products_zoom is not None and products_template_type is not None:
                products.setdefault("product_zoom", products_zoom)
                products.setdefault("template_type", products_template_type)

        if len(products) > 0:
            body.setdefault("products", products)

        if call_to_action is not None:
            body.setdefault("call_to_action", call_to_action)

        if deeplink is not None:
            body.setdefault("deeplink", deeplink)

        if name is not None:
            body.setdefault("name", name)

        if status is not None:
            body.setdefault("status", status)

        if (video_params_autoplay is not None
                and video_params_height is not None
                and video_params_loop is not None
                and video_params_over_video is not None
                and video_params_sound_delay is not None
                and video_params_video_x is not None
                and video_params_video_y is not None
                and video_params_width is not None):
            video_params = {"autoplay": video_params_autoplay,
                            "height": video_params_height,
                            "loop": video_params_loop,
                            "over_video": video_params_over_video,
                            "sound_delay": video_params_sound_delay,
                            "video_x": video_params_video_x,
                            "video_y": video_params_video_y,
                            "width": video_params_width
                            }

            body.setdefault("video_params", video_params)

        # print(json.dumps(body, ensure_ascii=False).encode('utf8').decode('utf8'))

        return requests.post(url=url, headers=headers,
                             # data=json.dumps(body),
                             data=json.dumps(body, ensure_ascii=False).encode('utf8')
                             )

    def add_url(self, url: str):
        """
        Создает новый объект URL в системе и отправляет его на проверку
        https://target.my.com/doc/api/ru/resource/CreateUrl
        """

        url_ = f"{self.host}/api/v2/urls.json"

        headers = {
            # "Content-Type": "application/x-www-form-urlencoded",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        body = {
            "url": url
        }

        return requests.post(url=url_, headers=headers, data=json.dumps(body))

    def read_urls(self, urls: list[int]):
        """
        Запрос возвращает данные о рекламируемых ссылках
        https://target.my.com/doc/api/ru/resource/ReadUrls
        """

        urls_list = ",".join([str(url) for url in urls])

        url_ = f"{self.host}/api/v2/urls/{urls_list}.json"

        headers = {
            # "Content-Type": "application/x-www-form-urlencoded",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        print(url_)

        return requests.get(url=url_, headers=headers)

    def add_content(self, content_type: str,
                    file_string,
                    filename: str = None,
                    width: int = None,
                    height: int = None
                    ):
        """
        Ресурс, позволяющий загружать креативы, которые в дальнейшем могут быть использованы в рекламных объявлениях.
        https://target.my.com/doc/api/ru/resource/Content
        """

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            # "Accept": "text/plain; charset=utf-8"
            # "Content-Length": "1991",
            "Accept-Encoding": "gzip,deflate,compress",
            # 'Cache-Control': "no-cache"
        }

        body = f"""------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="width"\r\n\r\n{width}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="height"\r\n\r\n{height}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="file"; filename="{filename}"\r\nContent-Type: application/octet-stream\r\n\r\n{file_string}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"""

        if content_type == "static":
            url = f"{self.host}/api/v2/content/static.json"
            # body = {
            #     "data": {"width": width, "height": height},
            #     # "file": f"@[{file_string}]",
            #     "file": file_string.decode('utf8')
            # }
            # body = f"""file=@[{file_string}]data={{"width":{width}, "height":{height}}}"""

        elif content_type == "video":
            url = f"{self.host}/api/v2/content/video.json"

        elif content_type == "html5":
            url = f"{self.host}/api/v2/content/html5.json"

            body = f"""------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="file"; filename="{filename}"\r\nContent-Type: application/octet-stream\r\n\r\n{file_string}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"""

        else:
            return None

        print(url, "\n\n")

        print(body)

        return requests.post(url, headers=headers,
                             # data=json.dumps(body),
                             data=body
                             )

    @staticmethod
    def file_convert(file_path: str):
        """Конвертирует файл в base64"""

        with open(file_path, "rb") as file:
            # encoded_string = base64.b64encode(file.read())

            encoded_string = base64.b64decode(file.read())
            #         return encoded_string.encode('utf8')
        return encoded_string

    @staticmethod
    def file_convert2(file_path: str):
        """Конвертирует файл в байтовую строку"""

        with open(file_path, 'rb') as file:
            data = file.read()

        return data

    @staticmethod
    def file_convert3(file_path: str):
        """Конвертирует файл в байтовую строку"""

        with open(file_path, "rb") as file:
            encoded_string = base64.b64encode(file.read())

        return encoded_string








# BannerPatterns +
# Campaign +
# Content
# CreateUrl +
# ReadUrls, ReadUrl +
# ProjectionPrediction
