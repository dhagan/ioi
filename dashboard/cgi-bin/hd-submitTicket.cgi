#!/usr/bin/perl

################################################################################
#
#       File Name: techSubmit.cgi
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
#
################################################################################

$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
#techSubmit
use DBI;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
my $dbh = getDBConnection();
$cgi = new CGI;
$sub_login = $cgi->param('customer');

## DJH $user = $cgi->param('user');
#$user = getRemoteUser();

($sub_e_mail, $sub_name, $sub_comp_link) = &getUserSession();
if (!$sub_e_mail || !$sub_name || !$sub_comp_link) {
   print $cgi->header();
   print "You appear to be logged out, please login";
   print "<input id='login' type='button' value='Login' onclick=\"window.location='hd-login.cgi'\"/>";
   exit;
}


print $cgi->header();
print "<html><head><title>Ticket Submit</title>
<meta http-equiv=\"Content-Type\" content=\"text/html;charset=iso-8859-1\">
<script language ='javascript'>
function setup()
{
	menu_focus(document.form1.assigned_to,'$user');
}

function menu_focus(el,val)
{
        var j;
        var el_length;
        el_length=el.length;
        for(j=0; j< el_length;j++)
        {
          if(el.options[j].value==val)
          	{
              el.selectedIndex=j;
             }
         }
}
function formOnClick(thisAction)
{
	if (thisAction == \"vendor\")
	{
		document.form1.email_action.value = 'Email Vendor';
	}
	if (thisAction == \"client\")
	{
		document.form1.email_action.value = 'Email Client';
	}
	if (thisAction == \"none\")
	{
		document.form1.email_action.value= 'Submit';
	}
}
function checkSubmit()
{
	

	if (document.form1.assigned_to.value != '$user')
	{
		var checkAssign = confirm('Are you sure you want to assign this to someone other than yourself ($user)');
		if (checkAssign == true)
		{
		}
		else
		{
			menu_focus(document.form1.assigned_to,'$user');
			return false;
		}
	}
	
	if (document.form1.subject.value == '')
	{
		alert('Please enter a short description for this ticket');
		return false;
	}
		
	if (document.form1.problem.value == '')
	{
		alert('Please enter a problem for this ticekt');
		return false;
	}
	if (document.form1.time_spent.value == 0)
	{
		alert('Time Spent is an invalid value');
		return false;
	}

	if (document.form1.time_spent.value >= 1000)
	{	
				
	var checkOver = confirm('This time spent value is too high, if this was meant to be the vendor ticket number click yes');
	if (checkOver == true)
	{
	document.form1.xinet_ticket_num.value = document.form1.time_spent.value;
	}
	document.form1.time_spent.value = '';
	return false;
	}
//	if (document.form1.product.value == '')
//	{
//		alert('Please select a product for this ticket');
//		return false;
//	}
				

}


</script></head><body onLoad='setup()'>";
print "<style type='text/css'>
<!--
body {
	background-color: #ffffff; margin: 25px;
}
-->
</style>
<div style=\"float: right;\">
<input id='helpdesk' type='button' value='Active Tickets' onclick=\"window.location='helpdesk.cgi'\"/>&nbsp;&nbsp;
<input id='logout' type='button' value='Logout' onclick=\"window.location='hd-logout.cgi'\"/>
</div>
<FORM ACTION=\"hd-email2.cgi\" METHOD=\"POST\" ENCTYPE=\"multipart/form-data\" name=\"form1\" onsubmit='return checkSubmit()'>
<input type='hidden' name='newticket' value='true'>
<input type='hidden' name='email_action'>
<input type='hidden' name='submitted_by' value='$sub_e_mail'>
<input type='hidden' name='comp_case_num' value='$sub_comp_link'>
<div align=\"center\">
  <p class=\"style1\"><font color='#808080'>Create Ticket for $sub_name</font></p>
  <table width=\"100%\"  border=\"1\" cellpadding=\"0\" cellspacing=\"0\" bordercolor=\"#C0C0C0\" bgcolor=\"#f5f5f5\">
    <tr>
      <td><span class=\"style3\">Product: <select name=\"product\" id=\"product\">
        <option value=\"\"></option>";
        $sth = $dbh->prepare("select prod_name,prod_case_num from product where prod_comp_link = '$sub_comp_link'");
        $sth->execute();
        while (($prod_name,$prod_case_num) = $sth->fetchrow_array())
        {
        	print "<option value='$prod_case_num'>$prod_name</option>";
        }
  print"  
	  </select></span></td>
</tr>
<tr>
      <td>Priority: 
        <select name=\"priority\" id=\"priority\">
          <option value=\"Critical\">Critical</option>
          <option value=\"High\">High</option>
          <option value=\"Medium\">Medium</option>
          <option value=\"Low\">Low</option>
          </select></td>
</tr>
    <tr>
      <td>Subject: <input name=\"short_desc\" type=\"text\" size=\"75\"></td>
    </tr>
    <tr>
      <td colspan=\"4\"><div align=\"left\">Problem: </div></td>
    </tr>
    <tr>
      <td colspan=\"4\"><div align=\"left\">
        <textarea name=\"problem\" cols=\"95\" rows=\"15\"></textarea>
      </div></td>
    </tr>
    <tr>
      <td colspan=\"4\"><div align=\"left\">Attachment 1 
        <input type=\"FILE\" name=\"attachment1\">
      </div></td>
    </tr>
    <tr>
      <td colspan=\"4\"><div align=\"left\">Attachment 2 
        <input type=\"file\" name=\"attachment2\">
      </div></td>
    </tr>
    <tr>
      <td colspan=\"4\"><div align=\"left\">Attachment 3 
        <input type=\"file\" name=\"attachment3\">
      </div></td>
    </tr>

  </table>
  <p class=\"style1\">
	  		<input type='submit' name='button' value='Create Ticket' onClick='formOnClick(\"none\")'>
    <input type=\"reset\" name=\"Reset\" value=\"Reset\">
  </p>
</div>
</form>
</body>
</html>";
