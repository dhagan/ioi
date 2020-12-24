#!/usr/bin/perl

################################################################################
#
#       File Name: productSubmit.cgi
#
#       Purpose: This file is used for 
#
#       Copyright © 2005 IOIntegration Inc. Internal use only.
#
#       Revision History:
#
#       Date            Author          Action
#       ----            ------          ------
#       ??/??/2005      M. Smith        Created this file
#       02/09/2007      B. Scarborough  Modified JS function productCheck to change
#                                       height/width for popup window
#       02/27/2007      B. Scarboorugh  Added printYears() function at end and throughout
################################################################################

use CGI;
use DBI;
use Time::Format;
$cgi = new CGI;
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
$comp_case_num= $cgi->param('comp_case_num');
my $dbh = getDBConnection();
$sth = $dbh->prepare("Select comp_name from company where comp_case_num = '$prod_comp_link'");
$sth->execute();
 while ( @row = $sth->fetchrow_array ) 
  {
  $comp_name = "@row";
  }
printHtml();



sub printHtml
{
print $cgi->header();

print "
<title>Product Submit</title>
<style type='text/css'>
<!--
.style4 {font-size: 12px}
body,td,th {
	font-size: 12px;
}
-->
</style>
</head>
	  <script language='JavaScript' type='text/JavaScript'>
	
function focus()
{
				menu_focus(document.form1.comp_name,\"$comp_case_num\");
				productCheck(\"$comp_case_num\");
}
function BrowserInfo()
{
  this.name = navigator.appName;
  this.codename = navigator.appCodeName;
  this.version = navigator.appVersion.substring(0,4);
  this.exeatform = navigator.exeatform;
  this.javaEnabled = navigator.javaEnabled();
  this.screenWidth = screen.width;
  this.screenHeight = screen.height;
}
function serialUpdate()
{
	document.form1.webnative_serial.value = document.form1.fullpress_serial.value;
	document.form1.portal_serial.value = document.form1.fullpress_serial.value;
	document.form1.flashnet_serial.value = document.form1.fullpress_serial.value;
	document.form1.flashweb_serial.value = document.form1.fullpress_serial.value;
}
/*function changeExp(thisExp,thisPur)
{
	document.form1.thisExp.value = document.form1.thisPur.value;
}*/
function compCheck()
{
	if (document.form1.comp_name.value == '')
	{	
		alert('No company is selected');
		return false;
	}
	else if (document.form1.fullpress.checked)
	{
		if (document.form1.fullpress_serial.value == '')
		{
			alert('Fullpress serial number can not be empty, please enter a serial number');
			return false;
		}
	}
	else if (document.form1.server.checked)
	{
		if (document.form1.server_serial.value == '')
		{
			alert('Please enter a serial number for the server');
			return false;
		}
	}
		
	else if (document.form1.raid.checked)
	{
		if (document.form1.raid_serial.value == '')
		{
			alert('Please enter a serial number for the Raid');
			return false;
		}
	}	
	else if (document.form1.tape_libraries.checked)
	{
		if (document.form1.tape_serial.value == '')
		{
			alert('Please enter a serial # for the Tape Library');
			return false;
		}
	}
	
	else
	{
			document.form1.webnative_serial.disabled = false;
		document.form1.portal_serial.disabled = false;
		document.form1.flashnet_serial.disabled = false;
		document.form1.flashweb_serial.disabled = false;
		return true;
	}
}
function xinetUpdate()
{
	menu_focus(document.form1.webnative_os,document.form1.fullpress_os.value);
	menu_focus(document.form1.portal_os,document.form1.fullpress_os.value);
	menu_focus(document.form1.flashnet_os,document.form1.fullpress_os.value);
	menu_focus(document.form1.flashweb_os,document.form1.fullpress_os.value);
	menu_focus(document.form1.webnative_day,document.form1.fullpress_day.value);
	menu_focus(document.form1.webnative_month,document.form1.fullpress_month.value);
	menu_focus(document.form1.webnative_year,document.form1.fullpress_year.value);
	menu_focus(document.form1.portal_day,document.form1.fullpress_day.value);
	menu_focus(document.form1.portal_month,document.form1.fullpress_month.value);
	menu_focus(document.form1.portal_year,document.form1.fullpress_year.value);
	menu_focus(document.form1.flashnet_day,document.form1.fullpress_day.value);
	menu_focus(document.form1.flashnet_month,document.form1.fullpress_month.value);
	menu_focus(document.form1.flashnet_year,document.form1.fullpress_year.value);
	menu_focus(document.form1.flashweb_day,document.form1.fullpress_day.value);
	menu_focus(document.form1.flashweb_month,document.form1.fullpress_month.value);
	menu_focus(document.form1.flashweb_year,document.form1.fullpress_year.value);	
	menu_focus(document.form1.webnative_exp_year,document.form1.fullpress_exp_year.value);
	menu_focus(document.form1.portal_exp_year,document.form1.fullpress_exp_year.value);
	menu_focus(document.form1.flashnet_exp_year,document.form1.fullpress_exp_year.value);
	menu_focus(document.form1.flashweb_exp_year,document.form1.fullpress_exp_year.value);
	menu_focus(document.form1.webnative_exp_month,document.form1.fullpress_month.value);
	menu_focus(document.form1.portal_exp_month,document.form1.fullpress_month.value);
	menu_focus(document.form1.flashnet_exp_month,document.form1.fullpress_month.value);
	menu_focus(document.form1.flashweb_exp_month,document.form1.fullpress_month.value);
	menu_focus(document.form1.webnative_exp_day,document.form1.fullpress_day.value);
	menu_focus(document.form1.portal_exp_day,document.form1.fullpress_day.value);
	menu_focus(document.form1.flashnet_exp_day,document.form1.fullpress_day.value);
	menu_focus(document.form1.flashweb_exp_day,document.form1.fullpress_day.value);
	


}
function productCheck(val)
{
	var caseNum = val
	var b = new BrowserInfo();
	if(caseNum != '')
	{
	if(b.name == 'Netscape')
	{
	var window1 = window.open('productCheck.cgi?prod_comp_link=' + caseNum,'productCheck','width=400,height=400,left=0,top=0,scrollbar=yes'); 
	}										

	if(b.name == 'Microsoft Internet Explorer')
	{
	var newwindow = '';
	newwindow = window.open('productCheck.cgi?prod_comp_link=' + caseNum,'productCheck','width=400,height=400,left=0,top=0,scrollbar=yes');
	newwindow.opener = self;
	}	
	}
}

function menu_focus(el,val)
{
        var     j;
        el_length=el.length;
        for(j=0;j<el_length;j++){
                if(el.options[j].value==val){
                        el.selectedIndex=j;
                }
         }
}
function year_menu_focus(el,val)
{
        var     j;
        el_length=el.length;
        for(j=0;j<el_length;j++){
                if(el.options[j].value==val){
                        el.selectedIndex=j+1;
                }
         }
         xinetUpdate();
}
function disableSerial()
{
	if (document.form1.fullpress.checked)
	{
		document.form1.webnative_serial.disabled = true;
		document.form1.portal_serial.disabled = true;
		document.form1.flashnet_serial.disabled = true;
		document.form1.flashweb_serial.disabled = true;
	}
	else {
			document.form1.webnative_serial.disabled = false;
		document.form1.portal_serial.disabled = false;
		document.form1.flashnet_serial.disabled = false;
		document.form1.flashweb_serial.disabled = false;
		}

}
</script>
<style type='text/css'>
	<!--
	body {
	background-color: #C0C0C0;
	}
	-->
	</style>
<center>
<body onLoad = 'focus()' >
<form name='form1' method='get' action='productSubmitRes.cgi'  onSubmit= 'return compCheck()'>
<b>Company</b><select name='comp_name' id='comp_name' onChange='productCheck(document.form1.comp_name.value)'><option value = ''> </option>";
  	$sth= $dbh->prepare("select  comp_name, comp_case_num from company order by comp_name ");
  	$sth->execute();
  	$array_ref = $sth->fetchall_arrayref( );
  	foreach my $row (@$array_ref)
  	{
  		my ($product, $comp_case_num) = @$row;
  		print "<option value ='$comp_case_num'>$product</option>";
  	}
 
        
 
print "</select>
  
         <table width='$95%'  border='1' align='center' cellpadding='5' cellspacing='0' bordercolor='#C0C0C0' bgcolor='#909090'>
      <tr>
        <th width='80' class='style4' scope='col'>Product</th>
        <th width='88' scope='col'><input name='fullpress' type='checkbox' id='FullPress' value='FullPress' onChange='disableSerial()'>
        FullPress</th>
        <th width='95' scope='col'><input name='webnative' type='checkbox' id='webnative' value='WebNative'>
        Webnative</th>
        <th width='88' scope='col'><input name='portal' type='checkbox' id='portal' value='WN Portal'>
        WN Portal </th>
        <th width='100' scope='col'><input name='flashnet' type='checkbox' id='flashnet' value='FlashNet'>
        FlashNet</th>
        <th width='88' scope='col'><input name='flashweb' type='checkbox' id='flashweb' value='FlashWeb'>
        FlashWeb</th>
        <th width='88' scope='col'><input name='ioi_support' type='checkbox' id='ioi_support' value='IOI Support'>
        IOI Support</th>
        <th width='94' scope='col'><input name='swing' type='checkbox' id='swing' value='Swing'>
        Swing </th>
        <th width='88' scope='col'><input name='twist' type='checkbox' id='twist' value='Twist'>
        Twist</th>
        <th width='86' scope='col'><input type='checkbox' name='litho' value='Litho'>
        Litho</th>
        <th width='88' scope='col'><input name='dialogue' type='checkbox' id='dialogue' value='Dialogue'>
        Dialogue</th>
        <th width='88' scope='col'><input type='checkbox' name='server' value='Server'>
        Server</th>
        <th width='88' scope='col'><input type='checkbox' name='raid' value='Raid'>
          Raid</th>
        <th width='88' scope='col'><input name='tape_libraries' type='checkbox' id='tape_libraries' value='Tape Library'>
        Tape Libraries</th>
      </tr>
      <tr>
        <th scope='row'>Serial # </th>
        <td><input name='fullpress_serial' type='text' size='10' onChange='serialUpdate()'></td>
        <td><input name='webnative_serial' type='text' size='10'></td>
        <td><input name='portal_serial' type='text' size='10'></td>
        <td><input name = 'flashnet_serial' type = 'text' size = '10'></td>
        <td><input name = 'flashweb_serial' type = 'text' size = '10'></td>
        <td><center>N/A</center></td>
        <td><center>N/A</center></td>
        <td><center>N/A</center></td>
        <td><center>N/A</center></td>
        <td><center>N/A</center></td>
        <td><input name='server_serial' type='text' size='10'></td>
        <td><input name='raid_serial' type='text' size='10'></td>
        <td><input name='tape_serial' type='text' size='10'></td>
      </tr>
      <tr>
        <th scope='row'>Version</th>
        <td>";
        dynamicDropDown('prod_version','FullPress','fullpress_version');
        print"</td><td>";
        dynamicDropDown('prod_version','WebNative','webnative_version');
        print"</td>
        <td>";
        dynamicDropDown('prod_version','WN Portal','portal_version');
        print"</td>
        <td>";
        dynamicDropDown('prod_version','FlashNet','flashnet_version');
        print"</td>
        <td>";
        dynamicDropDown('prod_version','FullPress','fullpress_version');
        print"</td>
        <td>";
        dynamicDropDown('prod_version','IOI Support','ioi_support_version');
        print"</td>
        <td>";
        dynamicDropDown('prod_version','Swing','swing_version');
        print"</td>
        <td>";
        dynamicDropDown('prod_version','Twist','twist_version');
        print"</td>
        <td>";
        dynamicDropDown('prod_version','Litho','litho_version');
        print"</td>
        <td>";
        dynamicDropDown('prod_version','Dialogue','dialogue_version');
        print"</td>
        <td>";
        dynamicDropDown('prod_version','Server','server_version');
        print"</td>
        <td>";
        dynamicDropDown('prod_version','Raid','raid_version');
        print"
        <td>";
        dynamicDropDown('prod_version','Tape Library','tape_version');
        print"</td>
      </tr>
      <tr>
        <th scope='row'>OS</th>
        <td>";
        dynamicDropDown('prod_oper_sys','','fullpress_os');
        print"</td>
        <td>";
        dynamicDropDown('prod_oper_sys','','webnative_os');
        print"</td>
        <td>";
        dynamicDropDown('prod_oper_sys','','portal_os');
        print"</td>
        <td>";
        dynamicDropDown('prod_oper_sys','','flashnet_os');
        print"</td>
        <td>";
        dynamicDropDown('prod_oper_sys','','flashweb_os');
        print"</td>
        <td>";
        dynamicDropDown('prod_oper_sys','','ioi_os');
        print"</td>
        <td>";
        dynamicDropDown('prod_oper_sys','','swing_os');
        print"</td>
        <td>";
        dynamicDropDown('prod_oper_sys','','twist_os');
        print"</td>
        <td>";
        dynamicDropDown('prod_oper_sys','','litho_os');
        print"</td>
        <td>";
        dynamicDropDown('prod_oper_sys','','dialogue_os');
        print"</td>
        <td>";
        dynamicDropDown('prod_oper_sys','','server_os');
        print"</td>
        <td>";
        dynamicDropDown('prod_oper_sys','','raid_os');
        print"</td>
        <td>";
        dynamicDropDown('prod_oper_sys','','tape_os');
        print"</td>
      </tr>
     <!-- <tr>
        <th scope='row'>PO Number </th>
        <td><input name='fullpress_po' type='text' id='fullpress_po' size='10'></td>
        <td><input name='webnative_po' type='text' id='webnative_po' size='10'></td>
        <td><input name='portal_po' type='text' id='portal_po' size='10'></td>
        <td><input name='flashnet_po' type='text' id='flashnet_po' size='10'></td>
        <td><input name='ioi_po' type='text' id='ioi_po' size='10'></td>
        <td><input name='swing_po' type='text' id='swing_po' size='10'></td>
        <td><input name='twist_po' type='text' id='twist_po' size='10'></td>
        <td><input name='dialogue_po' type='text' id='dialogue_po' size='10'></td>
        <td>&nbsp;</td>
        <td><input name='tape_po' type='text' id='tape_po' size='10'></td>
      </tr>-->
      <tr>
        <th scope='row'>Date Purchased</th>
        <td>          <select name='fullpress_month' id='fullpress_month' onChange='xinetUpdate();menu_focus(document.form1.fullpress_exp_month,this.value);'>
          <option value=' '> </option>";
         printMonth();
         print"
        </select> 
          M 
          <select name='fullpress_day' id='fullpress_day' onChange='xinetUpdate();menu_focus(document.form1.fullpress_exp_day,this.value)'>
          <option value=' '> </option>";
          
          printDay();
          print"
                  </select> 
          D      
          <select name='fullpress_year' id='fullpress_year' onChange='xinetUpdate();year_menu_focus(document.form1.fullpress_exp_year,this.value);'>";
          printYears();
          print "
          </select>
        Yr</td>
        <td><p>
          <select name='webnative_month' id='webnative_month'>
            <option value=' '> </option>";
            printMonth();
            print"
          </select> 
          M
          <select name='webnative_day' id='webnative_day'>
            <option value=' '> </option>";
            printDay();
            print"
          </select> 
          D
          <select name='webnative_year' id='webnative_year'>";
            printYears();
            print "
          </select> 
          Yr    
          </p>
        </td>
        <td><select name='portal_month' id='portal_month'>
          <option value=' '> </option>";
          printMonth();
        print"
        </select>
M
<select name='portal_day' id='portal_day'>
  <option value=' '> </option>";
  printDay();
  print"
</select>
D
<select name='portal_year' id='portal_year'>";
  printYears();
            print "
</select>
Yr </td>
        <td><p>
          <select name='flashnet_month' id='flashnet_month'>
            <option value=' '> </option>";
        printMonth();
    print"
          </select>
M          
<select name='flashnet_day' id='flashnet_day'>
            <option value=' '> </option>";
      printDay();
      print"
          </select>
  D
  <select name='flashnet_year' id='flashnet_year'>";
  printYears();
            print "
        </select>
    Yr </p>
        </td>
        <td><select name='flashweb_month' id='flashweb_month'>
          <option value=' '> </option>";
          printMonth();
   print"
        </select>
M
<select name='flashweb_day' id='flashweb_day'>
  <option value=' '> </option>";
  printDay();
  print"
</select>
D
<select name='flashweb_year' id='flashweb_year'>";
  printYears();
            print "
</select>
Yr </td>
        <td><select name='support_month' id='support_month' onChange = 'menu_focus(document.form1.support_exp_month,this.value)'>
          <option value=' '> </option>";
printMonth();
print"
        </select>
M
<select name='support_day' id='support_day'onChange = 'menu_focus(document.form1.support_exp_day,this.value)'>
  <option value=' '> </option>";
  
printDay();
print"
</select>
D
<select name='support_year' id='support_year'onChange = 'year_menu_focus(document.form1.support_exp_year,this.value)'>";
printYears();
            print "
            </select>
Yr </td>
        <td><select name='swing_month' id='swing_month' onChange = 'menu_focus(document.form1.swing_exp_month,this.value)'>
          <option value=' '> </option>";
printMonth();
print"
        </select>
M
<select name='swing_day' id='swing_day' onChange = 'menu_focus(document.form1.swing_exp_day,this.value)'>
  <option value=' '> </option>";
  printDay();
  print"
</select>
D
<select name='swing_year' id='swing_year' onChange = 'year_menu_focus(document.form1.swing_exp_year,this.value)'>";
  printYears();
            print "
</select>
Yr </td>
        <td><select name='twist_month' id='twist_month' onChange = 'menu_focus(document.form1.twist_exp_month,this.value)'>
          <option value=' '> </option>";
   printMonth();
  print"

        </select>
M
<select name='twist_day' id='twist_day' onChange = 'menu_focus(document.form1.twist_exp_day,this.value)'>
  <option value=' '> </option>";
  printDay();
  print"
</select>
D
<select name='twist_year' id='twist_year' onChange = 'year_menu_focus(document.form1.twist_exp_year,this.value)'>";
printYears();
            print "
</select>
Yr </td>
        <td><select name='litho_month' id='litho_month' onChange = 'menu_focus(document.form1.litho_exp_month,this.value)'>
          <option value=' '> </option>";
          printMonth();
   print"
        </select>
M
<select name='litho_day' id='litho_day' onChange = 'menu_focus(document.form1.litho_exp_day,this.value)'>
  <option value=' '> </option>";
  printDay();
  print"
</select>
D
<select name='litho_year' id='litho_year' onChange = 'year_menu_focus(document.form1.litho_exp_year,this.value)'>";
printYears();
            print "
</select>
Yr </td>
        <td><select name='dialogue_month' id='dialogue_month' onChange = 'menu_focus(document.form1.dialogue_exp_month,this.value)'>
          <option value=' '> </option>";
          printMonth();
         
 print"        
        </select>
M
<select name='dialogue_day' id='dialogue_day' onChange = 'menu_focus(document.form1.dialogue_exp_day,this.value)'>
  <option value=' '> </option>";
  printDay();
  print"
</select>
D
<select name='dialogue_year' id='dialogue_year' onChange = 'year_menu_focus(document.form1.dialogue_exp_year,this.value)'>";
printYears();
            print "
</select>
Yr </td>
        <td><select name='server_month' id='server_month' onChange = 'menu_focus(document.form1.server_exp_month,this.value)'>
          <option value=' '> </option>";
          printMonth();
  print"</select>
M
<select name='server_day' id='server_day' onChange = 'menu_focus(document.form1.server_exp_day,this.value)'>
  <option value=' '> </option>";
  printDay();
  print "
</select>
D
<select name='server_year' id='server_year' onChange = 'year_menu_focus(document.form1.server_exp_year,this.value)'>";
printYears();
            print "
            </select>
Yr </td>
        <td><select name='raid_month' id='raid_month' onChange = 'menu_focus(document.form1.raid_exp_month,this.value)'>
          <option value=' '> </option>";
  printMonth();
  print"
        </select>
M
<select name='raid_day' id='raid_day' onChange = 'menu_focus(document.form1.raid_exp_day,this.value)'>
<option value= ' '> </option>";
printDay();
print"
</select>
D
<select name='raid_year' id='raid_year' onChange = 'year_menu_focus(document.form1.raid_exp_year,this.value)'>";
printYears();
            print "
</select>
Yr </td>
        <td><select name='tape_month' id='tape_month' onChange = 'menu_focus(document.form1.tape_exp_month,this.value)'>
          <option value=' '> </option>";
          printMonth();
print"</select>
M
<select name='tape_day' id='tape_day' onChange = 'menu_focus(document.form1.tape_exp_day,this.value)'>
  <option value=' '> </option>";
printDay();

print "</select>
D
<select name='tape_year' id='tape_year' onChange = 'year_menu_focus(document.form1.tape_exp_year,this.value)'>";
printYears();
            print "
</select>
Yr </td>
      </tr>
     <!-- <tr>
        <th scope='row'>Date Installed </th>
        <td><input name='fullpress_date_inst' type='text' id='fullpress_date_inst' size='10'></td>
        <td><input name='webnative_date_inst' type='text' id='webnative_date_inst' size='10'></td>
        <td><input name='portal_date_inst' type='text' id='portal_date_inst' size='10'></td>
        <td><input name='flashnet_date_inst' type='text' id='flashnet_date_inst' size='10'></td>
        <td><input name='ioi_date_inst' type='text' id='ioi_date_inst' size='10'></td>
        <td><input name='swing_date_inst' type='text' id='swing_date_inst' size='10'></td>
        <td><input name='twist_date_inst' type='text' id='twist_date_inst' size='10'></td>
        <td><input name='dialogue_date_inst' type='text' id='dialogue_date_inst' size='10'></td>
        <td><input name='tape_date_inst' type='text' id='tape_date_inst' size='10'></td>
      </tr>
      <tr>
        <th scope='row'>Product Invoice </th>
        <td><input name='fullpress_prod_inv' type='text' id='fullpress_prod_inv' size='10'></td>
        <td><input name='webnative_prod_inv' type='text' id='webnative_prod_inv' size='10'></td>
        <td><input name='portal_prod_inv' type='text' id='portal_prod_inv' size='10'></td>
        <td><input name='flashnet_prod_inv' type='text' id='flashnet_prod_inv' size='10'></td>
        <td><input name='flashnet_date_pur' type='text' id='flashnet_date_pur' size='10'></td>
        <td><input name='ioi_prod_inv' type='text' id='ioi_prod_inv' size='10'></td>
        <td><input name='swing_prod_inv' type='text' id='swing_prod_inv' size='10'></td>
        <td><input name='twist_prod_inv' type='text' id='twist_prod_inv' size='10'></td>
        <td>&nbsp;</td>
        <td><input name='dialogue_prod_inv' type='text' id='dialogue_prod_inv' size='10'></td>
        <td><input name='dialogue_date_pur' type='text' id='dialogue_date_pur' size='10'></td>
        <td>&nbsp;</td>
        <td><input name='tape_prod_inv' type='text' id='tape_prod_inv' size='10'></td>
      </tr>-->
      <tr>
        <th scope='row'>Options/Model</th>
        <td>";
        dynamicDropDown('sub_prod_name','FullPress','fullpress_options');
        print"</td>
        <td>";
        dynamicDropDown('sub_prod_name','Webnative','webnative_options');
        print"</td>
        <td>&nbsp;</td>
        <td>";
        dynamicDropDown('sub_prod_name','FlashNet','flashnet_options');
        print"</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>";
        dynamicDropDown('sub_prod_name','Swing','swing_options');
        print"</td>
        <td>";
        dynamicDropDown('sub_prod_name','Twist','twist_options');
        print"</td>
        <td>";
        dynamicDropDown('sub_prod_name','Litho','litho_options');
        print"</td>
        <td>";
        dynamicDropDown('sub_prod_name','Dialogue','dialogue_options');
        print"</td>
        <td>";
        dynamicDropDown('sub_prod_name','Server','server_options');
        print"</td>
        <td>";
        dynamicDropDown('sub_prod_name','Raid','raid_options');
        print"</td>
        <td>";
       	print "Media";
        dynamicDropDown('sub_prod_name','Tape Library','tape_options');
        print "Slots:";
        dynamicDropDown('tape_slots','','tape_slots');
        print "Drives:";
        dynamicDropDown('tape_drives','','tape_drives');
        print"</td>
      </tr>
      <tr><th scope= 'row'>Maintenance Exp.</th>
       <td>          <select name='fullpress_exp_month' id='fullpress_exp_month' onChange='xinetUpdate()'>
          <option value=' '> </option>";
         printMonth();
         print "
        </select> 
          M 
          <select name='fullpress_exp_day' id='fullpress_exp_day' onChange='xinetUpdate()'>
          <option value=' '> </option>";
          
          printDay();
          print "
                  </select> 
          D      
          <select name='fullpress_exp_year' id='fullpress_exp_year' onChange='xinetUpdate()'>";
                printYears();
                print "
          </select>
        Yr</td>
        <td><p>
          <select name='webnative_exp_month' id='webnative_exp_month'>
            <option value=' '> </option>";
            printMonth();
            print "
          </select> 
          M
          <select name='webnative_exp_day' id='webnative_exp_day'>
            <option value=' '> </option>";
            printDay();
            print"
          </select> 
          D
          <select name='webnative_exp_year' id='webnative_exp_year'>";
                printYears();
                print "
          </select> 
          Yr    
          </p>
        </td>
        <td><select name='portal_exp_month' id='portal_exp_month'>
          <option value=' '> </option>";
          printMonth();
        print"
        </select>
M
<select name='portal_exp_day' id='portal_exp_day'>
  <option value=' '> </option>";
  printDay();
  print"
</select>
D
<select name='portal_exp_year' id='portal_exp_year'>";
                printYears();
                print"
</select>
Yr </td>
        <td><p>
          <select name='flashnet_exp_month' id='flashnet_exp_month'>
            <option value=' '> </option>";
        printMonth();
    print"
          </select>
M          
<select name='flashnet_exp_day' id='flashnet_exp_day'>
            <option value=' '> </option>";
      printDay();
      print"
          </select>
  D
  <select name='flashnet_exp_year' id='flashnet_exp_year'>";
                printYears();
                print "
        </select>
    Yr </p>
        </td>
        <td><select name='flashweb_exp_month' id='flashweb_exp_month'>
          <option value=' '> </option>";
          printMonth();
   print"
        </select>
M
<select name='flashweb_exp_day' id='flashweb_exp_day'>
  <option value=' '> </option>";
  printDay();
  print"
</select>
D
<select name='flashweb_exp_year' id='flashweb_exp_year'>";
                printYears();
                print "
</select>
Yr </td>
        <td><select name='support_exp_month' id='support_exp_month'>
          <option value=' '> </option>";
printMonth();
print"
        </select>
M
<select name='support_exp_day' id='support_exp_day'>
  <option value=' '> </option>";
  
printDay();
print"
</select>
D
<select name='support_exp_year' id='support_exp_year'>";
                printYears();
                print "
</select>
Yr </td>
        <td><select name='swing_exp_month' id='swing_exp_month'>
          <option value=' '> </option>";
printMonth();
print"
        </select>
M
<select name='swing_exp_day' id='swing_exp_day'>
  <option value=' '> </option>";
  printDay();
  print"
</select>
D
<select name='swing_exp_year' id='swing_exp_year'>";
                printYears();
                print "
</select>
Yr </td>
        <td><select name='twist_exp_month' id='twist_exp_month'>
          <option value=' '> </option>";
   printMonth();
  print"

        </select>
M
<select name='twist_exp_day' id='twist_exp_day'>
  <option value=' '> </option>";
  printDay();
  print"
</select>
D
<select name='twist_exp_year' id='twist_exp_year'>";
                printYears();
                print "
</select>
Yr </td>
        <td><select name='litho_exp_month' id='litho_exp_month'>
          <option value=' '> </option>";
          printMonth();
   print"
        </select>
M
<select name='litho_exp_day' id='litho_exp_day'>
  <option value=' '> </option>";
  printDay();
  print"
</select>
D
<select name='litho_exp_year' id='litho_exp_year'>";
                printYears();
                print "
</select>
Yr </td>
        <td><select name='dialogue_exp_month' id='dialogue_exp_month'>
          <option value=' '> </option>";
          printMonth();
         
 print"        
        </select>
M
<select name='dialogue_exp_day' id='dialogue_exp_day'>
  <option value=' '> </option>";
  printDay();
  print"
</select>
D
<select name='dialogue_exp_year' id='dialogue_exp_year'>";
                printYears();
                print "
</select>
Yr </td>
        <td><select name='server_exp_month' id='server_exp_month'>
          <option value=' '> </option>";
          printMonth();
  print"</select>
M
<select name='server_exp_day' id='server_exp_day'>
  <option value=' '> </option>";
  printDay();
  print "
</select>
D
<select name='server_exp_year' id='server_exp_year'>";
                printYears();
                print "
</select>
Yr </td>
        <td><select name='raid_exp_month' id='raid_exp_month'>
          <option value=' '> </option>";
  printMonth();
  print"
        </select>
M
<select name='raid_exp_day' id='raid_exp_day'>
<option value= ' '> </option>";
printDay();
print"
</select>
D
<select name='raid_exp_year' id='raid_exp_year'>";
                printYears();
                print "
</select>
Yr </td>
        <td><select name='tape_exp_month' id='tape_exp_month'>
          <option value=' '> </option>";
          printMonth();
print"</select>
M
<select name='tape_exp_day' id='tape_exp_day'>
  <option value=' '> </option>";
printDay();

print "</select>
D
<select name='tape_exp_year' id='tape_exp_year'>";
                printYears();
                print "
</select>
Yr </td>
        </table>
   <input type='submit' name='Submit' value='Submit'></center>

</form>
</body>
</html>
";
}
 sub printDay
  {
  for ($i = 1; $i < 32; $i++)
  { print "<option value ='$i'>$i</option>";
  }
  }
  sub printMonth
  {
  for ($i = 1;$i<=12; $i++)
  {
  	print "<option value = '$i'>$i</option>";
  }
  }

# Function: printYears
# Purpose: Displays years for the drop-down boxes from 3 years previous
#          to 4 years in the future (a total of 8 selections) plus a blank
# Inputs: None
# Returns: None

sub printYears()
{
        $date = time_format('yyyy');
        $date -= 3;
        print "<option value=' '> </option>";
        for ($i = 0; $i < 8; $i++, $date++)
        {
                print "<option value='$date'>$date</option>";
        }
}
