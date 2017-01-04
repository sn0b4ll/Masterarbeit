#!/usr/local/bin/python3
"""Web-Applikation zur Generierung von Fragen und Pentest-Reports"""
import os
import subprocess
import string
import hashlib

from flask import Flask, render_template, request, send_file

# From http://uweziegenhagen.de/wp-content/uploads/2013/08/LaTeX_and_Python.pdf
class LaTeXTemplate(string.Template):
    delimiter = "%%"

def __html_to_tex(input):
    return input.replace('\n', "\\\\")

def __html_to_checkbox(request, name):
    if name in request.form:
        return r'\mbox{\ooalign{$\checkmark$\cr\hidewidth$\square$\hidewidth\cr}}'
    else:
        return r'$\square$'

def __handle_alg_zeitraum(input):
    if input == 'buero':
        return r'\mbox{\ooalign{$\checkmark$\cr\hidewidth$\square$\hidewidth\cr}} & $\square$ & $\square$'
    elif input == 'feier':
        return r'$\square$ & \mbox{\ooalign{$\checkmark$\cr\hidewidth$\square$\hidewidth\cr}} & $\square$'
    elif input == 'woend':
        return r'$\square$ & $\square$ & \mbox{\ooalign{$\checkmark$\cr\hidewidth$\square$\hidewidth\cr}}'


def __html_to_radio(text, radio):
    if radio == 'ja':
        return text + r' & \mbox{\ooalign{$\checkmark$\cr\hidewidth$\square$\hidewidth\cr}} & $\square$'
    else:
        return text + r' & $\square$ & \mbox{\ooalign{$\checkmark$\cr\hidewidth$\square$\hidewidth\cr}}'

APP = Flask(__name__)

@APP.route('/fragebogen', methods=['GET'])
def fragebogen():
    return render_template('fragebogen.html')

@APP.route('/fragebogen', methods=['POST'])
def fragebogen_generieren():

    tex_path = os.path.join(os.getcwd(), 'tex')
    print(request.form)
    orig_file = open(tex_path + "/Fragen.tex", 'r')
    template = LaTeXTemplate(orig_file.read())
    orig_file.close()

    new_string = template.substitute(
        allg_anspr_web_app=__html_to_tex(request.form['allg_anspr_web_app']),
        allg_pen_art_wapt=__html_to_checkbox(request, 'allg_pen_art_wapt'),
        allg_pen_art_npt=__html_to_checkbox(request, 'allg_pen_art_npt'),
        allg_pen_art_se=__html_to_checkbox(request, 'allg_pen_art_se'),
        allg_pen_art_wl=__html_to_checkbox(request, 'allg_pen_art_wl'),
        allg_pen_art_phys=__html_to_checkbox(request, 'allg_pen_art_phys'),
        alg_compliance=__html_to_radio(request.form['alg_compliance_text'], request.form['alg_compliance']),
        allg_termin=__html_to_tex(request.form['allg_termin']),
        alg_zeitraum=__handle_alg_zeitraum(request.form['alg_zeitraum']),
        wapt_quell_zug=__html_to_radio(request.form['wapt_quell_zug_text'], request.form['wapt_quell_zug']),
        wapt_anz_web_app=__html_to_tex(request.form['wapt_anz_web_app']),
        wapt_anz_login_sys=__html_to_tex(request.form['wapt_anz_login_sys']),
        wapt_anz_stat_seiten=__html_to_tex(request.form['wapt_anz_stat_seiten']),
        wapt_anz_dyn_seiten=__html_to_tex(request.form['wapt_anz_dyn_seiten']),
        wapt_fuzzing=__html_to_radio(request.form['wapt_fuzzing_text'], request.form['wapt_fuzzing']),
        wapt_vers_rollen=__html_to_radio(request.form['wapt_vers_rollen_text'], request.form['wapt_vers_rollen']),
        wapt_pwd_scan=__html_to_radio(request.form['wapt_pwd_scan_text'], request.form['wapt_pwd_scan']),
        npt_ziel=__html_to_tex(request.form['npt_ziel']),
        npt_anz_ips=__html_to_tex(request.form['npt_anz_ips']),
        npt_verteidigung=__html_to_radio(request.form['npt_verteidigung_text'], request.form['npt_verteidigung']),
        npt_gel_ang=__html_to_tex(request.form['npt_gel_ang']),
        npt_nutz_lok_admin=__html_to_radio(request.form['npt_nutz_lok_admin_text'], request.form['npt_nutz_lok_admin']),
        npt_pwd_hashes=__html_to_radio(request.form['npt_pwd_hashes_text'], request.form['npt_pwd_hashes']),
        se_emails=__html_to_radio(request.form['se_emails_text'], request.form['se_emails']),
        se_tels=__html_to_radio(request.form['se_tels_text'], request.form['se_tels']),
        se_phys=__html_to_radio(request.form['se_phys_text'], request.form['se_phys']),
        se_anz_pers=__html_to_tex(request.form['se_anz_pers']),
        wl_anz_fnw=__html_to_tex(request.form['wl_anz_fnw']),
        wl_gastwlan=__html_to_radio(request.form['wl_gastwlan_text'], request.form['wl_gastwlan']),
        wl_encr=__html_to_tex(request.form['wl_encr']),
        wl_fremgeraet=__html_to_radio(request.form['wl_fremgeraet_text'], request.form['wl_fremgeraet']),
        wl_att_clients=__html_to_radio(request.form['wl_att_clients_text'], request.form['wl_att_clients']),
        wl_clients=__html_to_tex(request.form['wl_clients']),
        phys_anz_einr=__html_to_tex(request.form['phys_anz_einr']),
        phys_anz_part=__html_to_radio(request.form['phys_anz_part_text'], request.form['phys_anz_part']),
        phys_sich_pers=__html_to_radio(request.form['phys_sich_pers_text'], request.form['phys_sich_pers']),
        phys_sich_pers_dritt=__html_to_radio(request.form['phys_sich_pers_dritt_text'], request.form['phys_sich_pers_dritt']),
        phys_sich_pers_waffen=__html_to_radio(request.form['phys_sich_pers_waffen_text'], request.form['phys_sich_pers_waffen']),
        phys_sich_pers_gewalt=__html_to_radio(request.form['phys_sich_pers_gewalt_text'], request.form['phys_sich_pers_gewalt']),
        phys_anz_eing=__html_to_tex(request.form['phys_anz_eing']),
        phys_knacken=__html_to_radio(request.form['phys_knacken_text'], request.form['phys_knacken']),
        phys_flaeche=__html_to_tex(request.form['phys_flaeche']),
        phys_whitebox=__html_to_radio(request.form['phys_whitebox_text'], request.form['phys_whitebox']),
        phys_cam=__html_to_radio(request.form['phys_cam_text'], request.form['phys_cam']),
        phys_cam_dritte=__html_to_radio(request.form['phys_cam_dritte_text'], request.form['phys_cam_dritte']),
        phys_loeschen=__html_to_radio(request.form['phys_loeschen_text'], request.form['phys_loeschen']),
        phys_alarm=__html_to_radio(request.form['phys_alarm_text'], request.form['phys_alarm']),
        phys_alarm_still=__html_to_radio(request.form['phys_alarm_still_text'], request.form['phys_alarm_still']),
        phys_alarm_ausloeser=__html_to_tex(request.form['phys_alarm_ausloeser']),
        sysadm_altsysteme=__html_to_radio(request.form['sysadm_altsysteme_text'], request.form['sysadm_altsysteme']),
        sysadm_drittsysteme=__html_to_radio(request.form['sysadm_drittsysteme_text'], request.form['sysadm_drittsysteme']),
        sysadm_wiederherstellungszeit=__html_to_tex(request.form['sysadm_wiederherstellungszeit']),
        sysadm_monitoring=__html_to_radio(request.form['sysadm_monitoring_text'], request.form['sysadm_monitoring']),
        sysadm_krit_appl=__html_to_tex(request.form['sysadm_krit_appl']),
        sysadm_backup=__html_to_radio(request.form['sysadm_backup_text'], request.form['sysadm_backup']),
        bum_mgmt_inform=__html_to_radio(request.form['bum_mgmt_inform_text'], request.form['bum_mgmt_inform']),
        bum_krit_daten=__html_to_tex(request.form['bum_krit_daten']),
        bum_monitoring=__html_to_radio(request.form['bum_monitoring_text'], request.form['bum_monitoring']),
        bum_disaster_recovery=__html_to_radio(request.form['bum_disaster_recovery_text'], request.form['bum_disaster_recovery']),
    )

    sha3 = hashlib.sha3_384()
    sha3.update(new_string.encode())
    filename = sha3.hexdigest()
    new_file = open('tex/' + filename, 'w')
    new_file.write(new_string)
    new_file.close()

    # Generate PDF from Latex-File
    tex_path = os.path.join(os.getcwd(), 'tex')
    pdf_file = os.path.join(tex_path, filename) + ".pdf"
    os.chdir(tex_path)
    try:
        subprocess.check_output(
            [
                '/usr/local/texlive/2016/bin/x86_64-darwin/pdflatex',
                '-synctex=1',
                '-interaction=nonstopmode',
                filename
            ], cwd=tex_path
        )
    except subprocess.CalledProcessError as error:
        print(error)
    os.chdir("..")
    return send_file(pdf_file, 'Test.pdf')

APP.run(debug=True)
