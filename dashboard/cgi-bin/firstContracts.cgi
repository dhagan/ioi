#!/usr/bin/perl

################################################################################
#
#       File Name: firstContracts.cgi
#
#       Purpose: This file is used for 
#
#       Copyright © 2005 IOIntegration Inc. Internal use only.
#
#       Revision History:
#
#       Date            Author          Action
#       ----            ------          ------
#       12/13/2005      M. Smith        Created this file
#
################################################################################

use CGI qw(:standard escapeHTML);
use CGI::Carp "fatalsToBrowser";
use CGI;
$cgi = new CGI;
use Proc::PidUtil qw(:all);
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
if (param('update'))
{
	update();
}
else
{
	contracts();
}

sub contracts()
{
	$dbh = getDBConnection();
	$comp = $dbh->prepare("SELECT comp_name, comp_case_num FROM company");
	$comp->execute();
	print $cgi->header();
	headers();
	background();
	menu_focus();
	bodyAndLoad();
	tableHead('75%');
	print "<tr><td>Company Name</td><td>Contract type</td><td>Date Purchased</td><td>Date Expired</td><td>Notes</td></tr>";
	print "<form name='form1' action='firstContracts.cgi' method='post'>
	<input type='hidden' name='update' value='yes'>";
	
	while(($comp_name,$comp_case_num) = $comp->fetchrow_array())
	{
		($contract_type,$date_purchased,$date_expired,$contract_notes) = selectValues("SELECT contract_type, contract_date_created, contract_date_expired, contract_notes FROM contract WHERE contract_comp_link = '$comp_case_num'");
		print "<tr><input type = 'hidden' name='comp_case_num' value='$comp_case_num'>
		<td>$comp_name</td><td>";
		dynamicDropDown('ioi_support','','ioi_support') if ($contract_type eq "");
		print "<input type='text' name='ioi_support' value='$contract_type' READONLY>" if ($contract_type ne "");
		print"</td><td><input type='text' name='date_purchased' value='$date_purchased'></td><td>
		<input type='text' name='date_expired' value='$date_expired'></td><td><input type='text' name='notes' value='$contract_notes'></td></tr>";
		
	}
	print "<tr><td><input type='submit' name='submit' value='Submit'></td></tr></table></form>";
	end_HTML;
}
sub update()
{
	@comp_case_num = param('comp_case_num');
	@ioi_support = param('ioi_support');
	@date_purchased = param('date_purchased');
	@date_expired = param('date_expired');
	@notes = param('notes');
	
	for ( $i = 0; $i < $#comp_case_num; $i++)
	{
		my $thisComp = @comp_case_num[$i];
		my $thisSupport = @ioi_support[$i];
		my $thisPurchased = @date_purchased[$i];
		my $thisExpired = @date_expired[$i];
		my $thisNotes = @notes[$i];
		if ($thisSupport ne "")
		{
			$thisNotes = quoteValues($thisNotes);
			insert("INSERT INTO contract (contract_comp_link, contract_type, contract_date_created, contract_date_expired, contract_notes) 
			VALUES ('$thisComp','$thisSupport','$thisPurchased','$thisExpired',$thisNotes)");
		}
	}
	print $cgi->header();
	headers();
	background();
	ioiFont("Contracts inserted successfully");
	end_HTML;
}