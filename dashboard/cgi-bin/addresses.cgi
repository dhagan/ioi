#!/usr/bin/perl

################################################################################
#
#       File Name: addresses.cgi
#
#       Purpose: This file is used for 
#
#       Copyright © 2007 IOIntegration Inc. Internal use only.
#
#       Revision History:
#
#       Date            Author          Action
#       ----            ------          ------
#       ??/??/2007      B. Scarborough  Created this file
#       08/10/2007      B. Scarborough  Modified to support apostrophes in email addresses
################################################################################

use CGI;
use CGI qw(:standard escapeHTML);
use CGI::Carp "fatalsToBrowser";
use threads;
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
$cgi = new CGI;
my $dbh = getDBConnection();

# Get parameters from query string
$email_type = $cgi->param('email_type');
$comp_case_num = $cgi->param('comp_case_num');

# Style and header information
print $cgi->header();
print $cgi->start_html(-title=>'Add Addresses');
print"<style type='text/css'>
	<!--
	body {
	text-align: center;
	background-color: #808080;
	}
	-->
	</style>";
print"<style type='text/css'>
<!--
.style4 {font-size: 12px}
body,td,th {
	font-size: 12px;
}
-->
</style>";

# Javascript for pasting addresses back into main window
print "<script type='text/javascript' language='javascript'>
	function addAddresses(type)
	{
                var list = document.getElementsByName('emails');
                var input, emails, temp, exists;
                if(navigator.userAgent.indexOf('MSIE') == -1) {
                //Non-Internet Explorer Browsers
                        if(type == \"cc\") {
                                input = window.opener.document.getElementById('cc_div');
                                emails = window.opener.document.getElementsByName('cc_boxes');
                        } else if (type == \"bcc\") {
                                input = window.opener.document.getElementById('bcc_div');
                                emails = window.opener.document.getElementsByName('bcc_boxes');
                        } else {
                                input = window.opener.document.getElementById('to_div');
                                emails = window.opener.document.getElementsByName('to_boxes');
                        }
                        for(var i = 0; i < list.length; i++) {
                                exists = false;
                                if(list[i].checked)
                                {
                                        //checks to see if email address already in checkbox
                                        for(var j = 0; j < emails.length; j++)
                                        {
                                                if(list[i].value == emails[j].value)
                                                        exists = true;
                                        }
                                        if(!exists)
                                        {
                                                temp = document.createElement('INPUT');
                                                temp.setAttribute('type', 'checkbox');
                                                temp.setAttribute('name', type + '_boxes');
                                                temp.setAttribute('value', list[i].value);
                                                temp.setAttribute('checked', 'true');
                                                input.appendChild(temp);
                                                input.appendChild(document.createTextNode(list[i].value));
                                        }
                                }
                        }
                } else {
                //Internet Explorer Browser
                        if(type == \"cc\") {
                                input = window.opener.document.getElementById('cc');
                                emails = window.opener.document.getElementsByName('cc_boxes');
                        } else if (type == \"bcc\") {
                                input = window.opener.document.getElementById('bcc');
                        } else {
                                input = window.opener.document.getElementById('email');
                        }
                        if(input.value.length > 0) {
                                input.value = input.value + ', ';
                        }
                        for(var i = 0; i < list.length; i++) {
                                if(type == 'cc') {
                                        exists = false;
                                        for(var j = 0; j < emails.length; j++)
                                        {
                                                if(list[i].value == emails[j].value)
                                                        exists = true;
                                        }
                                }
                                if(list[i].checked && !exists && (input.value.indexOf(list[i].value)==-1)) {
                                        input.value = input.value + list[i].value + ', ';
                                }
                        }
                        input.value = input.value.substr(0, (input.value.length - 2));
                }
                document.email_form.reset();
	}
        </script>";

$increment = 0;
print "<form name='email_form' id='email_form'><table align='center' border='true' width='550'>";

if($email_type eq "customer" or $email_type eq "supplier") {
        print "<tr><td>", $cgi->h3({-align=>center}, 'Client Emails'), "</td></tr>";
	print "<tr><td>";

	# Gets and displays the company's email address
	$company_email = selectValues("SELECT comp_email FROM company WHERE comp_case_num = '$comp_case_num'");
	print "<input type='checkbox' name='emails' value=\"$company_email\"><b>Company Email</b><br />" if ($company_email ne "");

	# Gets and displays email addresses for individuals in the company
	$sth = $dbh->prepare("SELECT sub_e_mail FROM users WHERE sub_comp_link = '$comp_case_num'");
	$sth->execute();
	while ($email = $sth->fetchrow_array())
	{
        print "<input type = \"checkbox\" name=\"emails\" value=\"$email\">$email ";
        $increment++;
        if($increment == 3)
        {
            print "<br />";
            $increment = 0;
        }
	}
	print "</td></tr>";
	$increment = 0;
}

# Gets and displays email address for IO employees
print "<tr><td>", $cgi->h3({-align=>center}, 'IO Emails'), "</td></tr>";
print "<tr><td><b>IO Techs</b></td></tr><tr><td>";
printIoEmails("IT");
print "</td></tr><tr><td><b>IO Sales</b></td></tr><tr><td>";
printIoEmails("Sales");
print "</td></tr><tr><td><b>IO Staff</b></td></tr><tr><td>";
printIoEmails("Staff");

print "</td></tr><tr><td>";

# Buttons
print " <button type='reset'>Clear</button>";
print " <button type='button' onClick='addAddresses(\"to\")'>Add to Recipients</button>" if ($email_type eq "tech");
print "	<button type='button' onClick='addAddresses(\"cc\")'>Add to CCs</button>
	<button type='button' onClick='addAddresses(\"bcc\")'>Add to BCCs</button>
	<button type='close' onClick='window.close()'>Close</button>
	</td></tr></table></form>";
print $cgi->end_html();

#   Disconnect
$sth->finish();
$dbh->commit();
$dbh->disconnect();

sub printIoEmails {
        $sth = $dbh->prepare("select sa_e_mail from staff where sa_dept = '$_[0]' and sa_access <> 'Disabled'");
        $sth->execute();
        $increment = 0;
        while ($email = $sth->fetchrow_array())
        {
                print "<input type = 'checkbox' name= 'emails' value='$email'>$email ";
                $increment++;
                if($increment == 3)
                {
                        print "<br />";
                        $increment = 0;
                }
        }
}
