#!/usr/bin/perl

################################################################################
#
#       File Name: preferences2.cgi
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
use CGI;
use DBI;
my $dbh = getDBConnection();

$cgi = new CGI;

### DJH $user = $cgi->param('user');
$user = getRemoteUser();
$update = $cgi->param('update');
$cust_name = $cgi->param('customer_name');

if($update eq "true")
{
	$greeting = $cgi->param('greeting');
	$signature = $cgi->param('signature');
	$sth = $dbh->prepare("update staff set sa_email_header = '$greeting', sa_email_signature = '$signature' where sa_login = '$user'");
	$sth->execute();
	$dbh->commit();
}

$sth = $dbh->prepare("select sa_email_signature,sa_email_header from staff where sa_login = '$user'");
$sth->execute();
($signature,$greeting)= $sth->fetchrow_array();

print $cgi->header();
print $cgi->start_html(-title=>"Preferences for $user");
print "<style type='text/css'>
<!--
body {
	background-color: #C0C0C0;
}
.style1 {color: #000000}
-->
</style>
        <script language='javascript'>
                function submitAction(input)
                {
                        var greeting = document.getElementById('greeting').value;
                        var signature = document.getElementById('signature').value;
                        greeting = greeting.replace(/\\{customer_name}/g, '$cust_name');
                        signature = signature.replace(/\\{customer_name}/g, '$cust_name');
                        window.opener.document.getElementById('greeting').value = greeting;
                        window.opener.document.getElementById('signature').value = signature;
                        input.form.submit();
                }
        </script>
         <div align='center'> <form name='form1' method='post' action='preferences2.cgi'>
	<input type='hidden' name='user' value='$user'>
        <input type='hidden' name='customer_name' value='$cust_name'>
        <input type='hidden' name='update' value='true'>
    <h3 class='style1'>Please edit your preferences for the <br />email greeting and signature </h3>
    <table width='346' height='128' border='1' cellspacing='0' bordercolor='#C0C0C0' bgcolor='#909090'>
      <tr>
        <th scope='row'>Greeting</th>
        <td><textarea id='greeting' name='greeting' cols='40' rows='6'>$greeting</textarea></td>
      </tr>
      <tr>
        <th scope='row'>Signature</th>
        <td><textarea id='signature' name='signature' cols='40' rows='6'>$signature</textarea></td>
      </tr>
      <tr>
        <th scope='row' colspan='2'>Use {customer_name}  as a variable in your greeting/signature and it will be filled in according to the customer you are sending it to. </th>
       
      </tr>
    </table>
    <p class='style1'>
      <input type='button' name='Submit' value='Submit' onClick='submitAction(this)' /><input type='button' name='Close' value='Close' onClick='window.close()' /><p>
    </p>";
if($update eq "true")
{
        print "<h3 class='style1'>Preferences Updated</h3>";
}
print "</form>
  <h3 class='style1'>&nbsp;</h3>
</div>
</body>
</html>";
$dbh->disconnect();
