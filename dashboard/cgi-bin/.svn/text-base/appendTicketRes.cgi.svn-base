#!/usr/bin/perl

################################################################################
#
#       File Name: appendTicketRes.cgi
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
use File::Find::Rule;
use Tie::Array::Unique;
use CGI qw(:standard escapeHTML);
use CGI::Carp "fatalsToBrowser";
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
$cgi = new CGI;
$from = $cgi->param('from');
$to = $cgi->param('to');
$vendor_ticket = param('vendor_ticket');
$bug_ticket_num = param('bug_ticket_num');
print $cgi->header();
headers();
background();
bodyAndLoad();
$query = "SELECT customer_email,supplier_email,problem,xinet_ticket_num,bug_ticket_num FROM problems WHERE case_num = '$from'";
($from_customer_email,$from_supplier_email,$from_problem,$from_xinet_ticket_num,$from_bug_ticket_num) = selectValues($query) or die "cannot execute query:$!";
$query = "SELECT customer_email,supplier_email,problem,xinet_ticket_num,bug_ticket_num from problems WHERE case_num ='$to'";
($to_customer_email,$to_supplier_email,$to_problem,$to_xinet_ticket_num,$to_bug_ticket_num) = selectValues($query) or die "cannot execute query: $!";

print $to_xinet_ticket_num , ",", $from_xinet_ticket_num , "<p>";
print $to_bug_ticket_num , "," , $from_bug_ticket_num , "<p>";
print $vendor_ticket , "," , $bug_ticket_num;
if ((($to_xinet_ticket_num ne "") or ($from_xinet_ticket_num ne "" and $to_ticket_num ne "")) and $vendor_ticket eq "")
{
	ioiFont("Please choose what vendor ticket number to use");
	tableHead('30%');
	print "<form name ='form1' action='' method='post'>
	<input type='hidden' name='from' value = '$from'>
	<input type='hidden' name='to' value='$to'>
	<tr><td>Old</td><td><input type = 'radio' name='vendor_ticket' value='$to_xinet_ticket_num'>$to_xinet_ticket_num</td></tr>
	<tr><td>New</td><td><input type='radio' name='vendor_ticket' value='$from_xinet_ticket_num'>$from_xinet_ticket_num</td></tr></table>";
	if (($to_bug_ticket_num ne "" and $bug_ticket_num eq "") or ($from_bug_ticket_num ne "" and $to_bug_ticket_num ne ""))
	{	
		tableHead('30%');
		print "<tr>";
		ioiFont("Please choose which bug ticket number to use");
		print "</tr>";
		print "<tr><td>Old</td><td><input type='radio' name='bug_ticket_num' value='$to_bug_ticket_num'>$to_bug_ticket_num</td></tr>
				<tr><td>New</td><td><input type='radio' name='bug_ticket_num' value='$from_bug_ticket_num'>$from_bug_ticket_num</td></tr>";
	}
	print "</table><div align='center'><input type='submit' name='submit' value='Submit'></div></form>";
	exit;
}
if (($to_bug_ticket_num ne "" or $from_bug_ticket_num ne "" and $to_bug_ticket_num ne "") and $bug_ticket_num eq "")
{	
	tableHead('30%');
	print "<tr>";
	ioiFont("Please choose which bug ticket number to use");
	print "</tr>";
	print "<form name ='form1' action='' method='post'>
	<input type='hidden' name='from' value = '$from'>
	<input type='hidden' name='to' value='$to'>";
	print "<tr><td>Old</td><td><input type='radio' name='bug_ticket' value='$to_bug_ticket_num'>$to_bug_ticket_num</td></tr>
		<tr><td>New</td><td><input type='radio' name='bug_ticket' value='$from_bug_ticket_num'>$from_bug_ticket_num</td></tr>";
	print "</table><div align='center'><input type='submit' name='submit' value='Submit'></div></form>";
	exit;
}
	

	

tie my @customer_email, 'Tie::Array::Unique';
tie my @supplier_email, 'Tie::Array::Unique';
@customer_email = (split(/ /,$from_customer_email),split(/ /,$to_customer_email));
@supplier_email = (split(/ /,$from_supplier_email),split(/ /,$to_supplier_email));
$vendor_ticket = $to_xinet_ticket_num if ($vendor_ticket ne "");
$bug_ticket_num = $to_bug_ticket_num if ($bug_ticket_num ne "");
$sth = $dbh->prepare("SELECT id FROM problems WHERE case_num = '$from'");
$sth->execute();
my $from_problem_id = $sth->fetchrow_array();
$sth = $dbh->prepare("SELECT id FROM problems WHERE case_num = '$to'");
$sth->execute();
my $to_problem_id = $sth->fetchrow_array();

insert("UPDATE problems SET customer_email = '@customer_email', supplier_email = '@supplier_email', xinet_ticket_num = '$vendor_ticket', bug_ticket_num = '$bug_ticket_num' WHERE case_num = '$to'");
insert("UPDATE problems SET assigned_to = '', status = 'Deleted', customer_email = '', supplier_email = '', xinet_ticket_num = '', bug_ticket_num = '', problem_redirect='$to' WHERE case_num = '$from'");

insert("UPDATE descriptions SET problem_id = '$to_problem_id' WHERE problem_id = '$from_problem_id'");



 my @files = File::Find::Rule->file()
 							->name('*')
 							->in("/Library/WebServer/dashboard/attachments/$from/");
 						
 foreach $file(@files)
 {
 	if ($file =~ /\/$from\//)
 	{
 		$filename = $';
 	}
 	$newdir = "/Library/WebServer/dashboard/attachments/$to";
 	$olddir = "/Library/WebServer/dashboard/attachments/$from";
 	mkdir($newdir);
 	$newfile = $newdir . "/$filename";
 	rename($file,$newfile) or die "Cannot move file:$!";
 	system("rm -r $olddir");
 }
ioiFont("Ticket # $from has been successfully appended to ticket # < a href='respondTicket.cgi&user=$user&case_num=$to'>$to</a>");
end_HTML;