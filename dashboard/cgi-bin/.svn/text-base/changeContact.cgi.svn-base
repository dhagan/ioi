#!/usr/bin/perl

################################################################################
#
#       File Name: changeContact.cgi
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

use CGI;
use DBI;

$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
my $dbh = getDBConnection();
$dbh-> {'LongReadLen'} = 1000000; 
$cgi = new CGI;
$user = $ENV{"REMOTE_USER"};
$user =~ s/IOINTEGRATION\\//g;
use CGI qw(:standard escapeHTML);

if (param('submit'))
{
	updateTicketContact();
}
else { changeTicketContact(); }

sub changeTicketContact()
{
	$case_num = param('selrow');
	print $cgi->header();
	headers();
	print "<script language ='javascript'>
	function checkSubmit()
	{
		if (document.form1.sub_login.value == '')
		{
			alert('Please select a new user to assign this to');
			return false;
		}
		return true;
	}
	</script>";
	background();
	bodyAndLoad();
	ioiFont("Choose a new user to assign ticket $case_num to.");
	print "<div align='center'>
	<form name='form1' action ='' id='form1' onsubmit='return checkSubmit();'>
	<input type='hidden' name='case_num' value='$case_num'>";
	customerDropDown();
	print "<p><input type='submit' name='submit' value='Change user'></form>";
	end_html();
}

sub updateTicketContact()
{
	print $cgi->header();
	header();
	background();
	bodyAndLoad();
	
	$case_num = param('case_num');
	$sub_login = param('sub_login');
	insert("update problem set submitted_by = '$sub_login' where case_num = '$case_num'");
	ioiFont("Ticket $case_num has been successfully reassigned to '$sub_login'. <p>Click <a href='filterTickets.cgi'>here</a> to go back to the filter tickets page");
	end_html();
}
	
	