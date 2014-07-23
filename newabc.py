#!/usr/bin/env python3
# encoding: utf-8

#Contact: David Duan <david.3.duan@microsoft.com>

import getopt
import logging
import os
import re
import shutil
import sys
from xml.etree import ElementTree as etree

#logfile settings
logging.basicConfig(
    filename='newabc.log',
    filemode='w',
    format='%(asctime)s  :  %(message)s',
    level=logging.INFO
)

#global variables

TOOL_PATH = os.path.abspath('.')
OUTPUT = os.path.join(TOOL_PATH, "..", "..")
TEMPLATE_PATH = os.path.join(TOOL_PATH, "template")
STORAGE_PATH = os.path.join(TOOL_PATH, "..", "..", "storage")
COUNTRY_MCC_FILE = os.path.join(TOOL_PATH, "cfg", "country_mcc.txt")
SETTINGS_PATH = os.path.join(TOOL_PATH, "cfg", "Settings")
VARIANT_APPLICATIONS_APPNAME = []
VARIANT_APPLICATIONS_APPNAME_BGCOLOR = {}

logging.info("TOOL_PATH: %s", TOOL_PATH)
logging.info("TEMPLATE_PATH: %s", TEMPLATE_PATH)

def multi_replace(text, adict):
    rx = re.compile('|'.join(map(re.escape, adict)))
    def xlat(match):
        return adict[match.group(0)]
    return rx.sub(xlat, text)

def update_template_content(file_path, pairs):
    """
    Update file content, replace the placeholder in the tempalte file.
    Args:
        file_path:
        pairs:
    Return:
        None
    """
    text = open(file_path).read()
    newtext = multi_replace(text, pairs)
    if newtext != text:
        open(file_path, 'w').write(newtext)

def check_media_data(product_name, media_type, media_item):
    """
    Check if the media resources file exist under storage folder

    Args:
        product_name:
        media_type:
        media_item:
    Return:
        is_availability: True(exist), False(not exist)
    """

    is_availability = False

    common_videos_storage_path = os.path.join(STORAGE_PATH, "common", "videos")
    common_audio_storage_path = os.path.join(STORAGE_PATH, "common", "audio")
    common_images_storage_path = os.path.join(STORAGE_PATH, "common", "images")
    product_videos_storage_path = os.path.join(STORAGE_PATH, product_name, "videos")
    product_audio_storage_path = os.path.join(STORAGE_PATH, product_name, "audio")
    product_images_storage_path = os.path.join(STORAGE_PATH, product_name, "images")

    videos_file_list = os.listdir(common_videos_storage_path)
    if os.path.isdir(product_videos_storage_path):
        videos_file_list = os.listdir(product_videos_storage_path) + videos_file_list

    audio_file_list = os.listdir(common_audio_storage_path)
    if os.path.isdir(product_audio_storage_path):
        audio_file_list = os.listdir(product_audio_storage_path) + audio_file_list

    images_file_list = os.listdir(common_images_storage_path)
    if os.path.isdir(product_images_storage_path):
        images_file_list = os.listdir(product_images_storage_path) + images_file_list

    if media_type == "AlertTones":
        if media_item in audio_file_list:
            is_availability = True
        else:
            print("Warning: No " + media_type + " file named \"" + media_item + "\"")
            logging.info("Warning: No " + media_type + " file named \"" + media_item + "\"")
            is_availability = False
    elif media_type == "MiscTones":
        if media_item in audio_file_list:
            is_availability = True
        else:
            print("Warning: No " + media_type + " file named \"" + media_item + "\"")
            logging.info("Warning: No " + media_type + " file named \"" + media_item + "\"")
            is_availability = False
    elif media_type == "RingingTones":
        if media_item in audio_file_list:
            is_availability = True
        else:
            print("Warning: No " + media_type + " file named \"" + media_item + "\"")
            logging.info("Warning: No " + media_type + " file named \"" + media_item + "\"")
            is_availability = False
    elif media_type == "Music":
        if media_item in audio_file_list:
            is_availability = True
        else:
            print("Warning: No " + media_type + " file named \"" + media_item + "\"")
            logging.info("Warning: No " + media_type + " file named \"" + media_item + "\"")
            is_availability = False
    elif media_type == "ParallaxBackground":
        if media_item in images_file_list:
            is_availability = True
        else:
            print("Warning: No " + media_type + " file named \"" + media_item + "\"")
            logging.info("Warning: No " + media_type + " file named \"" + media_item + "\"")
            is_availability = False
    elif media_type == "LockscreenWallpaper":
        if media_item in images_file_list:
            is_availability = True
        else:
            print("Warning: No " + media_type + " file named \"" + media_item + "\"")
            logging.info("Warning: No " + media_type + " file named \"" + media_item + "\"")
            is_availability = False
    elif media_type == "Animations":
        if media_item in images_file_list:
            is_availability = True
        else:
            print("Warning: No " + media_type + " file named \"" + media_item + "\"")
            logging.info("Warning: No " + media_type + " file named \"" + media_item + "\"")
            is_availability = False
    elif media_type == "Videos":
        if media_item in videos_file_list:
            is_availability = True
        else:
            print("Warning: No " + media_type + " file named \"" + media_item + "\"")
            logging.info("Warning: No " + media_type + " file named \"" + media_item + "\"")
            is_availability = False
    else:
        print("no such kind of media type: %s in the storage folder" % media_type)

    return is_availability


def find_codelist_and_content_configure_data_files(type_designator):
    """
    find correct codelist and content_configure_date files in the abc_regionphone folder.

    Args:
        type_designator : rm1057 (example).

    Returns:
        product_name             : athena (example)
        product_nick_name        : athena_ds (example)
        codelist                 : rm1057_athena_ds_codelist.txt (example)
        content_configure_data   : rm1057_athena_ds_content_configure_data.txt (example)
    """
    is_find = False

    for (thisdir, subdirs, fileshere) in os.walk(TOOL_PATH):
        for filename in fileshere:
            if filename.startswith(type_designator):
                is_find = True
                if filename.endswith("_codelist.txt"):
                    codelist = os.path.join(thisdir, filename)
                    product_name = filename.split("_")[1]
                    product_nick_name = filename.replace(type_designator + '_','').replace("_codelist.txt",'')

    if not is_find:
        print("Error: no such type designator config files!!!")
        sys.exit()

    content_configure_data = codelist.replace("codelist",'content_configure_data')

    logging.info("[find_codelist_and_content_configure_data_files] product_name = %s " % product_name )
    logging.info("[find_codelist_and_content_configure_data_files] product_nick_name = %s " % product_nick_name )
    logging.info("[find_codelist_and_content_configure_data_files] codelist = %s " % codelist )
    logging.info("[find_codelist_and_content_configure_data_files] content_configure_data = %s " % content_configure_data )

    return product_name, product_nick_name, codelist, content_configure_data

def sub_variant_mcc_collect(sub_region, variant_subregion_to_ctrcode):
    """
    Collect each sub region covered mcc codes into list

    Args:
        sub_region:  EURO_CY_ES_FR_GR_IT,EURO_COMMON (example)
        variant_subregion_to_ctrcode : { EURO_CY_ES_FR_GR_IT:2301, EURO_COMMON:2300} (example)

    Return:
        sub_variant_mcc_collect_text : mcc codes list text
    """

    sub_variant_mcc_collect_text = ""
    mcc_pair_data = """\
              <MNCMCCPair>
                  <Name>%s</Name>
                  <Mcc>%s</Mcc>
                  <Mnc />
                  <SPN />
              </MNCMCCPair>
    """


    name = variant_subregion_to_ctrcode[sub_region]
    clongname_cshortname, clongname_mcc, cshortname_mcc, mcc_cshortname = get_country_mcc_info()

    sub_variant_mcc_collect_text += "        <Multivariant>\n"

    sub_region_list = sub_region.split("_")[1:] # remove the EURO, MEA etc..

    if "COMMON" in sub_region:
        sub_region = " ".join(sub_region.split("_")) # APAC COMMON, EURO COMMON...
        common_mcc_code_list = clongname_mcc[sub_region].split(",")
        for each_mcc_code in common_mcc_code_list:
            sub_variant_mcc_collect_text += mcc_pair_data % (name, each_mcc_code)
    else:
        for each_sub_region in sub_region_list:
            sub_variant_mcc_collect_text += mcc_pair_data % (name, cshortname_mcc[each_sub_region])

    sub_variant_mcc_collect_text += "        </Multivariant>\n"

    return sub_variant_mcc_collect_text

def variant_config_sets_collect(ctr_code, codelist, variant_ctrcode_to_subregions, variant_subregion_to_ctrcode):
    """
    Collect config-data-file list in the {ProductName}_{CTR}.xml,
    and list all sub region name/mcc codes under each config-data-file

    Args:
        ctr_code: 059xxxx
        codelist: rm1057_athena_ds_codelist.txt (example)
        variant_ctrcode_to_subregions:{'059W2Z0': ['INDIA_IN'], '059W0Q7': ['EURO_COMMON', 'EURO_CY_ES_FR_GR_IT', 'EURO_IL_NL', 'EURO_GB_IE'], ...} (example)
        variant_subregion_to_ctrcode: {'EURO_COMMON': '2300', 'APAC_SG': '2318', 'EURO_IL_NL': '2302', ...} (example)
    Return:
        variant_config_sets_content_text:
    """
    variant_config_sets_content_text = ""

    count = 0
    for each_sub_region in variant_ctrcode_to_subregions[ctr_code]:
        if 0 == count:
            variant_config_sets_content_text += '        <config-set name="'+ each_sub_region +'" config-data-file="' + each_sub_region + '-config-data.xml" default="True">\n'
            variant_config_sets_content_text += '        </config-set>\n'
            variant_config_sets_content_text += sub_variant_mcc_collect(each_sub_region, variant_subregion_to_ctrcode)
            count+=1
        else :
            variant_config_sets_content_text += '        <config-set name="'+ each_sub_region +'" config-data-file="' + each_sub_region + '-config-data.xml">\n'
            variant_config_sets_content_text += '        </config-set>\n'
            variant_config_sets_content_text += sub_variant_mcc_collect(each_sub_region, variant_subregion_to_ctrcode)

    return variant_config_sets_content_text

def variant_settings_collect(type_designator, product_name, product_nick_name, sv_sub_region):
    """
    collect all setting files content cascadingly according to this order:

    Settings_PRODUCT
    Settings_PRODUCT_{product}
    Settings_DS/SS
    Settings_DS/SS_{product}
    Setting_MV_{region}
    Setting_MV_{region}_{product}
    Setting_SV_{sub_region}
    Setting_SV_{sub_region}_{product}

    Args:
        type_designator : rm1057 (example).
        product_name :
        product_nick_name :
        sv_sub_region :

    Returns:
        variantsettings_content_text :

    """
    variantsettings_content = []
    variantsettings_file_list = []
    variantsettings_content_text = ""

    #PRODUCT
    setting_file = "Settings_PRODUCT.xml"
    if os.path.exists(os.path.join(SETTINGS_PATH, setting_file)):
        variantsettings_file_list = [setting_file]

    #PRODUCT_{product}
    setting_file = "Settings_PRODUCT_" + product_name + ".xml"
    if os.path.exists(os.path.join(SETTINGS_PATH, setting_file)):
        variantsettings_file_list.append(setting_file)

    #DS/SS
    if "_ds" in product_nick_name:
        setting_file = "Settings_DS.xml"
    elif "_ss" in product_nick_name:
        setting_file = "Settings_SS.xml"
    if os.path.exists(os.path.join(SETTINGS_PATH, setting_file)):
        variantsettings_file_list.append(setting_file)

    #DS/SS_{product}
    if "_ds" in product_nick_name:
        setting_file = "Settings_DS_" + product_name + ".xml"
    elif "_ss" in product_nick_name:
        setting_file = "Settings_SS_" + product_name + ".xml"
    if os.path.exists(os.path.join(SETTINGS_PATH, setting_file)):
        variantsettings_file_list.append(setting_file)

    #MV
    sub_region = sv_sub_region.split(">")[1]     #Strip the "SV>" from "SV>EURO_RU"
    mv = sub_region.split("_")[0]
    if mv == "LTA":
        mv = "LATAM"
    setting_file = "Settings_MV_" + mv + ".xml"
    if os.path.exists(os.path.join(SETTINGS_PATH, setting_file)):
        variantsettings_file_list.append(setting_file)

    #MV_{product}
    setting_file = "Settings_MV_" + mv + product_name + ".xml"
    if os.path.exists(os.path.join(SETTINGS_PATH, setting_file)):
        variantsettings_file_list.append(setting_file)

    #SV
    sub_region = sv_sub_region.split(">")[1]
    mv = sub_region.split("_")[0]
    setting_file = "Settings_SV_" + sub_region + ".xml"
    if mv == "LTA":
        setting_file = setting_file.replace("LTA", "LATAM")
    if os.path.exists(os.path.join(SETTINGS_PATH, setting_file)):
        variantsettings_file_list.append(setting_file)

    #SV_{product}
    setting_file = "Settings_SV_" + sub_region + "_" + product_name + ".xml"
    if mv == "LTA":
        setting_file = setting_file.replace("LTA", "LATAM")
    if os.path.exists(os.path.join(SETTINGS_PATH, setting_file)):
        variantsettings_file_list.append(setting_file)

    logging.info("[variant_settings_collect]:%s variantsettings_file_list is %s" % (sv_sub_region, variantsettings_file_list))

    for item in variantsettings_file_list:
        item_path = os.path.join(SETTINGS_PATH,item)
        if os.path.exists(item_path):
            with open(item_path) as f:
                for line in f.readlines():
                    if not line.split(): #skip blank line
                        pass
                    else:
                        line = line.strip()
                        line_m = re.search('<VariantSetting\s*packageId="(.+)"\s*settingId="(.+)"\s*value="(.+)"\s*/>', line)
                        if line_m: #skip meaningless lines, not start with "<VariantSetting packageId=....."
                            line_settingId = line_m.group(2)
                            line_value = line_m.group(3)
                            for inneritem in variantsettings_content:
                                innerline_m = re.search('<VariantSetting\s*packageId="(.+)"\s*settingId="(.+)"\s*value="(.+)"\s*/>', inneritem.strip())
                                if innerline_m:
                                    innerline_settingId = innerline_m.group(2)
                                    innerline_value = innerline_m.group(3)
                                    if line_settingId == innerline_settingId:
                                        variantsettings_content.remove(inneritem)

                            variantsettings_content.append(line)

    variantsettings_content_text = "\n".join(list(set(variantsettings_content)))

    return variantsettings_content_text

def get_codelist_info(codelist):
    """
    get necessary info from code list file.

    line example:
        MV 1302 059W210 9G-EURO RM-1056 NDT EURO|NO_SD|2300

        SV 2300 059W210 RM-1056 NDT EURO COMMON


    Args:
        codelist:

    Returns:
        ctr_code_list: ['0500001', '0590002', '059W0Q7', '059W1V5', ...]
        variant_region: {'059W2Z0': ['NDT', 'INDIA', 'IN'], '059W0Q7': ['NDT', 'EURO'], ...}
        country_set: {'059W2Z0': 'IN-India', '059W0Q7': '9G-EURO', '059W1V5': 'CN-China',...}
        sd_card: {'059W2Z0': 'NO_SD', '059W0Q7': 'NO_SD', ...}
        variant_ctrcode_to_subregions : {'059W2Z0': ['INDIA_IN'], '059W0Q7': ['EURO_COMMON', 'EURO_CY_ES_FR_GR_IT', 'EURO_IL_NL', 'EURO_GB_IE'], ...}
        variant_subregion_to_ctrcode : {'EURO_COMMON': '2300', 'APAC_SG': '2318', 'EURO_IL_NL': '2302', ...}
    """

    ctr_code_list = []
    variant_region = {}
    country_set = {}
    sd_card = {}
    variant_subregions = []
    variant_ctrcode_to_subregions = {}
    variant_subregion_to_ctrcode = {}

    if os.path.exists(codelist):
        with open(codelist) as f:
            for line in f.readlines():
                lineinfo = line.strip().split("|")
                variant_info = re.split('\s+', lineinfo[0])
                if line.startswith('#') or not line.split(): #skip comment line and blank line
                    pass
                elif line.startswith('MV'):
                    mv_ctr_code = variant_info[2]
                    ctr_code_list.append(mv_ctr_code)
                    variant_region[mv_ctr_code] = variant_info[5:]
                    country_set[mv_ctr_code] = variant_info[3]
                    sd_card[mv_ctr_code] = lineinfo[1]
                elif line.startswith('SV'):
                    pass
                else:
                    print("Error: Code list line does not start with SV or MV or has blank lines\n")
                    sys.exit()

    for each_ctr_code in ctr_code_list:
        variant_ctrcode_to_subregions[each_ctr_code] = []
        if os.path.exists(codelist):
            with open(codelist) as f:
                for line in f.readlines():
                    lineinfo = line.strip().split("|")
                    variant_info = re.split('\s+', lineinfo[0])
                    if line.startswith('#') or not line.split(): #skip comment line and blank line
                        pass
                    elif line.startswith('MV'):
                        pass
                    elif line.startswith('SV'):
                        if each_ctr_code == variant_info[2]:
                            variant_sub_region_part = variant_info[-1].split(",") # GREECE,CYPRUS,FRANCE,ITALY,SPAIN
                            country_short_name_list = []
                            for item in variant_sub_region_part:
                                country_short_name_list.append(get_country_short_name(item))
                            temp = variant_info[-2] + "_" + ("_".join(sorted(country_short_name_list))) # EURO_CY_ES_FR_GR_IT
                            variant_ctrcode_to_subregions[each_ctr_code].append(temp)
                            variant_subregion_to_ctrcode[temp] = variant_info[1]
                    else:
                        print("Error: Code list line does not start with SV or MV or has blank lines\n")
                        sys.exit()

    logging.info("[get_codelist_info] ctr_code_list = %s", ctr_code_list)
    logging.info("[get_codelist_info] variant_region = %s", variant_region)
    logging.info("[get_codelist_info] country_set = %s", country_set)
    logging.info("[get_codelist_info] sd_card = %s", sd_card)
    logging.info("[get_codelist_info] variant_ctrcode_to_subregions = %s", variant_ctrcode_to_subregions)
    logging.info("[get_codelist_info] variant_subregion_to_ctrcode = %s", variant_subregion_to_ctrcode)

    return ctr_code_list, variant_region, country_set, sd_card, variant_ctrcode_to_subregions, variant_subregion_to_ctrcode

def get_country_mcc_info():
    """
    Generate country name and mcc code look up table

    example:
        EURO COMMON:E_C:216,226,228,230,231,232,259,260,262,270,286,284
        ANDORRA:AD:213
    Args:
        None
    Returns:
        clongname_cshortname: {'ERITREA': 'ER', 'PORTUGAL': 'PT', 'MONTENEGRO': 'ME', ...}
        clongname_mcc: {'ERITREA': '234', 'PORTUGAL': '457' ...}
        cshortname_mcc: {'BD': '470', 'BE': '206', 'BF': '613',....}
        mcc_cshortname: {'216': 'HU', '214': 'ES', '212': 'MC',....}

    """
    clongname_cshortname = {}
    clongname_mcc = {}
    cshortname_mcc = {}
    mcc_cshortname = {}

    if os.path.exists(COUNTRY_MCC_FILE):
        with open(COUNTRY_MCC_FILE) as f:
            for line in f.readlines():
                mcc_info = line.strip().split(":")
                clongname_cshortname[mcc_info[0]] = mcc_info[1]
                clongname_mcc[mcc_info[0]] = mcc_info[2]
                cshortname_mcc[mcc_info[1]] = mcc_info[2]
                mcc_cshortname[mcc_info[2]] = mcc_info[1]

    return clongname_cshortname, clongname_mcc, cshortname_mcc, mcc_cshortname


def get_country_short_name(country_long_name):
    """
    convert country full name into short name, example: GREECE->GR

    Args:
        country long name
    Returns:
        country short name

    """
    clongname_cshortname, clongname_mcc, cshortname_mcc, mcc_cshortname = get_country_mcc_info()

    if country_long_name == "COMMON":
        return "COMMON"
    elif country_long_name in cshortname_mcc.keys():
        return country_long_name
    elif country_long_name in clongname_cshortname.keys():
        return clongname_cshortname[country_long_name]
    else:
        print("Error: [get_country_short_name] no this country: %s in country_mcc.txt" % country_long_name)
        sys.exit()

def content_keyinfo_string_update(content_keyinfo):
    """
    Update the content applyto string : SV>EURO:GREECE,CYPRUS,FRANCE,ITALY,SPAIN
    into this format:    SV>EURO_CY_ES_FR_GR_IT

    Args:
        content_keyinfo:
    Returns:

    """

    if content_keyinfo.startswith('PRODUCT'):
        return content_keyinfo
    elif content_keyinfo.startswith('MV'):  #MV>CHINA
        return content_keyinfo
    elif content_keyinfo.startswith('SV'):  #SV>EURO:GREECE,CYPRUS,FRANCE,ITALY,SPAIN
        sub_region_country_long_name_list = content_keyinfo.split(":")[1].split(",")
        content_keyinfo = content_keyinfo.split(":")[0]
        country_list = []
        for country_long_name in sub_region_country_long_name_list:
            country_list.append(get_country_short_name(country_long_name))
        for country_short_name in sorted(country_list):
            content_keyinfo += "_" + country_short_name
        return content_keyinfo  #SV>EURO_CY_ES_FR_GR_IT

def get_content_configure_data_info(content_configure_data):
    """
    get Wallpaper,Music,Video,PreloadedApps,Menu and Homescreen info from content_configure_data file.

    Args:
        content_configure_data: rm1057_athena_ds_content_configure_data.txt (example)

    Returns:
        sv_sub_region_list:
        videos_content:
        music_content:
        menu_content:
        home_content:
        preloadedapps_content:
        lockscreenwallpaper_content:
        ringingtones_content:
    """
    videos_content = {}
    music_content = {}
    menu_content = {}
    home_content = {}
    preloadedapps_content = {}
    lockscreenwallpaper_content = {}
    ringingtones_content = {}
    sv_sub_region_list = []

    if os.path.exists(content_configure_data):
        with open(content_configure_data) as f:
            for line in f.readlines():
                if line.startswith('$') or not line.split(): #skip comment line and blank line
                    pass
                else:
                    content_info = line.strip().split("-")
                    content_keyinfo = content_keyinfo_string_update(content_info[1].strip())

                    if content_info[0] == '#Videos':
                        videos_content[content_keyinfo] = ''.join(content_info[2])
                    elif content_info[0] == '#Music':
                        music_content[content_keyinfo] = ''.join(content_info[2])
                    elif content_info[0] == '#Menu':
                        menu_content[content_keyinfo] = ''.join(content_info[2])
                    elif content_info[0] == '#Home':
                        home_content[content_keyinfo] = ''.join(content_info[2])
                    elif content_info[0] == '#PreloadedApps':
                        sv_sub_region_list.append(content_keyinfo)
                        preloadedapps_content[content_keyinfo] = ''.join(content_info[2])
                    elif content_info[0] == '#LockscreenWallpaper':
                        lockscreenwallpaper_content[content_keyinfo] = ''.join(content_info[2])
                    elif content_info[0] == '#RingingTones':
                        ringingtones_content[content_keyinfo] = ''.join(content_info[2])
                    else:
                        print("Error: There is no this category: %s in %s" % (content_info[0], content_configure_data))
                        sys.exit()
    else:
        print("Error:" + content_configure_data + "not found!\n")
        sys.exit()

    logging.info("[get_content_configure_data_info] sv_sub_region_list = %s", sorted(set(sv_sub_region_list)))
    logging.info("[get_content_configure_data_info] videos_content = %s", videos_content)
    logging.info("[get_content_configure_data_info] music_content = %s", music_content)
    logging.info("[get_content_configure_data_info] menu_content = %s", menu_content)
    logging.info("[get_content_configure_data_info] home_content = %s", home_content)
    logging.info("[get_content_configure_data_info] preloadedapps_content = %s", preloadedapps_content)
    logging.info("[get_content_configure_data_info] lockscreenwallpaper_content = %s", lockscreenwallpaper_content)
    logging.info("[get_content_configure_data_info] ringingtones_content = %s", ringingtones_content)

    return sorted(set(sv_sub_region_list)), videos_content, music_content, menu_content, home_content, preloadedapps_content, lockscreenwallpaper_content, ringingtones_content

def get_generated_variant_applications_list_info(type_designator):
    """
    Get the variant application list info : appName, BGColor etc.. in generated xml, and save them into global variable for using.

    Args:
        type_designator:
    Return
        None
    """
    global VARIANT_APPLICATIONS_APPNAME
    global VARIANT_APPLICATIONS_APPNAME_BGCOLOR

    product_name, product_nick_name, codelist, content_configure_data = find_codelist_and_content_configure_data_files(type_designator)

    generated_file_folder = os.path.join(TOOL_PATH, "..", "..", product_name, "cached-config-base" )
    generated_file_path = os.path.join(generated_file_folder, "".join(os.listdir(generated_file_folder)))

    tree = etree.parse(generated_file_path)
    for elem in tree.iter():
        if elem.tag == "VariantApplication":
            VARIANT_APPLICATIONS_APPNAME.append(elem.get('appName'))
            VARIANT_APPLICATIONS_APPNAME_BGCOLOR[elem.get('appName')] = elem.get('BGColor')

    logging.info("etree [get_generated_variant_applications_list_info] VARIANT_APPLICATIONS_APPNAME=%s", VARIANT_APPLICATIONS_APPNAME)
    logging.info("etree [get_generated_variant_applications_list_info] VARIANT_APPLICATIONS_APPNAME_BGCOLOR=%s", VARIANT_APPLICATIONS_APPNAME_BGCOLOR)

def generate_config_sets_files(type_designator):
    """
    generate {SubRegion}-config-data.xml file in config-sets folder

    Args:
        type_designator:
    Returns:
        None
    """

    config_data_template = os.path.join(TEMPLATE_PATH, "{SubRegion}-config-data.xml")

    product_name, product_nick_name, codelist, content_configure_data = find_codelist_and_content_configure_data_files(type_designator)

    product_output = os.path.join(OUTPUT, product_name)

    sv_sub_region_list, videos_content, music_content, menu_content, home_content, preloadedapps_content, lockscreenwallpaper_content, ringingtones_content = get_content_configure_data_info(content_configure_data)

    if not os.path.exists(os.path.join(product_output, 'config-sets')):
        os.makedirs(os.path.join(product_output, 'config-sets'))

    for each_sv_sub_region in sv_sub_region_list:
        each_sub_region = each_sv_sub_region.split(">")[1]     #Strip the "SV>" from "SV>EURO_RU"
        each_sub_region_file_name = each_sub_region + '-config-data.xml'
        each_sub_region_file_path = os.path.join(product_output, 'config-sets', each_sub_region_file_name)

        #copy {SubRegion}-config-data.xml template to target folder.
        shutil.copyfile(config_data_template, each_sub_region_file_path)

        #update {configuration_name} {config_id} {config_type} {config_name} {config_index} in the template
        configuration_name = each_sub_region.replace("_"," ") + ' Configuration'
        config_id = each_sub_region
        config_type = "Area Configuration"
        config_name = configuration_name
        config_index = "C-0002"

        update_template_content(each_sub_region_file_path,{"{configuration_name}":configuration_name})
        update_template_content(each_sub_region_file_path,{"{config_id}":config_id})
        update_template_content(each_sub_region_file_path,{"{config_type}":config_type})
        update_template_content(each_sub_region_file_path,{"{config_name}":config_name})
        update_template_content(each_sub_region_file_path,{"{config_index}":config_index})

        #update {VideoList} in the template
        video_content_text = ""
        if videos_content:
            video_content_list = videos_content['PRODUCT'].split("/")
            for item in videos_content.keys():
                if item == "PRODUCT":
                    continue
                if item.split(">")[0] == "MV" and each_sub_region.split("_")[0] in item:
                    video_content_list += videos_content[item].split("/")
                if item.split(">")[1] == each_sub_region:
                    video_content_list += videos_content[item].split("/")

            for item in video_content_list:
                if check_media_data(product_name, "Videos", item):
                    video_content_text += '                <Video Name="' + item + '" targetpath="" localpath="common/videos" />\n'

        update_template_content(each_sub_region_file_path,{"{VideoList}":video_content_text})

        #update {MusicList} in the template
        music_content_text = ""
        if music_content:
            music_content_list = music_content['PRODUCT'].split("/")
            for item in music_content.keys():
                if item == "PRODUCT":
                    continue
                if item.split(">")[0] == "MV" and each_sub_region.split("_")[0] in item:
                    music_content_list += music_content[item].split("/")
                if item.split(">")[1] == each_sub_region:
                    music_content_list += music_content[item].split("/")

            for item in music_content_list:
                if check_media_data(product_name, "Music", item):
                    music_content_text += '                <Music Name="' + item + '" targetpath="" localpath="common/audio" />\n'
        update_template_content(each_sub_region_file_path,{"{MusicList}":music_content_text})

        #update {WallpaperList} in the template
        wallpaper_content_text = ""
        if lockscreenwallpaper_content:
            wallpaper_content_list = lockscreenwallpaper_content['PRODUCT'].split("/")
            for item in lockscreenwallpaper_content.keys():
                if item == "PRODUCT":
                    continue
                if each_sub_region.split("_")[0] in item:
                    wallpaper_content_list += lockscreenwallpaper_content[item].split("/")
                if item.split(">")[1] == each_sub_region:
                    wallpaper_content_list += lockscreenwallpaper_content[item].split("/")

            for item in wallpaper_content_list:
                if check_media_data(product_name, "LockscreenWallpaper", item):
                    wallpaper_content_text += '                <Wallpaper Name="' + item + '" targetpath="" localpath="common/images" />\n'
        update_template_content(each_sub_region_file_path,{"{WallpaperList}":wallpaper_content_text})


        #update {RingtoneList} in the template
        ringtones_content_text = ""
        if ringingtones_content:
            ringtones_content_list = ringingtones_content['PRODUCT'].split("/")
            for item in ringingtones_content.keys():
                if item == "PRODUCT":
                    continue
                if each_sub_region.split("_")[0] in item:
                    ringtones_content_list += ringingtones_content[item].split("/")
                if item.split(">")[1] == each_sub_region:
                    ringtones_content_list += ringingtones_content[item].split("/")

            for item in ringtones_content_list:
                if check_media_data(product_name, "RingingTones", item):
                    ringtones_content_text += '                <Ringtone  Name="' + item + '" targetpath="" localpath="common/audio/ringtones" />\n'
        update_template_content(each_sub_region_file_path,{"{RingtoneList}":ringtones_content_text})

        #update {VariantPreloadApplicationsList} in the template
        variantpreloadapp_content_text = ""
        if preloadedapps_content:
            variantpreloadapp_content_list = preloadedapps_content[each_sv_sub_region].split("/")
            for item in variantpreloadapp_content_list:
                if item in VARIANT_APPLICATIONS_APPNAME:
                    variantpreloadapp_content_text += '            <VariantApplication appName="' + item + '" installMethod="preset" />\n'
                else:
                    print("Error: {VariantPreloadApplicationsList} %s not in the generated application list, please check!!" % item)
                    sys.exit()
        update_template_content(each_sub_region_file_path,{"{VariantPreloadApplicationsList}":variantpreloadapp_content_text})

        #update {VariantMenuApplicationsList} in the template
        variantmenuapplication_content_text = ""
        if menu_content:
            variantmenuapplication_content_list = menu_content[each_sv_sub_region].split("/")
            for item in variantmenuapplication_content_list:
                m=re.match("(.*)\((.*)\)", item)
                #color given
                if m:
                    item_name = m.group(1)
                    item_color = m.group(2)
                    if item_name in VARIANT_APPLICATIONS_APPNAME:
                        variantmenuapplication_content_text += '            <VariantApplication appName="' + item_name + '" BGColor="' + item_color + '" />\n'
                    else:
                        print("Error: {VariantMenuApplicationsList} %s not in the generated application list, please check!!" % item)
                        sys.exit()
                #no color given
                else:
                    item_name = m.group(1)
                    if item_name in VARIANT_APPLICATIONS_APPNAME:
                        item_color = VARIANT_APPLICATIONS_APPNAME_BGCOLOR[item_name]
                        variantmenuapplication_content_text += '            <VariantApplication appName="' + item_name + '" BGColor="' + item_color + '" />\n'
                    else:
                        print("Error: {VariantMenuApplicationsList} %s not in the generated application list, please check!!" % item)
                        sys.exit()
        update_template_content(each_sub_region_file_path,{"{VariantMenuApplicationsList}":variantmenuapplication_content_text})

        #update {VariantHomeScreenList} in the template
        varianthomescreen_content_text = ""
        if home_content:
            varianthomescreen_content_list = home_content[each_sv_sub_region].split("/")
            for item in varianthomescreen_content_list:
                m=re.match("(.*)\((.*)\)", item)
                item_name = m.group(1)
                item_position = m.group(2).split(",")

                item_collection = item_position[0]
                item_row = item_position[1]
                item_column = item_position[2]
                item_width = item_position[3]
                item_height = item_position[4]

                if item_name in VARIANT_APPLICATIONS_APPNAME:
                    varianthomescreen_content_text += '            <VariantApplication appName="' + item_name + '" Collection="' + item_collection + '" Row="' + item_row + '" Column="' + item_column + '" Width="' + item_width + '" Height="' + item_height + '" />\n'
                else:
                    print("Error: {VariantHomeScreenList} %s not in the generated application list, please check!!" % item)
                    sys.exit()
        update_template_content(each_sub_region_file_path,{"{VariantHomeScreenList}":varianthomescreen_content_text})

        #update {VariantSettings} in the template
        variantsettings_content_text = ""
        variantsettings_content_text = variant_settings_collect(type_designator, product_name, product_nick_name, each_sv_sub_region)
        update_template_content(each_sub_region_file_path,{"{VariantSettings}":variantsettings_content_text})

    logging.info("[generate_config_sets_files]: config-sets files generated successfully!")
    print("[generate_config_sets_files]: config-sets files generated successfully!")

def generate_variants_files(type_designator):
    """
    generate {ProductName}_{CTR}.xml file in variants folder

    Args:
        type_designator:
    Returns:
        None
    """
    variants_template = os.path.join(TEMPLATE_PATH, "{ProductName}_{CTR}.xml")

    product_name, product_nick_name, codelist, content_configure_data = find_codelist_and_content_configure_data_files(type_designator)

    product_output = os.path.join(OUTPUT,product_name)

    if not os.path.exists(os.path.join(product_output, 'variants')):
        os.makedirs(os.path.join(product_output, 'variants'))

    ctr_code_list, variant_region, country_set, sd_card, variant_ctrcode_to_subregions, variant_subregion_to_ctrcode = get_codelist_info(codelist)

    count = 0
    for each_ctr_code in ctr_code_list:
        count+=1
        variant_file_name = product_name + '_' + each_ctr_code + '.xml'
        variant_file_path = os.path.join(product_output, 'variants', variant_file_name)
        shutil.copyfile(variants_template, variant_file_path)

        #update {variant_package_name} {variant_ctr} {variant_name} {variant_index} {variant_version}
        #       {platform} {type_designator} {country_set} {has_sdcard} in the template
        variant_package_name = ""
        variant_ctr = each_ctr_code
        variant_name = ""
        variant_index = '%04d'%count
        variant_version = "001"
        platform = "AOL"
        has_sdcard = ""
        if "rm" in type_designator:
            type_designator_upper = type_designator.replace("rm", "RM-")
        elif "mm" in type_designator:
            type_designator_upper = type_designator.replace("mm", "MM-")

        variant_name = " ".join(variant_region[each_ctr_code]) + " variant"

        #strip ERA, PAR, TRI operator name from APAC ID region
        if "ID" in variant_region[each_ctr_code]:
            variant_name = " ".join(variant_region[each_ctr_code][:-1]) + " variant"

        variant_package_name = variant_ctr + " " + type_designator_upper + " " + variant_name

        if sd_card[each_ctr_code] == "NO_SD":
            has_sdcard = "False"
        elif sd_card[each_ctr_code] == "HAS_SD":
            has_sdcard = "True"

        update_template_content(variant_file_path,{"{variant_package_name}":variant_package_name})
        update_template_content(variant_file_path,{"{variant_ctr}":variant_ctr})
        update_template_content(variant_file_path,{"{variant_name}":variant_name})
        update_template_content(variant_file_path,{"{variant_index}":variant_index})
        update_template_content(variant_file_path,{"{variant_version}":variant_version})
        update_template_content(variant_file_path,{"{platform}":platform})
        update_template_content(variant_file_path,{"{product_name}":product_name})
        update_template_content(variant_file_path,{"{type_designator}":type_designator_upper})
        update_template_content(variant_file_path,{"{country_set}":country_set[each_ctr_code]})
        update_template_content(variant_file_path,{"{has_sdcard}":has_sdcard})

        #update {variant_config_sets_content} in the template
        variant_config_sets_content = ""
        variant_config_sets_content = variant_config_sets_collect(each_ctr_code, codelist, variant_ctrcode_to_subregions, variant_subregion_to_ctrcode)
        update_template_content(variant_file_path,{"{variant_config_sets_content}":variant_config_sets_content})

    logging.info("[generate_variants_files]: variants files generated successfully!")
    print("[generate_variants_files]: variants files generated successfully!")

def main():

    global OUTPUT

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:t:")
    except getopt.GetoptError as err:
        # print help information and exit:
        print("error message:", err)
        sys.exit(2)

    for opt, value in opts:
        if opt == "-o":
            OUTPUT = value
            print("main OUTPUT",value)
        elif opt == "-t":
            type_designator = value
        elif opt == "-h":
            print('abc.py -t <rm1057> -o <out dir>')
            sys.exit()
        else:
            assert False, "unhandled option"

    # get variant application list info : appName, BGColor etc.. in generated xml, and save them into global variable for using.
    get_generated_variant_applications_list_info(type_designator)

    # generate config_data.xml file in config-sets folder
    generate_config_sets_files(type_designator)

    # generate ctr.xml file in variants folder
    generate_variants_files(type_designator)

    print("[main]: all files generated successfully!")

if __name__ == '__main__':
    main()
