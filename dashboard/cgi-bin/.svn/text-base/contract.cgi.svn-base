#!/usr/bin/perl

################################################################################
#
#       File Name: contract.cgi
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
print $cgi->header();
$dbh = getDBConnection();
$dbh-> {'LongReadLen'} = 1000000; 

$sth = $dbh->prepare("select prod_comp_link,prod_version,prod_notes,date_prod_purchased,prod_status from product where prod_name = 'IOI Support'");
$sth->execute();
$count = $dbh->prepare("select max(contract_num) from contract");
$count->execute();
$count = $count->fetchrow_array();
while (($prod_comp_link,$prod_version,$prod_notes,$date_prod_purchased,$prod_status) = $sth->fetchrow_array())
{
	$do_not_send= 0;
	print $date_prod_purchased;
	$date_prod_purchased =~ s/00:00:00//;
	$do_not_send  = 1 if ($date_prod_purchased eq "");
	@date = split(/-/,$date_prod_purchased);
	$new_date = @date[1] . "-" . @date[2] . "-" . @date[0];
	$date_prod_purchased = $new_date;	
	$date_prod_purchased =~ s/ //g;
	$count = $dbh->prepare("select max(contract_num) from contract");
	$count->execute();
	$count = $count->fetchrow_array();
	$count++;
	$statement ="insert into contract (contract_num,contract_comp_link,contract_type,contract_notes,contract_date_created,contract_status) 
	values ($count,'$prod_comp_link','$prod_version','$prod_notes',$date_prod_purchased,'$prod_status')\n";
	print $statement;
	$insert = $dbh->prepare($statement) if ($date_prod_purchased ne "--");
	$insert->execute() if ($date_prod_purchased ne "--");
	}
$dbh->commit;
$sth->finish();
$insert->finish();
$dbh->disconnect();