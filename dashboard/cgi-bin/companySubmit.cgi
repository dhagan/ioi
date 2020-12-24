#!/usr/bin/perl

################################################################################
#
#       File Name: companySubmit.cgi
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
#       02/09/2007      B. Scarborough  Modified to insure lowercase email addresses
################################################################################

$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
use DBI;
use CGI;
use Time::Format qw(time_format);
use CGI::Carp qw{fatalsToBrowser};
my $dbh = getDBConnection();

$cgi = new CGI;
print $cgi->header();
print $cgi->start_html();
$comp_name = $cgi->param('comp_name');
$comp_phone = $cgi->param('comp_phone');
$comp_fax = $cgi->param('comp_fax');
$comp_www = $cgi->param('comp_www');
$comp_email = lc($cgi->param('comp_email'));
$comp_bill_address = $cgi->param('comp_bill_address');
$comp_bill_city = $cgi->param('comp_bill_city');
$comp_bill_state = $cgi->param('comp_bill_state');
$comp_bill_zip = $cgi->param('comp_bill_zip');
$comp_bill_country = $cgi->param('comp_bill_country');
$comp_ship_address = $cgi->param('comp_ship_address');
$comp_ship_city = $cgi->param('comp_ship_city');
$comp_ship_state = $cgi->param('comp_ship_state');
$comp_name = $dbh->quote($comp_name);
$comp_phone = $dbh->quote($comp_phone);
$comp_fax = $dbh->quote($comp_fax);
$comp_www = $dbh->quote($comp_www);
$comp_bill_address = $dbh->quote($comp_bill_address);
$comp_bill_city = $dbh->quote($comp_bill_city);
$comp_bill_state = $dbh->quote($comp_bill_state);
$comp_bill_zip = $dbh->quote($comp_bill_zip);
$comp_bill_country = $dbh->quote($comp_bill_country);
$comp_ship_address = $dbh->quote($comp_ship_address);
$comp_ship_city= $dbh->quote($comp_ship_city);
$comp_ship_state = $dbh->quote($comp_ship_state);
$comp_email = $dbh->quote($comp_email);
$date=time_format('yyyy/mm/dd');
# $sth = $dbh->prepare("Select * from company where comp_name = '$comp_name'");
# $sth->execute();
# while ( @row = $sth->fetchrow_array ) 
# 	 {
# 	 $comp_test = "@row";
# 	 }
# if ($comp_test ne "")
# {
$sth =$dbh->prepare("Select max(id_num) from company");
$sth->execute();
$id_num = $sth->fetchrow_array();
$id_num += 1;
$sth = $dbh->prepare("select max(comp_case_num) from company");
$sth->execute();
$old_ticket_num = $sth->fetchrow_array();

$old_ticket_num = $' if ($old_ticket_num =~ /COMP/);
$new_ticket_num = $old_ticket_num + 1;
$case_num = "COMP" . $new_ticket_num;
$id_num = $dbh->quote($id_num);
$case_num = $dbh->quote($case_num);
$statement = "Insert into company(date_comp_created,comp_status,id_num,comp_case_num,comp_name, comp_phone,comp_fax,comp_www,comp_bill_address,comp_bill_city,comp_bill_state,comp_bill_zip,comp_bill_country,comp_ship_address,comp_ship_city,comp_ship_state) Values ($date,'Active',$id_num,$case_num,$comp_name,$comp_phone,$comp_fax,$comp_www,$comp_bill_address,$comp_bill_city,$comp_bill_state,$comp_bill_zip,$comp_bill_country,$comp_ship_address,$comp_ship_city,$comp_ship_state)";
$sth = $dbh->prepare("Insert into company(date_comp_created,comp_status,id_num,comp_case_num,comp_name, comp_phone,comp_fax,comp_www,comp_bill_address,comp_bill_city,comp_bill_state,comp_bill_zip,comp_bill_country,comp_ship_address,comp_ship_city,comp_ship_state,comp_email) Values ($date,'Active',$id_num,$case_num,$comp_name,$comp_phone,$comp_fax,$comp_www,$comp_bill_address,$comp_bill_city,$comp_bill_state,$comp_bill_zip,$comp_bill_country,$comp_ship_address,$comp_ship_city,$comp_ship_state,$comp_email)") or die "Can't prepare statement: $DBI::errstr";
$sth->execute() ;
$dbh->commit;
background();
print "<center><font color='#808080'>The company $comp_name was added successfully, if you wish to add products click</font></center> <form name='form1' method='get' action='productSubmit.cgi'> <input type ='hidden' name='comp_case_num' value ='$case_num'  <input type='submit' name='Sumbit' value='Submit Product'></form>
";

# else
# {
# 	print "The company $comp_name is already taken, to enter a new company click <a href= companySubmit.html>here</a>";
# }