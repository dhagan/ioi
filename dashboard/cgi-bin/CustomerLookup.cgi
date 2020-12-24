#!/usr/bin/perl

################################################################################
#
#       File Name: CustomerLookup.cgi
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

use DBI;
use CGI;
$cgi = new CGI;

	my $dbh = getDBConnection();
	$dbh-> {'LongReadLen'} = 1000000; 
		
	$sth = $dbh->prepare("SELECT comp_name, comp_case_num FROM company ORDER BY comp_name");
	$customer = $dbh->prepare("SELECT sub_name, sub_comp_link from users ORDER BY sub_name");
	$customer->execute();
	$sth->execute();
	print $cgi->header();
	print $cgi->start_html();
	print "
<style type=\"text/css\">
<!--
body {
	background-color: #C0C0C0;
}

-->
</style>

		<form name='form1' method='post' action='searchCustomer.cgi'>
		  <p align='center'>IOI Ticket Submit/Contact Lookup </p>
		  <table width='80%'  border='1' align='center' cellpadding='5' cellspacing='0' bordercolor='#C0C0C0' bgcolor='#909090'>
			<tr>
			  <td width='18%'><strong>Customer</strong></td>
			  <td width='82%'><div align='center'>
				<input name='customer' type='text' id='customer' size='30'>  
				<select name='customer_select'>
				  <option value = ''></option>";
			   $array_ref2 = $customer->fetchall_arrayref( );
			foreach my $row (@$array_ref2)
			{
				my ($sub_name, $sub_comp_link) = @$row;
				print "<option value ='$sub_name'>$sub_name</option>\n";
			}
		 print"
				</select>
			  </div>
			</tr>
			<tr>
			  <td><strong>Company</strong></td>
			  <td><!--<input name='company' type='text' id='company'></td><td>-->
				<div align='center'>
				  <select name='company_select'>
			<option value = '' name = ''></option>";
			 $array_ref = $sth->fetchall_arrayref();
			foreach my $row (@$array_ref)
			{
				my ($comp_name, $comp_case_num) = @$row;
				print "<option value ='$comp_case_num'>$comp_name</option>\n";
			}
		   print"
				  </select>
				</div>
			</tr>
		  </table>
		  <div align='center'>
			<input name='Submit' type='submit' id='Submit' value='Find'> 
			<input type='reset' name='Reset' value='Reset'>
		  </div>
		</form>";

		
		print"</table></body></html>";