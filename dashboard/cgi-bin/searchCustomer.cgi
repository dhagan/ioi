#!/usr/bin/perl

################################################################################
#
#       File Name: searchCustomer.cgi
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
print $cgi->header();
print $cgi->start_html();
$search_name = $cgi->param('customer');
$searchCompany = $cgi->param('company');
$customer_select = $cgi->param('customer_select');
$company_select = $cgi->param('company_select');

if ($search_name ne "" and  $company_select ne "" )
	{	

		$statement = "SELECT sub_name,sub_login,sub_comp_link,sub_e_mail
		FROM users
		WHERE sub_name like '%$search_name%' and sub_comp_link = '$company_select';";
	}
elsif ($search_name ne "" and $company_select eq "")
{
	$statement = "SELECT sub_name,sub_login,sub_comp_link,sub_e_mail
		FROM users
		WHERE sub_name like '%$search_name%'";
}
elsif ($customer_select ne "" and $company_select ne "")
{
		$statement = "SELECT sub_name,sub_login,sub_comp_link,sub_e_mail
		FROM users
		WHERE sub_name like '%$customer_select%' and sub_comp_link = '$company_select';";
}
elsif ($customer_select ne "" and $company_select eq "")
{
	
	$statement = "SELECT sub_name,sub_login,sub_comp_link,sub_e_mail
		FROM users
		WHERE sub_name = '$customer_select'";
}
elsif ($company_select ne "")
{
		$statement = "SELECT sub_name,sub_login,sub_comp_link,sub_e_mail
		FROM users
		WHERE  sub_comp_link = '$company_select';";	
}
elsif ($customer_select ne "")
{
	$statement = "SELECT sub_name,sub_login,sub_comp_link,sub_e_mail
		FROM users
		WHERE sub_name = '$customer_select'";
}
else 
{
	print "<center><font color='#C0C0C0'>Please enter search criteria</font></center>";
}

print "<style type='text/css'>
<!--
body {
	background-color: #C0C0C0;
}

-->
</style>";
if ($statement ne "")
{
	$user = $dbh->prepare($statement);
	$user->execute();
	$i=0;
	tableHead('75%');
	while (($sub_name,$sub_login,$sub_comp_link,$sub_e_email) = $user->fetchrow_array)
	{
		$comp_name = selectValues("SELECT comp_name FROM company WHERE comp_case_num = '$sub_comp_link'");
		print "<tr><td><a href = 'ticketSubmit.cgi?sub_comp_link=$sub_comp_link&sub_login=$sub_login&comp_name=$comp_name[$i]'>$sub_name</a></td><td>$comp_name</td>";
	}
	if ($j == 0)
	{
		print "<center><b>No Search Results were found</center></b>";
	}
	print "</table>";
	#<center><p><p><b>If the user you are searching for is not available you can:
	#  </select><p><center>1.<a href='ticketSubmit.cgi?createCustomer=true'>Create ticket for new customer with existing company</a><p>2.<a href = 'ticketSubmit.cgi?createCompany=true'>Create ticket for new customer with new company</a></center>";
	print "<center><font color='#808080'>If the customer you are looking for is not available click <a href='customerSubmit.cgi?company=$company_select'>here</a> to add them.<p>
		   If the company is not in the database please click <a href ='companySubmit.html'>here</a> to add the company and then submit a customer for that company.</font></center>";
		   
}
print $cgi->end_html();