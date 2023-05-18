from pathlib import Path
import glob
import re
import subprocess
import os
import html_generator_kit

DMS_HOME_PATH = Path(r'C:\apps\devop_tools')


def _get_tc_ci_path():
    path = Path(r"\\plm\pnnas\tc_ci")
    return path


def get_cps_logs_base_dir(dms_node_name: str):
    tc_ci_path = _get_tc_ci_path()
    cps_log_dir = tc_ci_path / "SubmitPipeline" / "awserver" / dms_node_name
    return cps_log_dir


def get_error_file_from_kit_err_dir(kit_error_dir: Path) -> list:
    files = glob.glob(str(kit_error_dir / "*"))
    end_with_err_pattern = r'.*(_err|_err\.log)$'
    error_file = [file for file in files if re.match(
        end_with_err_pattern, file)]
    return error_file


def check_list_have_same_members(lst_1: list, lst_2: list) -> bool:
    x = set(lst_1)
    y = set(lst_2)
    return x == y

#def get_cps_with_no_logs_count(cp_log_path: str()):
   # logs_does_not_exists_count=0
   # common_log_path_pipelineEnd =cp_log_path / "*"
   # if common_log_path_pipelineEnd.exists():
   #         pass
   # else:
    #        logs_does_not_exists_count=logs_does_not_exists_count+1
    #        print("Logs are purged for purged for this CP-}"f"{ logs_does_not_exists_count}")
    #return logs_does_not_exists_count
def process_cps_log(dms_node_name: Path):
    cps_log_dir = get_cps_logs_base_dir(dms_node_name)
    plm_cps_path = glob.glob(str(cps_log_dir / "PLM*"))

    cps_meta = {}
    total_cps_present_release = len(plm_cps_path)
    logs_does_not_exists_count=0

    for cp_log_path in plm_cps_path:

        cp_log_path = Path(cp_log_path)

        cp_name = cp_log_path.name

        # Checking for linux error
        linux_error_dir = cp_log_path / "lnxkitErrorLogs"
        linux_error_files_name = []
        print(f"- CP:{cp_name}")
         #checking if any logs exists
        #logs_does_not_exists_count=get_cps_with_no_logs_count(cp_log_path)
        #if (logs_does_not_exists_count)!=0:
           # print("This CP has no logs"f"{cp_name}{logs_does_not_exists_count}")

        if linux_error_dir.exists():
            print(f"{' '*3}- Linux kit error presents")
            linux_error_files_path = get_error_file_from_kit_err_dir(
                linux_error_dir)
            linux_error_files_name = [
                Path(path).name for path in linux_error_files_path]

        # Checking for windows
        windows_error_dir = cp_log_path / "wntxkitErrorLogs"
        windows_error_files_name = []
        if windows_error_dir.exists():
            print(f"{' '*3}- Windows kit error presents")
            windows_error_files_path = get_error_file_from_kit_err_dir(
                windows_error_dir)
            windows_error_files_name = [
                Path(path).name for path in windows_error_files_path]

        is_same_wntx_lnx_kit_err = check_list_have_same_members(
            linux_error_files_name, windows_error_files_name)

        # Generating meta data for cp
        if len(linux_error_files_name) or len(windows_error_files_name):
            diary_output = get_cp_diary(cp_name)
            is_triage = is_cp_triage_based_on_diary(diary_output)
            cps_meta[cp_name] = {
                "windows_kit_err_file": windows_error_files_name,
                "linux_kit_err_file": linux_error_files_name,
                "is_same_wntx_lnx_kit_err": is_same_wntx_lnx_kit_err,
                "is_triage": is_triage
            }

    return cps_meta, total_cps_present_release


def demo():
    bat_file_name = "dt.cmd"
    bin_dir = DMS_HOME_PATH / "bin"

    bat_file_path = bin_dir / bat_file_name
    print(bat_file_path)
    if bin_dir.exists():
        bin_str = r"C:\apps\devop_tools\bin"
        command = f"{bin_str}\\ dt cp qry PLM829523 -F d"
        subprocess.call(command)
    else:
        print("Error")


def get_cp_diary(cp_name: str):
    cp_name = cp_name.strip()
    if cp_name == "":
        raise Exception("Invalid CP")
    bin_dir = DMS_HOME_PATH / "bin"
    command = f"dt cp qry {cp_name} -F d"
    result = subprocess.run(command, shell=True,
                            cwd=bin_dir, capture_output=True)
    output = result.stdout
    output = output.decode("latin-1")
    return output


def is_cp_triage_based_on_diary(diary_cmd_output: str):
    latest_triage_failed_msg_from_yytcadm = None
    latest_triage_failed_msg_idx = None

    lines = re.split(r'\r?\n', diary_cmd_output)
    for idx, line in enumerate(lines):
        split_str = line.split(":", 2)
        if len(split_str) > 0 and split_str[0].strip() == "user" and split_str[1].strip() == "yytcadm":
            msg = split_str[2]
            if msg.find("SubmitPipeline: Failed") != -1  or msg.find("SubmitPipeline: Aborted") != -1:
                latest_triage_failed_msg_from_yytcadm = msg
                latest_triage_failed_msg_idx = idx

    if latest_triage_failed_msg_idx is None:
        return False

    for i in range(latest_triage_failed_msg_idx, len(lines)):
        line = lines[i]
        split_str = line.split(":", 2)

        if len(split_str) > 0 and split_str[0].strip() == "user" and split_str[1].strip() != "yytcadm":
            #print(split_str[1])
            msg = split_str[2]

            if msg.find("Triage:")!=-1:
                print("This is triaged")
                print(msg)
                return True

    return False


if __name__ == "__main__":
   # out_dir = Path.cwd() / "out"

    dms_node_name = "aw6.3.0.14x"
    out_dir = Path(get_cps_logs_base_dir(dms_node_name))/ "PythonScripts"
    #if not out_dir.exists():
       # os.makedirs(out_dir)

    cps_meta_data, total_cps_to_process = process_cps_log(dms_node_name)
    html_generator_kit.generate_report(
        out_dir, dms_node_name, total_cps_to_process, cps_meta_data)
