import logging
import os
import xml.etree.ElementTree as et
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from .models import Hospital


logger_hospinfo = logging.getLogger('logger_hospinfo')


def get_hospinfo(): 
    """
    :return: a dictionary having its key as hospital_id and its values as follows:
            {
                'hospital_name'
                'class_code'
                'class_code_name'
                'phone'
                'url'
                'established_at'
                'sggu_name'
                'emdong_name'
                'post_no'
                'address'
                'sido_name'
                'sggu_no'
                'sido_no'
                'general_doctor_count'
                'intern_count'
                'resident_count'
                'fellow_doctor_count'
            }
    """

    hospinfo = {}

    for pageno in range(1, 9):

        # do a get request to the openapi service.
        try:
            r = requests.get(
                'http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList?' \
                '&numOfRows=10000' \
                '&ServiceKey=%s' \
                '&pageNo=%s'
                %(os.getenv('HOSPITAL_API_KEY'), str(pageno))
                )
        except Exception as e:
            logger_hospinfo.critical('An openapi request error occured: %s at pageno %d' % (e, pageno)) 
            raise Exception('An openapi request error occured: %s at pageno %d' % (e, pageno)) 

        # exclude irrelevant things that will not be used in the app from the get request result.
        try: 
            root = et.fromstring(r.text)
            items = root[1][0]
        except Exception as e:
            logger_hospinfo.critical('A XML parsing error occured: %s at pageno %d' % (e, pageno)) 
            raise Exception('A XML parsing error occured: %s at pageno %d' % (e, pageno)) 

        # create the key-value variable.
        for item in items:
            if not (class_code_name:=item.find('clCd')).text in ['01', '11', '41', '51']: 
                continue

            hospital_id = hospital_id.text if (hospital_id:=item.find('ykiho')) != None else None
            hospital_name = hospital_name.text if (hospital_name:=item.find('yadmNm')) != None else None
            class_code = class_code.text if (class_code:=item.find('clCdNm')) != None else None
            class_code_name = int(class_code_name.text) if (class_code_name:=item.find('clCd')) != None else None
            phone = phone.text if (phone:=item.find('telno')) != None else None
            url = url.text if (url:=item.find('hospUrl')) != None else None
            established_at = datetime.strptime(established_at.text, '%Y%m%d').date() if (established_at:=item.find('estbDd')) != None else None 
            sggu_name = sggu_name.text if (sggu_name:=item.find('sgguCdNm')) != None else None
            emdong_name = emdong_name.text if (emdong_name:=item.find('emdongNm')) != None else None
            post_no = int(post_no.text) if (post_no:=item.find('postNo')) != None else None
            address = address.text if (address:=item.find('addr')) != None else None
            sido_name = sido_name.text if (sido_name:=item.find('sidoCdNm')) != None else None
            sggu_no = int(sggu_no.text) if (sggu_no:=item.find('sgguCd')) != None else None
            sido_no = int(sido_no.text) if (sido_no:=item.find('sidoCd')) != None else None
            general_doctor_count = int(general_doctor_count.text) if (general_doctor_count:=item.find('detyGdrCnt')) != None else None
            intern_count = int(intern_count.text) if (intern_count:=item.find('detyIntnCnt')) != None else None
            resident_count = int(resident_count.text) if (resident_count:=item.find('detyResdntCnt')) != None else None
            fellow_doctor_count = int(fellow_doctor_count.text) if (fellow_doctor_count:=item.find('detySdrCnt')) != None else None

            hospinfo[hospital_id] = {
                'hospital_name': hospital_name,
                'class_code': class_code,
                'class_code_name': class_code_name,
                'phone': phone,
                'url': url,
                'established_at': established_at,
                'sggu_name': sggu_name,
                'emdong_name': emdong_name,
                'post_no': post_no,
                'address': address,
                'sido_name': sido_name,
                'sggu_no': sggu_no,
                'sido_no': sido_no,
                'general_doctor_count': general_doctor_count,
                'intern_count': intern_count,
                'resident_count': resident_count,
                'fellow_doctor_count': fellow_doctor_count
                }

    return hospinfo

def update_hospinfo():
    hospinfo = get_hospinfo()

    # iterate the hospinfo,
    # crate a model instance if an element of the hospinfo is not registered in the database,
    # update the model instance if an element of the hospinfo is registered in the database.

    logger_hospinfo.info('Start process')


    for k, v in hospinfo.items():         
        try:
            im = Hospital.objects.get(hospital_id=k)

            im.hospital_name = new_hospital_name if (new_hospital_name:=v['hospital_name']) != im.hospital_name else im.hospital_name
            im.class_code = new_class_code if (new_class_code:=v['class_code']) != im.class_code else im.class_code
            im.class_code_name = new_class_code_name if (new_class_code_name:=v['class_code_name']) != im.class_code_name else im.class_code_name
            im.phone = new_phone if (new_phone:=v['phone']) != im.phone else im.phone
            im.url = new_url if (new_url:=v['url']) != im.url else im.url
            im.established_at = new_established_at if (new_established_at:=v['established_at']) != im.established_at else im.established_at
            im.sggu_name = new_sggu_name if (new_sggu_name:=v['sggu_name']) != im.sggu_name else im.sggu_name
            im.emdong_name = new_emdong_name if (new_emdong_name:=v['emdong_name']) != im.emdong_name else im.emdong_name
            im.post_no = new_post_no if (new_post_no:=v['post_no']) != im.post_no else im.post_no
            im.address = new_address if (new_address:=v['address']) != im.address else im.address
            im.sido_name = new_sido_name if (new_sido_name:=v['sido_name']) != im.sido_name else im.sido_name
            im.sggu_no = new_sggu_no if (new_sggu_no:=v['sggu_no']) != im.sggu_no else im.sggu_no
            im.sido_no = new_sido_no if (new_sido_no:=v['sido_no']) != im.sido_no else im.sido_no
            im.general_doctor_count = new_general_doctor_count if (new_general_doctor_count:=v['general_doctor_count']) != im.general_doctor_count else im.general_doctor_count
            im.intern_count = new_intern_count if (new_intern_count:=v['intern_count']) != im.intern_count else im.intern_count
            im.resident_count = new_resident_count if (new_resident_count:=v['resident_count']) != im.resident_count else im.resident_count
            im.fellow_doctor_count = new_fellow_doctor_count if (new_fellow_doctor_count:=v['fellow_doctor_count']) != im.fellow_doctor_count else im.fellow_doctor_count

            im.save()

        except Hospital.DoesNotExist:
            im = Hospital(
                hospital_id=k,
                hospital_name=v['hospital_name'],
                class_code=v['class_code'],
                class_code_name=v['class_code_name'],
                phone=v['phone'],
                url=v['url'],
                established_at=v['established_at'],
                sggu_name=v['sggu_name'],
                emdong_name=v['emdong_name'],
                post_no=v['post_no'],
                address=v['address'],
                sido_name=v['sido_name'],
                sggu_no=v['sggu_no'],
                sido_no=v['sido_no'],
                general_doctor_count=v['general_doctor_count'],
                intern_count=v['intern_count'],
                resident_count=v['resident_count'],
                fellow_doctor_count=v['fellow_doctor_count']
                )
            im.save()

    logger_hospinfo.info('update_hospinfo done.')

def start_scheduler():
    bs = BackgroundScheduler()
    bs.add_job(update_hospinfo, 'cron', hour='23', minute='59')
    bs.start()