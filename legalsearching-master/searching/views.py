from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import json
from elasticsearch import Elasticsearch
import re
import jieba.analyse

def esgetresult(keyword, tags):
    if type(keyword) == type('str'):
        keyword = jieba.analyse.extract_tags(keyword, topK=10)
    mustlist = []
    for item in tags:
        mustlist.append({ "match_phrase": { "content": item }})
    shouldlist = []
    for item in keyword:
        shouldlist.append({ "match_phrase": { "content": item }})
    es = Elasticsearch('localhost:9200')
    doc = {
      "query": {
        "bool": {
          "must":     mustlist,
          "should": shouldlist
        }
      }
    }
    returnlist = []
    try:
        res = es.search(index="legalsearch",body=doc)
        hits = res['hits']['hits']
        for item in hits:
            hitspath =item['_source']['path']
            hitsfull = item['_source']['content']
            try:
                title = re.search('<WS nameCN="文首" value="(.*?)">',hitsfull).group(1)
            except:
                title = "xml格式不正确，无法匹配标题"
            returnlist.append({'title':title,'path':hitspath})
            # print(returnlist)
        return returnlist
    except:
        return([{'title':'无检索内容，请重新输入','path':'无检索内容，请重新输入'}])

def esgetcase(path):
    topK = 100
    content = open(path, encoding='UTF-8').read()
    stopWords = ['nameCN', 'value', '被告人', 'CUS', '被害人', '原判', '上诉人', '第一款', '自首', '量刑', 'oValue', '原审', '检察员', '出庭',
                 '辩护人', '人民检察院', '认定', '意见']
    tags = jieba.analyse.extract_tags(content, topK=topK)
    res = [w for w in tags if w not in stopWords]
    related = esgetresult(res,[])
    resrelated = []
    for item in related:
        if item['path'] != path:
            resrelated.append(item)
    return content,resrelated

#返回所有可能的标签
def gettagcandidates():
    return ["北京", "陕西", "河北", "刑事案件", "寻衅滋事罪", "恶势力", "交通肇事罪","故意杀人罪", "纠纷"]

#根据查询词和标签过滤数组返回结果
#keyword是一个string，查询词
#tags是一个string array，包含所有标签
#返回一个dict array，每个dict里包含title和path
def getresult(keyword, tags):
    return esgetresult(keyword, tags)
    return [{'title': '广东省广州市荔湾区人民检察院 起诉书 穗荔检诉刑诉（2017）1623号',
                'path': '0000b222-5503-486d-9edd-33992135b47b'},
            {'title': '广东省广州市荔湾区人民检察院 起诉书 穗荔检诉刑诉（2017）1623号',
                'path': '0000b222-5503-486d-9edd-33992135b47b'}]
#根据getresult里返回的path，得到对应path的案件的内容以及相关按键
#返回一个tuple，第一个返回值为案件内容，第二个返回值为关联案件，关联案件的格式同getresult
def getcase(path):
    return esgetcase(path)
    return \
            '''
            <writ><QW nameCN="全文" oValue="广东省广州市荔湾区人民检察院 起诉书 穗荔检诉刑诉（2017）1623号 被告人崔某某，男，1974年＊＊月＊＊日出生，居民身份证号码5222281974＊＊＊＊＊＊＊＊，汉族，文化程度初中，住广东省广州市＊＊（户籍所在地贵州省铜仁地区沿河土家族自治县＊＊街道＊＊组），2017年10月20日因涉嫌盗窃被广州市公安局荔湾区公安分局刑事拘留，2017年11月1日经本院批准逮捕，同日被广州市公安局荔湾区公安分局逮捕。 本案由广东省广州市公安局荔湾区分局侦查终结，以被告人崔某某涉嫌盗窃罪，于2017年11月30日向本院移送审查起诉。本院受理后，已告知被告人有权委托辩护人，依法讯问了被告人，审查了全部案件材料。 经依法审查查明： 1.2017年10月11日凌晨4时许，被告人崔某某到广州市越秀区卖麻街66号604房，趁被害人梁某某睡觉时打开房门入屋，盗走被害人梁某某及家人的三个手袋（内共有人民币2700元、联想笔记本电脑一台及证件、信用卡等物）、华为手机一台。得手后被告人崔某某将人民币2700元拿走、将笔记本电脑、华为手机、证件及信用卡等物扔在5至6楼的楼梯处，后被被害人找回。 2．被告人崔某某于2017年10月20日凌晨4时许，到广州市荔湾区涌边街48号4楼，趁被害人张某某睡觉时，打开该房门入屋，从被害人张某某挂在房门边的长裤口袋内盗得人民币1455元。后逃离现场时被巡逻的辅警人员抓获。 认定上述事实的证据如下： 1．缴获的赃款等物证； 2．视频截图、扣押清单、抓获经过等书证； 3．被害人张某某、梁某某的陈述； 4．证人罗某某等2人的证言； 5．被告人崔某某的供述与辩解； 6．现场勘验检查工作记录； 8．视听资料等。 本院认为，被告人崔某某无视国家法律，盗窃公民财物，数额较大，其行为触犯了《中华人民共和国刑法》第二百六十四条之规定，犯罪事实清楚，证据确实、充分，应当以盗窃罪追究其刑事责任。被告人崔某某如实供述自己的罪行，根据《中华人民共和国刑法》第六十七条第三款的规定，可以从轻处罚。根据《中华人民共和国刑事诉讼法》第一百七十二条的规定，提起公诉，请依法判处。 此致 广东省广州市荔湾区人民法院 检察员：姚伟明 2017年12月16日 附： 1．被告人崔某某现羁押于广州市荔湾区看守所。 2．案卷材料和证据2册、光盘2只。 3．依法扣押的赃款已由广州市公安局荔湾区分局发还给被害人。 " value="广东省广州市荔湾区人民检察院 起诉书 穗荔检诉刑诉（2017）1623号 被告人崔某某，男，1974年＊＊月＊＊日出生，居民身份证号码5222281974＊＊＊＊＊＊＊＊，汉族，文化程度初中，住广东省广州市＊＊（户籍所在地贵州省铜仁地区沿河土家族自治县＊＊街道＊＊组），2017年10月20日因涉嫌盗窃被广州市公安局荔湾区公安分局刑事拘留，2017年11月1日经本院批准逮捕，同日被广州市公安局荔湾区公安分局逮捕。 本案由广东省广州市公安局荔湾区分局侦查终结，以被告人崔某某涉嫌盗窃罪，于2017年11月30日向本院移送审查起诉。本院受理后，已告知被告人有权委托辩护人，依法讯问了被告人，审查了全部案件材料。 经依法审查查明： 1.2017年10月11日凌晨4时许，被告人崔某某到广州市越秀区卖麻街66号604房，趁被害人梁某某睡觉时打开房门入屋，盗走被害人梁某某及家人的三个手袋（内共有人民币2700元、联想笔记本电脑一台及证件、信用卡等物）、华为手机一台。得手后被告人崔某某将人民币2700元拿走、将笔记本电脑、华为手机、证件及信用卡等物扔在5至6楼的楼梯处，后被被害人找回。 2．被告人崔某某于2017年10月20日凌晨4时许，到广州市荔湾区涌边街48号4楼，趁被害人张某某睡觉时，打开该房门入屋，从被害人张某某挂在房门边的长裤口袋内盗得人民币1455元。后逃离现场时被巡逻的辅警人员抓获。 认定上述事实的证据如下： 1．缴获的赃款等物证； 2．视频截图、扣押清单、抓获经过等书证； 3．被害人张某某、梁某某的陈述； 4．证人罗某某等2人的证言； 5．被告人崔某某的供述与辩解； 6．现场勘验检查工作记录； 8．视听资料等。 本院认为，被告人崔某某无视国家法律，盗窃公民财物，数额较大，其行为触犯了《中华人民共和国刑法》第二百六十四条之规定，犯罪事实清楚，证据确实、充分，应当以盗窃罪追究其刑事责任。被告人崔某某如实供述自己的罪行，根据《中华人民共和国刑法》第六十七条第三款的规定，可以从轻处罚。根据《中华人民共和国刑事诉讼法》第一百七十二条的规定，提起公诉，请依法判处。 此致 广东省广州市荔湾区人民法院 检察员：姚伟明 2017年12月16日 附： 1．被告人崔某某现羁押于广州市荔湾区看守所。 2．案卷材料和证据2册、光盘2只。 3．依法扣押的赃款已由广州市公安局荔湾区分局发还给被害人。 "><WS nameCN="文首" value="广东省广州市荔湾区人民检察院 起诉书 穗荔检诉刑诉（2017）1623号 "><WSZZDW nameCN="文书制作单位" value="检察院"/><WSZL nameCN="文书种类" value="起诉书"/><WSMC nameCN="文书名称" value="起诉书"/><AJLB nameCN="案件类别" value="刑事案件"/><AH nameCN="案号" value="穗荔检诉刑诉（2017）1623号"/><CBJG nameCN="承办机关" value="广州市荔湾区人民检察院"/><XZQH_CODE nameCN="行政区划代码" value="440103"/><XZQH_P nameCN="行政区划_省" value="广东"/><XZQH_C nameCN="行政区划_市" value="广州市"/><XZQH_CC nameCN="行政区划_区县" value="荔湾区"/><CBJG_LEVEL nameCN="行政机关_级别" value="4"/></WS><DSRD nameCN="当事人段" value="被告人崔某某，男，1974年＊＊月＊＊日出生，居民身份证号码5222281974＊＊＊＊＊＊＊＊，汉族，文化程度初中，住广东省广州市＊＊（户籍所在地贵州省铜仁地区沿河土家族自治县＊＊街道＊＊组），2017年10月20日因涉嫌盗窃被广州市公安局荔湾区公安分局刑事拘留，2017年11月1日经本院批准逮捕，同日被广州市公安局荔湾区公安分局逮捕。"><CUS_BGRXX nameCN="被告人信息" value="被告人崔某某，男，1974年＊＊月＊＊日出生，居民身份证号码5222281974＊＊＊＊＊＊＊＊，汉族，文化程度初中，住广东省广州市＊＊（户籍所在地贵州省铜仁地区沿河土家族自治县＊＊街道＊＊组），2017年10月20日因涉嫌盗窃被广州市公安局荔湾区公安分局刑事拘留，2017年11月1日经本院批准逮捕，同日被广州市公安局荔湾区公安分局逮捕。"><XM nameCN="姓名" value="崔某某"/><XB nameCN="性别" value="男"/><GJ nameCN="国籍" value="中国"/><SFZJ nameCN="身份证件"><ZL nameCN="种类" value="身份证"/><HM nameCN="号码" value="5222281974＊＊＊＊＊＊＊＊"/></SFZJ><CSRQ nameCN="出生日期" value="1974年＊＊月＊＊日"/><MZ nameCN="民族" value="汉族"/><WHCD nameCN="文化程度" value="初中"/><ZZMM nameCN="政治面貌" value="群众"/><HJSZD nameCN="户籍所在地" value="贵州省铜仁地区沿河土家族自治县＊＊街道＊＊组"><HJXZQH nameCN="户籍行政区划" value="贵州"/></HJSZD><ZZ nameCN="住址" value="广东省广州市＊＊"/><QZCSXX nameCN="强制措施信息" value="2017年10月20日因涉嫌盗窃被广州市公安局荔湾区公安分局刑事拘留，2017年11月1日经本院批准逮捕，同日被广州市公安局荔湾区公安分局逮捕。"><JYRQ nameCN="羁押日期" value="2017年10月20日"/><R_QZCS nameCN="强制措施记录"><QZCSZL nameCN="强制措施种类" value="拘留"/><QZCSZXSJ nameCN="强制措施执行时间" value="2017年10月20日"/><QZCSZXDW nameCN="强制措施执行单位" value="广州市公安局荔湾区公安分局"/><QZCSYYFZ nameCN="强制措施原因组"><QZCSYY nameCN="强制措施原因" value="盗窃"/></QZCSYYFZ></R_QZCS><R_QZCS nameCN="强制措施记录"><QZCSZL nameCN="强制措施种类" value="逮捕"/><QZCSPZSJ nameCN="强制措施批准时间" value="2017年11月1日"/><QZCSPZDW nameCN="强制措施批准单位" value="广州市荔湾区人民检察院"/></R_QZCS><R_QZCS nameCN="强制措施记录"><QZCSZL nameCN="强制措施种类" value="逮捕"/><QZCSZXSJ nameCN="强制措施执行时间" value="2017年11月1日"/><QZCSZXDW nameCN="强制措施执行单位" value="广州市公安局荔湾区公安分局"/></R_QZCS></QZCSXX><DSRLX nameCN="当事人类型" value="自然人"/></CUS_BGRXX></DSRD><AJJBQKD nameCN="案件基本情况段" value="本案由广东省广州市公安局荔湾区分局侦查终结，以被告人崔某某涉嫌盗窃罪，于2017年11月30日向本院移送审查起诉。本院受理后，已告知被告人有权委托辩护人，依法讯问了被告人，审查了全部案件材料。"><QSAY nameCN="起诉案由" value="盗窃罪"/><ZCJG nameCN="侦查机关" value="广东省广州市公安局荔湾区分局"/><YSSCQS nameCN="移送审查起诉" value="2017年11月30日"/><CUS_YCCS nameCN="延长次数" value="0"/><CUS_TBCS nameCN="退补次数" value="0"/><CUS_YSSCQSSJ nameCN="移送审查起诉时间" value="2017年11月30日"/></AJJBQKD><AJSSD nameCN="案件事实段" value="经依法审查查明： 1.2017年10月11日凌晨4时许，被告人崔某某到广州市越秀区卖麻街66号604房，趁被害人梁某某睡觉时打开房门入屋，盗走被害人梁某某及家人的三个手袋（内共有人民币2700元、联想笔记本电脑一台及证件、信用卡等物）、华为手机一台。得手后被告人崔某某将人民币2700元拿走、将笔记本电脑、华为手机、证件及信用卡等物扔在5至6楼的楼梯处，后被被害人找回。 2．被告人崔某某于2017年10月20日凌晨4时许，到广州市荔湾区涌边街48号4楼，趁被害人张某某睡觉时，打开该房门入屋，从被害人张某某挂在房门边的长裤口袋内盗得人民币1455元。后逃离现场时被巡逻的辅警人员抓获。 认定上述事实的证据如下： 1．缴获的赃款等物证； 2．视频截图、扣押清单、抓获经过等书证； 3．被害人张某某、梁某某的陈述； 4．证人罗某某等2人的证言； 5．被告人崔某某的供述与辩解； 6．现场勘验检查工作记录； 8．视听资料等。 "><FZSS nameCN="犯罪事实" value="经依法审查查明： 1.2017年10月11日凌晨4时许，被告人崔某某到广州市越秀区卖麻街66号604房，趁被害人梁某某睡觉时打开房门入屋，盗走被害人梁某某及家人的三个手袋（内共有人民币2700元、联想笔记本电脑一台及证件、信用卡等物）、华为手机一台。得手后被告人崔某某将人民币2700元拿走、将笔记本电脑、华为手机、证件及信用卡等物扔在5至6楼的楼梯处，后被被害人找回。 2．被告人崔某某于2017年10月20日凌晨4时许，到广州市荔湾区涌边街48号4楼，趁被害人张某某睡觉时，打开该房门入屋，从被害人张某某挂在房门边的长裤口袋内盗得人民币1455元。后逃离现场时被巡逻的辅警人员抓获。 "/><ZJLB nameCN="证据列表"><ZJ nameCN="证据" value="缴获的赃款等物证"/><ZJ nameCN="证据" value="视频截图、扣押清单、抓获经过等书证"/><ZJ nameCN="证据" value="被害人张某某、梁某某的陈述"/><ZJ nameCN="证据" value="证人罗某某等"/><ZJ nameCN="证据" value="人的证言"/><ZJ nameCN="证据" value="被告人崔某某的供述与辩解"/><ZJ nameCN="证据" value="现场勘验检查工作记录"/><ZJ nameCN="证据" value="视听资料等"/></ZJLB></AJSSD><QSFXD nameCN="起诉分析段" value="本院认为，被告人崔某某无视国家法律，盗窃公民财物，数额较大，其行为触犯了《中华人民共和国刑法》第二百六十四条之规定，犯罪事实清楚，证据确实、充分，应当以盗窃罪追究其刑事责任。被告人崔某某如实供述自己的罪行，根据《中华人民共和国刑法》第六十七条第三款的规定，可以从轻处罚。根据《中华人民共和国刑事诉讼法》第一百七十二条的规定，提起公诉，请依法判处。 "><QSJL nameCN="起诉记录" value="本院认为，被告人崔某某无视国家法律，盗窃公民财物，数额较大，其行为触犯了《中华人民共和国刑法》第二百六十四条之规定，犯罪事实清楚，证据确实、充分，应当以盗窃罪追究其刑事责任"><BQRXM nameCN="被告人姓名" value="崔某某"/><BGRZM_FW nameCN="被告人罪名_范围"><ZM nameCN="罪名"><ZMDM nameCN="罪名代码" value="201"/><WZZM nameCN="完整罪名" value="盗窃罪"/><FJM nameCN="分级码" value="001005002"/></ZM></BGRZM_FW><WFFLTW nameCN="违反法律条文"><FLMC nameCN="法律名称" value="《中华人民共和国刑法》"/><T nameCN="条" value="第二百六十四条"/></WFFLTW><LXFLYJ nameCN="量刑法律依据"><FLMC nameCN="法律名称" value="《中华人民共和国刑法》"/><T nameCN="条" value="第六十七条"><K nameCN="款" value="第三款"/></T></LXFLYJ><LXFLYJ nameCN="量刑法律依据"><FLMC nameCN="法律名称" value="《中华人民共和国刑事诉讼法》"/><T nameCN="条" value="第一百七十二条"/></LXFLYJ><AJDX nameCN="案件定性" value="无视国家法律，盗窃公民财物，数额较大"/></QSJL><SSFLYJ nameCN="诉讼法律依据" value="根据《中华人民共和国刑事诉讼法》第一百七十二条的规定，提起公诉"><FLMC nameCN="法律名称" value="中华人民共和国刑事诉讼法"/><T nameCN="条" value="第一百七十二条"/><QSJL nameCN="结论" value="提起公诉"/></SSFLYJ><FLFTYY nameCN="法律法条引用"><FLFTFZ nameCN="法律法条分组"><MC nameCN="名称" value="《中华人民共和国刑法》"/><T nameCN="条" value="第二百六十四条"/></FLFTFZ></FLFTYY><FLFTYY nameCN="法律法条引用"><FLFTFZ nameCN="法律法条分组"><MC nameCN="名称" value="《中华人民共和国刑法》"/><T nameCN="条" value="第六十七条"><K nameCN="款" value="第三款"/></T></FLFTFZ></FLFTYY><FLFTYY nameCN="法律法条引用"><FLFTFZ nameCN="法律法条分组"><MC nameCN="名称" value="《中华人民共和国刑事诉讼法》"/><T nameCN="条" value="第一百七十二条"/></FLFTFZ></FLFTYY><CUS_FLFT_FZ_RY nameCN="法律法条分组冗余"><CUS_FLFT_RY nameCN="法律法条" value="《中华人民共和国刑法》第二百六十四条"/><CUS_FLFT_RY nameCN="法律法条" value="《中华人民共和国刑法》第六十七条第三款"/><CUS_FLFT_RY nameCN="法律法条" value="《中华人民共和国刑事诉讼法》第一百七十二条"/></CUS_FLFT_FZ_RY></QSFXD><WW nameCN="文尾" value="此致 广东省广州市荔湾区人民法院 检察员：姚伟明 2017年12月16日 附： 1．被告人崔某某现羁押于广州市荔湾区看守所。 2．案卷材料和证据2册、光盘2只。 3．依法扣押的赃款已由广州市公安局荔湾区分局发还给被害人。 "><FLD nameCN="附录段" value="附： 1．被告人崔某某现羁押于广州市荔湾区看守所。 2．案卷材料和证据2册、光盘2只。 3．依法扣押的赃款已由广州市公安局荔湾区分局发还给被害人。 "><CUS_FLLB nameCN="附录列表" value=" 1．被告人崔某某现羁押于广州市荔湾区看守所。 2．案卷材料和证据2册、光盘2只。 3．依法扣押的赃款已由广州市公安局荔湾区分局发还给被害人。 "><CUS_FL nameCN="附录" value="被告人崔某某现羁押于广州市荔湾区看守所"/><CUS_FL nameCN="附录" value="案卷材料和证据2册、光盘2只"/><CUS_FL nameCN="附录" value="依法扣押的赃款已由广州市公安局荔湾区分局发还给被害人"/></CUS_FLLB></FLD><JCZZ nameCN="检察组织" value="此致 广东省广州市荔湾区人民法院 检察员：姚伟明 2017年12月16日 "><R_JCRY nameCN="检察人员记录"><JS nameCN="角色" value="检察员"/><XM nameCN="姓名" value="姚伟明"/></R_JCRY><QSRQ nameCN="起诉日期" value="2017年12月16日"/><SZFY nameCN="诉至法院" value="广东省广州市荔湾区人民法院"/></JCZZ></WW></QW><CUS_FJD nameCN="附加段" oValue="是" value="是"><AJLB nameCN="案件类别" oValue="刑事案件" value="刑事案件"/><CUS_AY nameCN="案由" oValue="盗窃罪"><ZMDM nameCN="罪名代码" oValue="201" value="201"/><WZZM nameCN="完整罪名" oValue="盗窃罪" value="盗窃罪"/><FJM nameCN="分级码" oValue="001005002" value="001005002"/></CUS_AY></CUS_FJD><CUS_QSS_FZSS nameCN="自定义_起诉书_犯罪事实" oValue="经依法审查查明： 1.2017年10月11日凌晨4时许，被告人崔某某到广州市越秀区卖麻街66号604房，趁被害人梁某某睡觉时打开房门入屋，盗走被害人梁某某及家人的三个手袋（内共有人民币2700元、联想笔记本电脑一台及证件、信用卡等物）、华为手机一台。得手后被告人崔某某将人民币2700元拿走、将笔记本电脑、华为手机、证件及信用卡等物扔在5至6楼的楼梯处，后被被害人找回。 2．被告人崔某某于2017年10月20日凌晨4时许，到广州市荔湾区涌边街48号4楼，趁被害人张某某睡觉时，打开该房门入屋，从被害人张某某挂在房门边的长裤口袋内盗得人民币1455元。后逃离现场时被巡逻的辅警人员抓获。 " value="经依法审查查明： 1.2017年10月11日凌晨4时许，被告人崔某某到广州市越秀区卖麻街66号604房，趁被害人梁某某睡觉时打开房门入屋，盗走被害人梁某某及家人的三个手袋（内共有人民币2700元、联想笔记本电脑一台及证件、信用卡等物）、华为手机一台。得手后被告人崔某某将人民币2700元拿走、将笔记本电脑、华为手机、证件及信用卡等物扔在5至6楼的楼梯处，后被被害人找回。 2．被告人崔某某于2017年10月20日凌晨4时许，到广州市荔湾区涌边街48号4楼，趁被害人张某某睡觉时，打开该房门入屋，从被害人张某某挂在房门边的长裤口袋内盗得人民币1455元。后逃离现场时被巡逻的辅警人员抓获。 "><CUS_FZ_YS_DQZ nameCN="要素分则盗窃罪"><CUS_MMQQ nameCN="秘密窃取" oValue="趁被害人梁某某睡觉" value="趁被害人梁某某睡觉" code="0100140101" s="1.2017年10月11日凌晨4时许，被告人崔某某到广州市越秀区卖麻街66号604房，趁被害人梁某某睡觉时打开房门入屋，盗走被害人梁某某及家人的三个手袋（内共有人民币2700元、联想笔记本电脑一台及证件、信用卡等物）、华为手机一台"/><CUS_MMQQ nameCN="秘密窃取" oValue="趁被害人张某某睡觉" value="趁被害人张某某睡觉" code="0100140101" s="2．被告人崔某某于2017年10月20日凌晨4时许，到广州市荔湾区涌边街48号4楼，趁被害人张某某睡觉时，打开该房门入屋，从被害人张某某挂在房门边的长裤口袋内盗得人民币1455元"/><CUS_YBSHXW nameCN="一般盗窃行为" oValue="1.2017年10月11日凌晨4时许，被告人崔某某到广州市越秀区卖麻街66号604房，趁被害人梁某某睡觉时打开房门入屋，盗走被害人梁某某及家人的三个手袋（内共有人民币2700元、联想笔记本电脑一台及证件、信用卡等物）、华为手机一台" value="1.2017年10月11日凌晨4时许，被告人崔某某到广州市越秀区卖麻街66号604房，趁被害人梁某某睡觉时打开房门入屋，盗走被害人梁某某及家人的三个手袋（内共有人民币2700元、联想笔记本电脑一台及证件、信用卡等物）、华为手机一台" code="0100140102"/><CUS_PQ nameCN="扒窃" oValue="口袋内盗得" value="口袋内盗得" code="0100140106" s="2．被告人崔某某于2017年10月20日凌晨4时许，到广州市荔湾区涌边街48号4楼，趁被害人张某某睡觉时，打开该房门入屋，从被害人张某某挂在房门边的长裤口袋内盗得人民币1455元"/><CUS_YBSHXW nameCN="一般盗窃行为" oValue="1.2017年10月11日凌晨4时许，被告人崔某某到广州市越秀区卖麻街66号604房，趁被害人梁某某睡觉时打开房门入屋，盗走被害人梁某某及家人的三个手袋（内共有人民币2700元、联想笔记本电脑一台及证件、信用卡等物）、华为手机一台" value="1.2017年10月11日凌晨4时许，被告人崔某某到广州市越秀区卖麻街66号604房，趁被害人梁某某睡觉时打开房门入屋，盗走被害人梁某某及家人的三个手袋（内共有人民币2700元、联想笔记本电脑一台及证件、信用卡等物）、华为手机一台" code="0100140102"/><CUS_GSCW nameCN="公私财物" oValue="盗走被害人梁某某及家人的三个手袋（内共有人民币2700元、联想笔记本电脑一台及证件、信用卡等物）、华为手机" value="盗走被害人梁某某及家人的三个手袋（内共有人民币2700元、联想笔记本电脑一台及证件、信用卡等物）、华为手机" code="0100140403" s="1.2017年10月11日凌晨4时许，被告人崔某某到广州市越秀区卖麻街66号604房，趁被害人梁某某睡觉时打开房门入屋，盗走被害人梁某某及家人的三个手袋（内共有人民币2700元、联想笔记本电脑一台及证件、信用卡等物）、华为手机一台"/><CUS_GSCW nameCN="公私财物" oValue="盗得人民币1455元" value="盗得人民币1455元" code="0100140403" s="2．被告人崔某某于2017年10月20日凌晨4时许，到广州市荔湾区涌边街48号4楼，趁被害人张某某睡觉时，打开该房门入屋，从被害人张某某挂在房门边的长裤口袋内盗得人民币1455元"/></CUS_FZ_YS_DQZ></CUS_QSS_FZSS><CUS_QSS_QSFXD nameCN="自定义_起诉书_起诉分析段" oValue="本院认为，被告人崔某某无视国家法律，盗窃公民财物，数额较大，其行为触犯了《中华人民共和国刑法》第二百六十四条之规定，犯罪事实清楚，证据确实、充分，应当以盗窃罪追究其刑事责任。被告人崔某某如实供述自己的罪行，根据《中华人民共和国刑法》第六十七条第三款的规定，可以从轻处罚。根据《中华人民共和国刑事诉讼法》第一百七十二条的规定，提起公诉，请依法判处。 " value="本院认为，被告人崔某某无视国家法律，盗窃公民财物，数额较大，其行为触犯了《中华人民共和国刑法》第二百六十四条之规定，犯罪事实清楚，证据确实、充分，应当以盗窃罪追究其刑事责任。被告人崔某某如实供述自己的罪行，根据《中华人民共和国刑法》第六十七条第三款的规定，可以从轻处罚。根据《中华人民共和国刑事诉讼法》第一百七十二条的规定，提起公诉，请依法判处。 "><CUS_ZZ_YS nameCN="要素总则"><TB nameCN="坦白" oValue="如实供述自己的罪行" value="如实供述自己的罪行" code="0100011507" s="被告人崔某某如实供述自己的罪行，根据《中华人民共和国刑法》第六十七条第三款的规定，可以从轻处罚"/></CUS_ZZ_YS><CUS_FZ_YS_DQZ nameCN="要素分则盗窃罪"><CUS_YBSHXW nameCN="一般盗窃行为" oValue="盗窃" value="盗窃" code="0100140102" s="本院认为，被告人崔某某无视国家法律，盗窃公民财物，数额较大，其行为触犯了《中华人民共和国刑法》第二百六十四条之规定，犯罪事实清楚，证据确实、充分，应当以盗窃罪追究其刑事责任"/><CUS_GSCW nameCN="公私财物" oValue="盗窃公民财物" value="盗窃公民财物" code="0100140403" s="本院认为，被告人崔某某无视国家法律，盗窃公民财物，数额较大，其行为触犯了《中华人民共和国刑法》第二百六十四条之规定，犯罪事实清楚，证据确实、充分，应当以盗窃罪追究其刑事责任"/><CUS_SEJIAOD nameCN="数额较大" oValue="数额较大" value="数额较大" code="0100140601" s="本院认为，被告人崔某某无视国家法律，盗窃公民财物，数额较大，其行为触犯了《中华人民共和国刑法》第二百六十四条之规定，犯罪事实清楚，证据确实、充分，应当以盗窃罪追究其刑事责任"/></CUS_FZ_YS_DQZ></CUS_QSS_QSFXD><CUS_QSS_DSRD nameCN="自定义_起诉书_当事人段" oValue="被告人崔某某，男，1974年＊＊月＊＊日出生，居民身份证号码5222281974＊＊＊＊＊＊＊＊，汉族，文化程度初中，住广东省广州市＊＊（户籍所在地贵州省铜仁地区沿河土家族自治县＊＊街道＊＊组），2017年10月20日因涉嫌盗窃被广州市公安局荔湾区公安分局刑事拘留，2017年11月1日经本院批准逮捕，同日被广州市公安局荔湾区公安分局逮捕。" value="被告人崔某某，男，1974年＊＊月＊＊日出生，居民身份证号码5222281974＊＊＊＊＊＊＊＊，汉族，文化程度初中，住广东省广州市＊＊（户籍所在地贵州省铜仁地区沿河土家族自治县＊＊街道＊＊组），2017年10月20日因涉嫌盗窃被广州市公安局荔湾区公安分局刑事拘留，2017年11月1日经本院批准逮捕，同日被广州市公安局荔湾区公安分局逮捕。"/><BHYJTP nameCN="辩护意见图谱" oValue="辩护意见图谱" value="辩护意见图谱"/></writ>
            ''', \
            [{'title': '广东省广州市荔湾区人民检察院 起诉书 穗荔检诉刑诉（2017）1623号',
                'path': '0000b222-5503-486d-9edd-33992135b47b'},
             {'title': '广东省广州市荔湾区人民检察院 起诉书 穗荔检诉刑诉（2017）1623号',
                'path': '0000b222-5503-486d-9edd-33992135b47b'}]
def home(request):
    i = 0
    tags = []
    while True:
        t = request.GET.get(str(i), None)
        if t is None:
            break
        tags.append(t)
        i += 1
    keyword = request.GET.get("keyword", "")
    res = []
    if keyword != "" or len(tags) > 0:
        res = getresult(keyword, tags)
    tagcandidates = gettagcandidates()
    return render(request, 'searching/home.html',{
        'dtags': json.dumps(tags),
        'dword': keyword,
        'res': res,
        'tagcandidates': tagcandidates
    })
def viewcase(request, str):
    textraw, related = getcase(str)
    try:
        text = re.search(r'<QW nameCN="全文" oValue="(.*?)" value',textraw).group(0)[len('<QW nameCN="全文" oValue="'):-7]
        text = text.replace(' ', '<br>')
    except:
        text = textraw
    return render(request, 'searching/case.html',{
            'text': text,
            'related': related
        })