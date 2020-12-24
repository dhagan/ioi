#!/usr/bin/perl

################################################################################
#
#       File Name: productCheck.cgi
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
#       02/09/2007      B. Scarborough  Added more columns (version and OS)
#       12/10/2007      B. Scarborough  Added display of contract information
################################################################################

$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
use DBI;
use CGI;
$cgi = new CGI;
print $cgi->header();
print $cgi->start_html();
	print"<style type='text/css'>
	<!--
	body {
	background-color: #C0C0C0;
        color: #808080;
	}
        table {
        color: black;
        }
	-->
	</style>";
$prod_comp_link = $cgi->param("prod_comp_link");
my $dbh = getDBConnection();
$sth = $dbh->prepare("SELECT comp_name FROM company WHERE comp_case_num = '$prod_comp_link'");
$sth->execute;
while(@row = $sth->fetchrow_array)
{
	$comp_name = "@row";
}

$sth = $dbh->prepare("SELECT prod_name,prod_version,prod_oper_sys,prod_part_num FROM product WHERE prod_name <> 'IOI Support' AND prod_comp_link = '$prod_comp_link' order by prod_name asc");
  	$sth->execute();
  	$array_ref = $sth->fetchall_arrayref( );
  	print "<div align='center'><p>Current Products for <b>$comp_name</b></p>";
print "<table width='$width'  border='1' align='center' cellpadding='5' cellspacing='0' bordercolor='#C0C0C0' bgcolor='#909090'>
      <tr>
        <th scope='col'>Product</th>
        <th scope='col'>Version</th>
        <th scope='col'>Operating System</th>
        <th scope='col'>Serial #</th>
      </tr>";
  	foreach my $row (@$array_ref)
  	{
  		my ($product,$version,$oper_sys,$prod_num) = @$row;
  		print "<tr><th scope='row'>$product</th>
                           <td>$version</td>
                           <td>$oper_sys</td>
                           <td>$prod_num</td>";
  	}
  	 print"</table><br /><font color='#808080'>";
  	 $sth = $dbh->prepare("SELECT contract_type, DATE_FORMAT(contract_date_created, '%c/%e/%Y'), DATE_FORMAT(contract_date_expired, '%c/%e/%Y') FROM contract WHERE contract_comp_link = '$prod_comp_link'");
  	 $sth->execute();
  	 my ($contractType, $contractEffective, $contractExpires) = $sth->fetchrow_array();
  	 if ($contractType eq "") {
  	    print "This company has no support information on record.";
  	 } elsif ($contractType eq "NONE") {
  	    print "This company's support level is NONE.";
  	 } else {
  	    print "$contractType Support effective FROM $contractEffective to $contractExpires";
  	 }
  	 
  	 print "</font></div>";
print $cgi->end_html();