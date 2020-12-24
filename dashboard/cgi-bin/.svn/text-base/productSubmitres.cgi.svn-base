#!/usr/bin/perl

################################################################################
#
#       File Name: productSubmitres.cgi
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
use CGI::Carp qw(fatalsToBrowser);
use CGI;
use DBI;
$cgi = new CGI;
my $dbh = getDBConnection();
print $cgi->header();
print $cgi->start_html();
	print"<style type='text/css'>
	<!--
	body {
	background-color: #C0C0C0;
	}
	-->
	</style>";
$prod_comp_link = $cgi->param("comp_name");
##############Fullpress###############################
$fullpress = $cgi->param("fullpress");
if ($fullpress ne "")
{
$fullpress_serial= ($cgi->param("fullpress_serial"));
$webnative_serial = $fullpress_serial;
$flashnet_serial = $fullpress_serial;
$flashweb_serial = $fullpress_serial;
$portal_serial = $fullpress_serial;
$fullpress_version = ($cgi->param("fullpress_version"));
$fullpress_os = ($cgi->param("fullpress_os"));
$fullpress_month = ($cgi->param("fullpress_month"));
$fullpress_day = ($cgi->param("fullpress_day"));
$fullpress_year = ($cgi->param("fullpress_year"));
$fullpress_options = $cgi->param(("fullpress_options"));
$fullpress_exp_month = ($cgi->param("fullpress_exp_month"));
$fullpress_exp_day = ($cgi->param("fullpress_exp_day"));
$fullpress_exp_year = ($cgi->param("fullpress_exp_year"));
if(serialCheck($fullpress_serial,$fullpress))
{
	submitProduct($fullpress,$fullpress_serial,$fullpress_version,$fullpress_os,$fullpress_month,$fullpress_day,$fullpress_year,$fullpress_options,$fullpress_exp_month,$fullpress_exp_year,$fullpress_exp_day);
}
else {	print "<center>Fullpress will not be submitted because a product with that serial number already exists.</center><p>";}

}
if ($fullpress  eq "")
{
	$sth = $dbh->prepare("Select prod_part_num from product where prod_name = 'Fullpress' and prod_comp_link = '$prod_comp_link'");
	$sth->execute();
	while (@row = $sth->fetchrow_array)
	{
		$fullpress_serial = "@row";
	}
}
############Webnative###################################
$webnative = $cgi->param("webnative");
if ($webnative ne "")
{
if ($fullpress eq "")
{
$webnative_serial = ($cgi->param("webnative_serial"));
}
$webnative_version = ($cgi->param("webnative_version")) ;
$webnative_os = ($cgi->param("webnative_os")) ;
$webnative_month = ($cgi->param("webnative_month"));
$webnative_day = ($cgi->param("webnative_day"));
$webnative_year = ($cgi->param("webnative_year"));
$webnative_options = $cgi->param(("webnative_options")) ;
$webnative_exp_month = ($cgi->param("webnative_exp_month"));
$webnative_exp_day = ($cgi->param("webnative_exp_day"));
$webnative_exp_year = ($cgi->param("webnative_exp_year"));
if (serialCheck($webnative_serial,$webnative))
{
submitProduct($webnative,$webnative_serial,$webnative_version,$webnative_os,$webnative_month,$webnative_day,$webnative_year,$webnative_options,$webnative_exp_month,$webnative_exp_year,$webnative_exp_day);
}
else {	print "<center>Webnative will not be submitted because a product with that serial number already exists.</center><p>";}


}
#############Recaster###################################
$portal = $cgi->param("portal");
if ($portal ne "")
{
if ($fullpress eq "")
{
$portal_serial = ($cgi->param("portal_serial"));
}$portal_version = ($cgi->param("portal_version")) ;
$portal_os = ($cgi->param("portal_os")) ;
$portal_month = ($cgi->param("portal_month"));
$portal_day = ($cgi->param("portal_day"));
$portal_year = ($cgi->param("portal_year"));
$portal_options = $cgi->param(("portal_options")) ;
$portal_exp_month = ($cgi->param("portal_exp_month"));
$portal_exp_day = ($cgi->param("portal_exp_day"));
$portal_exp_year = ($cgi->param("portal_exp_year"));
if (serialCheck($portal_serial,$portal))
{
submitProduct($portal,$portal_serial,$portal_version,$portal_os,$portal_month,$portal_day,$portal_year,$portal_options,$portal_exp_month,$portal_exp_year,$portal_exp_day);
}
else {	print "<center>WN Portal will not be submitted because a product with that serial number already exists.</center><p>";}

}
##############Flashnet#################################
$flashnet = $cgi->param("flashnet");
if ($flashnet ne "")
{
if ($fullpress eq "")
{
$flashnet_serial = ($cgi->param("flashnet_serial"));
}$flashnet_version = ($cgi->param("flashnet_version")) ;
$flashnet_os = ($cgi->param("flashnet_os")) ;
$flashnet_month = ($cgi->param("flashnet_month"));
$flashnet_day = ($cgi->param("flashnet_day"));
$flashnet_year = ($cgi->param("flashnet_year"));
$flashnet_options = $cgi->param(("flashnet_options")) ;
$flashnet_exp_month = ($cgi->param("flashnet_exp_month"));
$flashnet_exp_day = ($cgi->param("flashnet_exp_day"));
$flashnet_exp_year = ($cgi->param("flashnet_exp_year"));
if (serialCheck($flashnet_serial,$flashnet))
{
submitProduct($flashnet,$flashnet_serial,$flashnet_version,$flashnet_os,$flashnet_month,$flashnet_day,$flashnet_year,$flashnet_options,$flashnet_exp_month,$flashnet_exp_year,$flashnet_exp_day);
}
else {	print "<center>Flashnet will not be submitted because a product with that serial number already exists.</center><p>";}

}
$flashweb = $cgi->param("flashweb");
if ($flashweb ne "")
{
if ($fullpress eq "")
{
$flashweb_serial = ($cgi->param("flashweb_serial"));
}
$flashweb_version = ($cgi->param("flashweb_version")) ;
$flashweb_os = ($cgi->param("flashweb_os")) ;
$flashweb_month = ($cgi->param("flashweb_month"));
$flashweb_day = ($cgi->param("flashweb_day"));
$flashweb_year = ($cgi->param("flashweb_year"));
$flashweb_options = $cgi->param(("flashweb_options")) ;
$flashweb_exp_month = ($cgi->param("flashweb_exp_month"));
$flashweb_exp_day = ($cgi->param("flashweb_exp_day"));
$flashweb_exp_year = ($cgi->param("flashweb_exp_year"));
if (serialCheck($flashweb_serial,$flashweb))
{
submitProduct($flashweb,$fullpress_serial,$flashweb_version,$flashweb_os,$flashweb_month,$flashweb_day,$flashweb_year,$flashweb_options,$flashweb_exp_month,$flashweb_exp_year,$flashnet_exp_day);
}
else {	print "<center>Flashweb will not be submitted because a product with that serial number already exists.</center><p>";}

}
################IOI Support#############################
$ioi_support = $cgi->param("ioi_support");
if ($ioi_support ne "")
{
$ioi_support_serial = ($cgi->param("ioi_support_serial")) ;
$ioi_support_version = ($cgi->param("ioi_support_version")) ;
$ioi_support_os= ($cgi->param("ioi_os")) ;
$ioi_support_month = ($cgi->param("support_month"));
$ioi_support_day = ($cgi->param("support_day"));
$ioi_support_year = ($cgi->param("support_year"));
$support_options = ($cgi->param("support_options")) ;
$ioi_support_exp_day = ($cgi->param("support_exp_day"));
$ioi_support_exp_year = ($cgi->param("support_exp_year"));
$ioi_support_exp_month = ($cgi->param("support_exp_month"));

$support_options = ($cgi->param("support_options")) ;
if(duplicateCheck())
{
submitProduct($ioi_support,$ioi_support_serial,$ioi_support_version,$ioi_support_os,$ioi_support_month,$ioi_support_day,$ioi_support_year,$support_options,$ioi_support_exp_month,$ioi_support_exp_year,$ioi_support_exp_day);
}
else {print "<center>IOI Support was not submitted because this customer already has an IOI Support package"};
}
###############swing###################################
$swing = $cgi->param("swing");
if ($swing ne "")
{
$swing_serial = ($cgi->param("swing_serial")) ;
$swing_version = ($cgi->param("swing_version")) ;
$swing_os = ($cgi->param("swing_os")) ;
$swing_month = ($cgi->param("swing_month"));
$swing_day = ($cgi->param("swing_day"));
$swing_year = ($cgi->param("swing_year"));
$swing_options = $cgi->param(("swing_options")) ;
$swing_exp_month = ($cgi->param("swing_exp_month"));
$swing_exp_day = ($cgi->param("swing_exp_day"));
$swing_exp_year = ($cgi->param("swing_exp_year"));
if (optionsCheck($swing_options,$swing))
{
	submitProduct($swing,$swing_serial,$swing_version,$swing_os,$swing_month,$swing_day,$swing_year,$swing_options,$swing_exp_month,$swing_exp_year,$swing_exp_day);
}
else {	print "<center>Swing will not be submitted because a product with those options already exists.</center><p>";}

}
$twist = $cgi->param("twist");
################Twist###################################
if ($twist ne "")
{
$twist_serial = ($cgi->param("twist_serial")) ;
$twist_version = ($cgi->param("twist_version")) ;
$twist_os = ($cgi->param("twist_os")) ;
$twist_month = ($cgi->param("twist_month"));
$twist_day = ($cgi->param("twist_day"));
$twist_year = ($cgi->param("twist_year"));
$twist_options = $cgi->param(("twist_options")) ;
$twist_exp_month = ($cgi->param("twist_exp_month"));
$twist_exp_day = ($cgi->param("twist_exp_day"));
$twist_exp_year = ($cgi->param("twist_exp_year"));
if (optionsCheck($twist_options,$twist))
{
submitProduct($twist,$twist_serial,$twist_version,$twist_os,$twist_month,$twist_day,$twist_year,$twist_options,$twist_exp_month,$twist_exp_year,$twist_exp_day);
}
else {	print "<center>Twist will not be submitted because a product with those options already exists.</center><p>";}

}
################Dialogue##############################
$dialogue = $cgi->param("dialogue");
if ($dialogue ne "")
{
$dialogue_serial = ($cgi->param("dialogue_serial")) ;
$dialogue_version = ($cgi->param("dialogue_version")) ;
$dialogue_os = ($cgi->param("dialogue_os")) ;
$dialogue_month = ($cgi->param("dialogue_month"));
$dialogue_day = ($cgi->param("dialogue_day"));
$dialogue_year = ($cgi->param("dialogue_year"));
$dialogue_options = $cgi->param(("dialogue_options")) ;
$dialogue_exp_month = ($cgi->param("dialogue_exp_month"));
$dialogue_exp_day = ($cgi->param("dialogue_exp_day"));
$dialogue_exp_year = ($cgi->param("dialogue_exp_year"));
if (optionsCheck($dialogue_options,$dialogue))
{
submitProduct($dialogue,$dialogue_serial,$dialogue_version,$dialogue_os,$dialogue_month,$dialogue_day,$dialogue_year,$dialogue_options,$dialogue_exp_month,$dialogue_exp_year,$dialogue_exp_day);
}
else {	print "<center>Dialogue will not be submitted because a product with those options already exists.</center><p>";}

}
$litho = $cgi->param("litho");
if ($litho ne "")
{
$litho_serial = ($cgi->param("litho_serial")) ;
$litho_version = ($cgi->param("litho_version")) ;
$litho_os = ($cgi->param("litho_os")) ;
$litho_month = ($cgi->param("litho_month"));
$litho_day = ($cgi->param("litho_day"));
$litho_year = ($cgi->param("litho_year"));
$litho_options = $cgi->param(("litho_options")) ;
$litho_exp_month = ($cgi->param("litho_exp_month"));
$litho_exp_day = ($cgi->param("litho_exp_day"));
$litho_exp_year = ($cgi->param("litho_exp_year"));
if (optionsCheck($litho_options,$litho))
{
submitProduct($litho,$litho_serial,$litho_version,$litho_os,$litho_month,$litho_day,$litho_year,$litho_options,$litho_exp_month,$litho_exp_year,$litho_exp_day);
}
else {	print "<center>Litho will not be submitted because a product with those options already exists.</center><p>";}

}
################server LIbraries#######################
$tape_libraries = $cgi->param("tape_libraries");
if ($tape_libraries ne "")
{
$tape_serial = ($cgi->param("tape_serial")) ;
$tape_version = ($cgi->param("tape_version")) ;
$tape_os = ($cgi->param("tape_os")) ;
$tape_month = ($cgi->param("tape_month"));
$tape_day = ($cgi->param("tape_day"));
$tape_year = ($cgi->param("tape_year"));
$tape_options = $cgi->param(("tape_options"));
$tape_drives = $cgi->param("tape_drives");
$tape_slots = $cgi->param("tape_slots");
$tape_exp_month = ($cgi->param("tape_exp_month"));
$tape_exp_day = ($cgi->param("tape_exp_day"));
$tape_exp_year = ($cgi->param("tape_exp_year"));
if (serialCheck($tape_serial,$tape_libraries))
{
submitProduct($tape_libraries,$tape_serial,$tape_version,$tape_os,$tape_month,$tape_day,$tape_year,$tape_options,$tape_exp_month,$tape_exp_year,$tape_exp_day,$tape_drives,$tape_drives);
}
else { 
print "<center>Tape Library will not be submitted because a server with that serial number already exists.</center><p>";
}
}
$server = $cgi->param("server");
if ($server ne "")
{
$server_serial = ($cgi->param("server_serial")) ;
$server_version = ($cgi->param("server_version")) ;
$server_os = ($cgi->param("server_os")) ;
$server_month = ($cgi->param("server_month"));
$server_day = ($cgi->param("server_day"));
$server_year = ($cgi->param("server_year"));
$server_options = $cgi->param(("server_options")) ;
$server_exp_day = ($cgi->param("server_exp_day"));
$server_exp_month = ($cgi->param("server_exp_month"));
$server_exp_year = ($cgi->param("server_exp_year"));
$server_options = $cgi->param(("server_options")) ;
if (serialCheck($server_serial,$serial))
{
submitProduct($server,$server_serial,$server_version,$server_os,$server_month,$server_day,$server_year,$server_options,$server_exp_month,$server_exp_year,$server_exp_day);
}
else { 
print "<center>Server will not be submitted because a server with that serial number already exists.</center><p>";
}
}
$raid = $cgi->param("raid");
if ($raid ne "")
{
$raid_serial = ($cgi->param("raid_serial")) ;
$raid_version = ($cgi->param("raid_version")) ;
$raid_os = ($cgi->param("raid_os")) ;
$raid_month = ($cgi->param("raid_month"));
$raid_day = ($cgi->param("raid_day"));
$raid_year = ($cgi->param("raid_year"));
$raid_options = $cgi->param(("raid_options")) ;
$raid_exp_month = ($cgi->param("raid_exp_month"));
$raid_exp_day = ($cgi->param("raid_exp_day"));
$raid_exp_year = ($cgi->param("raid_exp_year"));
if (serialCheck($raid_serial,$raid))
{
submitProduct($raid,$raid_serial,$raid_version,$raid_os,$raid_month,$raid_day,$raid_year,$raid_options,$raid_exp_month,$raid_exp_year,$raid_exp_day);
}
else { 
print "<center>Raid will not be submitted because a server with that serial number already exists.</center><p>";
}
}
print "<center>If you want to add more products click <a href = 'productSubmit.cgi'>here</a></center>";
print $cgi->end_html;
sub getId
{
	$sth = $dbh->prepare("Select max(id_num) from product");
	$sth->execute();
	while(@row = $sth->fetchrow() )
	{
		$id_num = "@row" + 1;
	}
}
sub getCaseNum
{
	open(DAT, "/Library/WebServer/dashboard/config/case_num") || die ("Could Not Open File");
	@File=<DAT>;
	close(DAT);
	foreach $line (@File)
	{
		if ($line =~ /^(P)\s+/i)			#Gets next case number from file
		{
		$old_ticket_num =  $';
		$new_ticket_num = $old_ticket_num + 1;
		$prod_case_num = "P" . $new_ticket_num;
		$new_ticket_num = $new_ticket_num . "\n";
		}
	}
	open(DAT,">/Library/WebServer/dashboard/config/case_num");
	for(@File)
	{
		s/$old_ticket_num/$new_ticket_num/;
	}
	print DAT (@File);
	close(DAT);
}
sub duplicateCheck
{
	$sth = $dbh->prepare("Select prod_name from product where prod_name = 'IOI Support' and prod_comp_link = '$prod_comp_link'");
	$sth->execute();
	while(@row = $sth->fetchrow_array)
	{
		$check = "@row";
	}
	if ($check ne "")
	{
		return(0);
	}
	else {return(1);}
}
sub submitProduct()
{ 

my $prod_name = $dbh->quote("$_[0]");
my $prod_serial = $dbh->quote("$_[1]");
my $prod_version = $dbh->quote("$_[2]");
my $prod_oper_sys = $dbh->quote("$_[3]");
my $prod_month = $_[4]; 
my $prod_day = $_[5];
my $prod_year = $_[6];

if ($prod_month ne " " and $prod_day ne " " and $prod_year ne " ")
{
$date_prod_purchased = $prod_year . "/" . $prod_month . "/" . $prod_day;
$date_prod_purchased = $dbh->quote("$date_prod_purchased");
}
else{
	$date_prod_purchased= "";
	}
my $prod_options = $dbh->quote("$_[7]");
my $prod_exp_month = $_[8];
my $prod_exp_year = $_[9];
my $prod_exp_day = $_[10];
my $prod_drives = $dbh->quote($_[11]);
my $prod_slots = $dbh->quote($_[12]) ;
if ($prod_exp_month ne " " and $prod_exp_day ne " " and $prod_exp_year ne " ")
{
	$prod_maint_exp = $prod_exp_year . "/" . $prod_exp_month . "/" . $prod_exp_day;
	$prod_maint_exp = $dbh->quote("$prod_maint_exp");
}
else {$prod_maint_exp = "";}

$prod_comp_link = $dbh->quote("$prod_comp_link");
getId();
getCaseNum();
$prod_case_num = $dbh->quote("$prod_case_num");
$id_num = $dbh->quote("$id_num");
if ($date_prod_purchased ne "" and $prod_maint_exp eq "")
{
	$statement ="Insert into product 
	(id_num,prod_case_num,prod_comp_link, prod_name, prod_version, prod_oper_sys, date_prod_purchased, prod_part_num, prod_status,sub_prod_name,prod_drive_num,prod_slot_num)
	values ($id_num,$prod_case_num,$prod_comp_link, $prod_name, $prod_version, $prod_oper_sys, $date_prod_purchased, $prod_serial, 'Active',$prod_options,$prod_drives,$prod_slots)";
}
elsif ($date_prod_purchased eq "" and $prod_maint_exp eq "")
{
	$statement ="Insert into product 
	(id_num,prod_case_num,prod_comp_link, prod_name, prod_version, prod_oper_sys, prod_part_num, prod_status,sub_prod_name,prod_drive_num,prod_slot_num)
	values ($id_num,$prod_case_num,$prod_comp_link, $prod_name, $prod_version, $prod_oper_sys, $prod_serial, 'Active',$prod_options,$prod_drives,$prod_slots)";
}
elsif ($date_prod_purchased eq "" and $prod_maint_exp ne "")
{
	$statement ="Insert into product 
	(id_num,prod_case_num,prod_comp_link, prod_name, prod_version, prod_oper_sys, prod_maint_exp, prod_part_num, prod_status,sub_prod_name,prod_drive_num,prod_slot_num)
	values ($id_num,$prod_case_num,$prod_comp_link, $prod_name, $prod_version, $prod_oper_sys, $prod_maint_exp, $prod_serial, 'Active',$prod_options,$prod_drives,$prod_slots)";
}
elsif ($date_prod_purchased ne "" and $prod_maint_exp ne "")
{
	$statement ="Insert into product 
	(id_num,prod_case_num,prod_comp_link, prod_name, prod_version, prod_oper_sys, date_prod_purchased, prod_part_num, prod_status,sub_prod_name,prod_maint_exp,prod_drive_num,prod_slot_num)
	values ($id_num,$prod_case_num,$prod_comp_link, $prod_name, $prod_version, $prod_oper_sys, $date_prod_purchased, $prod_serial, 'Active',$prod_options,$prod_maint_exp,$prod_drives,$prod_slots)";
}

$sth= $dbh->prepare($statement);
$sth->execute();
$dbh->commit();
print "<center>$prod_name has been submitted successfully. <p></center>";
 $prod_name="";
 $prod_version="";
 $prod_oper_sys="";
 $prod_po="";
 $date_prod_purchased="";
 $prod_invoice="";
 $xinet_users="";
 $prod_part_num="";
 $prod_case_num="";
$id_num;
$prod_comp_link = $cgi->param("comp_name");

}
sub optionsCheck
{
	$options = $_[0];
	$prod_name = $_[1];
	$options = $dbh->quote($options);
	$prod_name = $dbh->quote($prod_name);
	$comp_case_num = $dbh->quote($prod_comp_link);
	$sth = $dbh->prepare("select sub_prod_name from product where sub_prod_name = $options and prod_name = $prod_name and prod_comp_link = $comp_case_num");
	$comp_case_num = "";
	$sth->execute();
	while (@row = $sth->fetchrow_array)
	{
		$check = "@row";
	}
	if ($check ne "")
	{
		return(0);
	}
	else {return(1);}
	
}
sub serialCheck
{
	$serial = $_[0];
	$prod_name = $_[1];
	$prod_name = $dbh->quote($prod_name);
	$serial = $dbh->quote($serial);
	$sth = $dbh->prepare("select prod_part_num from product where prod_part_num = $serial and prod_name = $prod_name");
	$sth->execute();
	while (@row = $sth->fetchrow_array)
	{
		$check = "@row";
		print "$check";
	}
	if ($check ne "")
	{
		return(0);
	}
	else {return(1);}
 }