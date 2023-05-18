import datetime
from pathlib import Path


def get_row_tag_for_cp_info(idx: int, dms_node_name: str, cp_name: str, lnx_kit_err_files: list, wntx_kit_err_files: list, is_wntx_lnx_err_files_equals: bool, is_triage_by_devops_member: bool) -> str:
    cp_name = cp_name.strip()
    link = f"http://devops/self-service/dms/developer-pipeline?cp={cp_name}"

    lnxFlag = False
    if len(lnx_kit_err_files) > 0:
        lnxFlag = True

    wntxflag = False
    if len(wntx_kit_err_files) > 0:
        wntxflag = True

    is_wntx_lnx_err_files_equals = False

    row_tag = f"""
            <tr>
                <th>
                    {idx}
                </th>
                <td>
                    tc
                </td>
                <td>
                    {dms_node_name}
                </td>
                <td>
                    <a href={link} target = \"_self\">{cp_name}</a>
                </td>
                <td>
                    {str(lnxFlag)}
                </td>
                <td>
                    {str(lnx_kit_err_files)}
                </td>
                <td>
                    {str(wntxflag)}
                </td>
                <td>
                    {str(wntx_kit_err_files)}
                </td>
                <td>
                    {str(is_wntx_lnx_err_files_equals)}
                </td>
                <td>
                    {str(is_triage_by_devops_member)}
                </td>
            </tr>
        """
    return row_tag.strip()


def generate_report(out_dir: Path, dms_node_name: str, scaned_cps_count: int, cps_meta_data: dict):
    date = datetime.datetime.now()
    file_path = out_dir / f"{dms_node_name}.html"
    with open(file_path, "w", encoding="utf8") as report_file:

        html_init_content = f"""
<!DOCTYPE html>
    <html>
        <head>
        <style>
            #customers {{font-family: Arial, Helvetica, sans-serif;font-size:15px border-collapse: collapse;}}#customers td, #customers th {{border: 1px solid #ddd;font-weight: normal;padding: 5px;font-size:15px;text-align: center}}#customers tr:nth-child(even){{background-color: #f2f2f2;font-size:15px;text-align: center}}#customers tr:hover {{background-color: #ddd;font-size:10px;text-align: center}}#customers th {{padding-top: 10px;padding-bottom: 10px;text-align: center;background-color: #04AA6D;color: white;}}
        </style>
        </head>
        <section class=\"container\">
            <h1>
                <font-family= Arial, Helvetica, sans-serif;>
                    kit error {dms_node_name}
            </h1>
            <h4>
                <font-family= Arial, Helvetica, sans-serif;>
                    Time:{date}<br>
                <font-family= Arial, Helvetica, sans-serif;>
                    Total CPs scanned:{str(scaned_cps_count)}
                <font-family= Arial, Helvetica, sans-serif;>
                <b>
                    CPs with failure: {len(cps_meta_data)}
                </b>
            </h4>
            <center>
                <table style=\"border:1px solid black;margin-left:auto;margin-right:auto;\">
                    <table class=\"display\" style=\"width:100%\">
                        <table id=\"customers\">
                            <tr style=\"text-align: center;\">
                                <thead>
                                    <tr>
                                        <th></th>
                                        <th></th>
                                        <th></th>
                                        <th>
                                            <input type=\"text\" name=\"search\" id=\"input2_CP\" placeholder=\"Search CP\"onkeyup=\"searchFunCP()\" />
                                        </th>
                                        <th>
                                            <form><select id=\"Linux flag\" onchange=\"searchFunlnxFlag()\"; >
                                                <option  value=\"none\"selected>
                                                </option>
                                                <option onselect=\"searchFunlnxFlag()\"; value=\"True\">
                                                    True
                                                </option>
                                                <option onselect=\"searchFunlnxFlag()\";value=\"False\">
                                                    False
                                                </option>
                                            </form>
                                        </th>
                                        <th>
                                            <input type=\"text\" name=\"search4\" id=\"input4_lnxFile\" placeholder=\"Search lnxFile\"onkeyup=\"searchFunlnxFile()\" />
                                        </th>
                                        <th>
                                            <form>
                                                <select id=\"Windows flag\" onchange=\"searchFunwnx64Flag()\"; >
                                                    <option value=\"none\"selected>
                                                    </option>
                                                    <option onselect=\"searchFunlnxFlag()\"; value=\"True\">
                                                        True
                                                    </option>
                                                    <option onselect=\"searchFunlnxFlag()\";value=\"False\">
                                                        False
                                                    </option>
                                                </select>
                                            </form>
                                        </th>
                                        <th>
                                            <input type=\"text\" name=\"search6\" id=\"input6_wnx64File\" placeholder=\"Search wnxFile\"onkeyup=\"searchFunwnxFile()\" />
                                        </th>
                                        <th>
                                            <form>
                                                <select id=\"Equal flag\" onchange=\"searchFunequalFlag()\"; >
                                                    <option  value=\"none\"selected>
                                                    </option>
                                                    <option onselect=\"searchFunlnxFlag()\"; value=\"True\">
                                                        True
                                                    </option>
                                                    <option onselect=\"searchFunlnxFlag()\";value=\"False\">
                                                        False
                                                    </option>
                                                </select>
                                            </form>
                                        </th>
                                        <th>
                                        <form><select id=\"Triage flag\" onchange=\"searchTriageFlag()\"; >
                                                <option  value=\"none\"selected>
                                                </option>
                                                <option onselect=\"searchTriageFlag()\"; value=\"True\">
                                                    True
                                                </option>
                                                <option onselect=\"searchTriageFlag()\";value=\"False\">
                                                    False
                                                </option>
                                            </form>
                                        </th>
                                    </tr>
                                    <tr>
                                        <th>
                                            Sr No
                                        </th>
                                        <th>
                                            Product
                                        </th>
                                        <th>
                                            DMS Node
                                        </th>
                                        <th>
                                            CP
                                        </th>
                                        <th>
                                            Linux error flag
                                        </th>
                                        <th>
                                            File name
                                        </th>
                                        <th>
                                            Windows error flag
                                        </th>
                                        <th>
                                            File name
                                        </th>
                                        <th>
                                            Same Error
                                        </th>
                                        <th>
                                            Triaged?
                                        </th>
                                    </tr>
                                </thead>
        """

        row_tags = []

        for idx, cp in enumerate(cps_meta_data):
            print(cp)
            windows_kit_err_files = cps_meta_data[cp]["windows_kit_err_file"]
            linux_kit_err_files = cps_meta_data[cp]["linux_kit_err_file"]
            is_same_wntx_lnx_kit_err = cps_meta_data[cp]["is_same_wntx_lnx_kit_err"]
            is_triage = cps_meta_data[cp]["is_triage"]
            row_tag = get_row_tag_for_cp_info(
                idx+1, dms_node_name, cp, linux_kit_err_files, windows_kit_err_files, is_same_wntx_lnx_kit_err, is_triage)
            row_tags.append(row_tag)

        all_rows_tag = '\n'.join(row_tags)

        tbody = f"""
                                <tbody>
                                    {all_rows_tag}
                                </tbody>
        """

        end_html = f"""
                            </tr>
                        </table>
                    </table>
                </table>
            </center>
        </section>
            <font color=\"#04AA6D\";font-family= Arial, Helvetica, sans-serif;>
            <b>
                CPs with failure: {len(cps_meta_data)}
            </b>
            <script>
            const searchFunCP = () => {{
                let filter = document.getElementById('input2_CP').value.toLowerCase();
                let myTable = document.getElementById('customers');
                let tr = myTable.getElementsByTagName('tr');
                for (var i = 0; i < tr.length; i++) {{
                    let td = tr[i].getElementsByTagName('td')[2];
                    if (td) {{
                        let textvlaue = td.textContent || td.innerHTML;
                        if (textvlaue.toLowerCase().indexOf(filter) > -1) {{
                            tr[i].style.display =\"\";
                        }}
                        else {{
                            tr[i].style.display =\"none\";
                        }}
                    }}
                }}
            }}
            const searchFunlnxFlag = () => {{
                let filter = document.getElementById('Linux flag').value.toLowerCase();
                let myTable = document.getElementById('customers');
                let tr = myTable.getElementsByTagName('tr');
                for (var i = 0; i < tr.length; i++) {{
                    let td = tr[i].getElementsByTagName('td')[3];
                    if (td) {{
                        let textvlaue = td.textContent || td.innerHTML;
                        if (textvlaue.toLowerCase().indexOf(filter) > -1) {{
                            tr[i].style.display =\"\";
                        }} else if (filter ==\"none\"){{
                        tr[i].style.display =\"\";
                    }} else {{
                        tr[i].style.display =\"none\";
                    }}
                }}
            }}
                            }}
            const searchFunlnxFile = () => {{
                let filter = document.getElementById('input4_lnxFile').value.toLowerCase();
                let myTable = document.getElementById('customers');
                let tr = myTable.getElementsByTagName('tr');
                for (var i = 0; i < tr.length; i++) {{
                    let td = tr[i].getElementsByTagName('td')[4];
                    if (td) {{
                        let textvlaue = td.textContent || td.innerHTML;
                        if (textvlaue.toLowerCase().indexOf(filter) > -1) {{
                            tr[i].style.display =\"\";
                        }} else {{
                            tr[i].style.display =\"none\";
                        }}
                    }}
                }}
            }}

            const searchFunwnx64Flag = () => {{
                let filter = document.getElementById('Windows flag').value.toLowerCase();
                let myTable = document.getElementById('customers');
                let tr = myTable.getElementsByTagName('tr');
                for (var i = 0; i < tr.length; i++) {{
                    let td = tr[i].getElementsByTagName('td')[5];
                    if (td) {{
                        let textvlaue = td.textContent || td.innerHTML;
                        if (textvlaue.toLowerCase().indexOf(filter) > -1) {{
                            tr[i].style.display =\"\";
                        }} else if (filter ==\"none\"){{
                        tr[i].style.display =\"\";
                    }} else {{
                        tr[i].style.display =\"none\";
                    }}
                }}
            }}
            }}
            const searchFunwnxFile = () => {{
                let filter = document.getElementById('input6_wnx64File').value.toLowerCase();
                let myTable = document.getElementById('customers');
                let tr = myTable.getElementsByTagName('tr');
                for (var i = 0; i < tr.length; i++) {{
                    let td = tr[i].getElementsByTagName('td')[6];
                    if (td) {{
                        let textvlaue = td.textContent || td.innerHTML;
                        if (textvlaue.toLowerCase().indexOf(filter) > -1) {{
                            tr[i].style.display =\"\";
                        }} else {{
                            tr[i].style.display =\"none\";
                        }}
                    }}
                }}
            }}

            const searchFunequalFlag = () => {{
                let filter = document.getElementById('Equal flag').value.toLowerCase();
                let myTable = document.getElementById('customers');
                let tr = myTable.getElementsByTagName('tr');
                for (var i = 0; i < tr.length; i++) {{
                    let td = tr[i].getElementsByTagName('td')[7];
                    if (td) {{
                        let textvlaue = td.textContent || td.innerHTML;
                        if (textvlaue.toLowerCase().indexOf(filter) > -1) {{
                            tr[i].style.display =\"\";
                        }} else if (filter ==\"none\"){{
                        tr[i].style.display =\"\";
                    }} else {{
                        tr[i].style.display =\"none\";
                    }}
                }}
            }}
            }}
             const searchTriageFlag = () => {{
                let filter = document.getElementById('Triage flag').value.toLowerCase();
                let myTable = document.getElementById('customers');
                let tr = myTable.getElementsByTagName('tr');
                for (var i = 0; i < tr.length; i++) {{
                    let td = tr[i].getElementsByTagName('td')[8];
                    if (td) {{
                        let textvlaue = td.textContent || td.innerHTML;
                        if (textvlaue.toLowerCase().indexOf(filter) > -1) {{
                            tr[i].style.display =\"\";
                        }} else if (filter ==\"none\"){{
                        tr[i].style.display =\"\";
                    }} else {{
                        tr[i].style.display =\"none\";
                    }}
                }}
            }}
            }}
            </script>
    </html>

        """

        complete_html = html_init_content + tbody + end_html

        with open(out_dir / f"{dms_node_name}KitError.html", 'w') as file:
            file.write(complete_html)
