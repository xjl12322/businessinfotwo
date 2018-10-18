# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from .items import BeianItem,BusinessinfoItem,DomainItem,BaiduqiyeItem
import redis
from utils import Utils
from .utils_common.long import Logger
from .utils_common.md5_use import mad5_url,c_company

class BusinessinfoPipeline(object):
    def process_item(self, item, spider):
        return item


# class redisinsert(object):
#     def __init__(self):
#         self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=1)
#         self.r = redis.Redis(connection_pool=self.pool)
#
#     def process_item(self, item, spider):
#         if spider.name== "domian_spider":
#             aa = item["domain"]
#             print(aa,"33333333333333333333333333")
#             print("响应2")
#             result_num = self.r.lpush("my_url_list", item["domain"])
#             print(result_num,"响应")
#
#     def spider_closed(self, spider):
#         pass
class mysql_yi_pipelines(object):

    '''异步写入'''
    def __init__(self,dbpool):
        self.dbpool = dbpool
        self.utils = Utils()
        # self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=1)
        # self.r = redis.Redis(connection_pool=self.pool)

    #创建一个静态方法,静态方法的加载内存优先级高于init方法
    #在创建这个类的对之前就已将加载到了内存中，所以init这个方法可以调用这个方法产生的对象

    @classmethod
    def from_settings(cls,settings):
        # 先将setting中连接数据库所需内容取出，构造一个地点
        dbparams = dict(
            host=settings['SQLDB'][settings['CONRENT_CONF']]['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['SQLDB'][settings['CONRENT_CONF']]['MYSQL_DBNAME'],
            port=settings['SQLDB'][settings['CONRENT_CONF']]['MYSQL_PORT'],
            user=settings['SQLDB'][settings['CONRENT_CONF']]['MYSQL_USER'],
            passwd=settings['SQLDB'][settings['CONRENT_CONF']]['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            # 游标设置
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )

        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        return cls(dbpool)

    def process_item(self,item,spider):
        # 使用Twisted异步的将Item数据插入数据库
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error,item)


    def do_insert(self,cursor,item):

        if isinstance(item,BeianItem):
            sql = "insert ignore into beian(company_name,company_type,website_recard_num,website_homepage,website_name,check_date) VALUES (%s,%s,%s,%s,%s,%s)"
            num_beianitem = cursor.execute(sql,(item["company_name"],item["company_type"],item["website_recard_num"],str(item["website_homepage"]),item["website_name"],item["check_date"],))
            if num_beianitem==0:
                print("insert database seccess fail,in exist")
                pass
            else:
                print(num_beianitem,"nnnnnnnnnnnnnn")
                cursor.execute('select last_insert_id() as id')
                id = cursor.fetchone()
                # print(id)
                print("insert database seccess: ID is :{}".format(id["id"]))


        if isinstance(item,BusinessinfoItem):
            print("--------------------------")
            print(item["company_introduce"],"1111111111111")
            print(item["tel"],"22222222222")
            print(item["contacts_people"],"33333333333")
            print(item["m_phone"],"44444444444")
            print(item["company_name"],"5555555555")
            print(item["status"],"66666666666")
            print(item["company_type"],"77777777")
            print(item["establish_date"],"888888888888")
            print(item["expire_date"],"9999999999")
            print(item["register_money"],"aaaaaaaaaa")
            print(item["register_authority"],"bbbbbbbbbb")
            print(item["business_scope"],"ccccccccccccc")
            print(item["register_address"],"dddddddddddd")
            print(item["legal_representative"],"eeeeeeeeee")
            print(item["register_num"])
            print(item["company_website"])
            print(item["industry_id"])
            print(item["area_p"],"nnnnnnnnnn")
            print(item["area_s"],"ppppppppp")
            print(item["area_q"],"ooooooo")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            eid = mad5_url(item["company_name"])

            print(eid,"eideideideideideideideid")
            sql2 = "insert ignore into business(eid,company_introduce,tel,contacts_people,m_phone,company_name,status,company_type,establish_date,expire_date,register_money,register_authority,business_scope,register_address,legal_representative,register_num,company_website,industry_id,area_p,area_s,area_q,origin_id,industry) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            num_businessinfoitem = cursor.execute(sql2,(eid,item["company_introduce"],item["tel"], item["contacts_people"], item["m_phone"],item["company_name"],item["status"], item["company_type"], str(item["establish_date"]), item["expire_date"],item["register_money"], item["register_authority"], item["business_scope"], item["register_address"],item["legal_representative"], item["register_num"], item["company_website"],item["industry_id"],item["area_p"],item["area_s"],item["area_q"],item["origin_id"],item["industry"]))
            if num_businessinfoitem:
                cursor.execute('select last_insert_id() as id')
                id = cursor.fetchone()

                print("insert database seccess: ID is :{}".format(id["id"]))
            else:
                print("insert database fail,in exist")
            #
            if item["register_address"]:
                company_c = {
                    "compName": item["company_name"],
                    "compAddress": item["register_address"]
                }
                try:
                    b = c_company(company_c)
                    print("es状态{}".format(b))
                    if (b == "true") or (b == True) or (b == "True"):
                        print("插入es成功")
                    else:
                        print("插入es失败")
                except Exception as e:
                    print("异常信息".format(e))
                    print("插入es异常")

        if isinstance(item,DomainItem):

            domain = item["domain"][0]
            if domain in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if item["domain"].startswith(domain):
                    sql3 = "insert ignore into "+"`"+domain+"`"+" VALUES (0,%s)"
                    num_domainitem = cursor.execute(sql3,(item["domain"],))
                    if num_domainitem:
                        print("insert database  domain seccess")
                    else:
                        print("insert database domain fail,in exist")
            else:
                sql3 = "insert ignore into qt VALUES (0,%s)"
                num_domainitem = cursor.execute(sql3, (item["domain"],))
                if num_domainitem:
                    print("insert database  domain seccess")
                else:
                    print("insert database domain fail,in exist")

            # print(item["domain"],"写入redis")
            # result_num = self.r.lpush("my_url_list", item["domain"])
            # print(result_num,"响应")

        if isinstance(item, BaiduqiyeItem):
            if item["company_name"]:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                eid = mad5_url(item["company_name"])
                sql = "insert ignore into business(eid,company_introduce,tel,contacts_people,m_phone,company_name,status,company_type,establish_date,expire_date,register_money,register_authority,business_scope,register_address,legal_representative,register_num,company_website,industry_id,area_p,area_s,area_q,industry) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                num_businessinfoitem = cursor.execute(sql, (
                eid, item["company_introduce"], item["tel"], item["contacts_people"], item["m_phone"],
                item["company_name"], item["status"], item["company_type"], str(item["establish_date"]),
                item["expire_date"], item["register_money"], item["register_authority"], item["business_scope"],
                item["register_address"], item["legal_representative"], item["register_num"],
                item["company_website"], item["industry_id"], item["area_p"], item["area_s"], item["area_q"],
                item["industry"]))

                if num_businessinfoitem:



                    cursor.execute('select last_insert_id() as id')
                    id = cursor.fetchone()
                    # return num_businessinfoitem
                    Logger.info("插入数据库成功：{}".format(id))
                    if item["register_address"]:
                        company_c = {
                            "compName": item["company_name"],
                            "compAddress": item["register_address"]
                        }
                        try:
                            b = c_company(company_c)
                            Logger.info("es状态{}".format(b))
                            if (b == "true") or (b == True) or (b == "True"):
                                Logger.info("插入es成功")
                            else:
                                Logger.info("插入es失败")
                        except Exception as e:
                            Logger.info("异常信息".format(e))
                            Logger.info("插入es异常")

                else:

                    sql2 = 'select * from business where company_name=%s'
                    sql3 = 'UPDATE business SET status = %s, company_type = %s,establish_date = %s,expire_date = %s,register_money = %s,register_authority = %s,business_scope = %s,register_address = %s,legal_representative = %s,register_num = %s,company_website = %s,industry = %s WHERE company_name=%s'

                    cursor.execute(sql2, (item["company_name"],))
                    alls = cursor.fetchone()
                    if alls.get("register_num", "") == "":
                        try:
                            cursor.execute(sql3, (
                                item["status"], item["company_type"], item["establish_date"],
                                item["expire_date"],
                                item["register_money"], item["register_authority"], item["business_scope"],
                                item["register_address"], item["legal_representative"], item["register_num"],
                                item["company_website"], item["industry"], item["company_name"]))
                            # return num_businessinfoitem

                            Logger.info("更新成功:id-{}".format(alls.get("id")))

                            if item["register_address"]:
                                company_c = {
                                    "compName": item["company_name"],
                                    "compAddress": item["register_address"]
                                }
                                try:
                                    b = c_company(company_c)
                                    Logger.info("es状态{}".format(b))
                                    if (b == "true") or (b == True) or (b == "True"):
                                        Logger.info("插入es成功")
                                    else:
                                        Logger.info("插入es失败")
                                except Exception as e:
                                    Logger.info("异常信息".format(e))
                                    Logger.info("插入es异常")
                        except Exception as e:

                            Logger.info("更新异常:{}".format(e))

                            # self.loging.info("insert database fail,in exist")
                    else:
                        Logger.info("数据完整无需更新")









    def handle_error(self,failure,item):
        # 打印异步插入异常

        print(failure,"mysql异常")
