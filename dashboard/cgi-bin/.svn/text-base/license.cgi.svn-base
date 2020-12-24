#!/usr/bin/perl

################################################################################
#
#       File Name: license.cgi
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

#IOI License Generator
use CGI;
use strict;
use Crypt::Lite;


if (param('getLicense'))
{
	getLicense();
}
elsif(param('getDemoLicense'))
{
	getDemoLicense();
}
else
{
	licenseForm();
}

sub licenseForm()
{
	print header();
}




sub getLicense()
{
	my $xinet_license = `/usr/etc/appletalk/atlic`;
	my $hardware_id = $1 if ($xinet_license =~ /The ID for this machine is:  (.*?)\n/);	
	my $ioistring = "~12.,>¿öÆµú©Ã";
	my $license_string = crypt($ioistring,$hardware_id);
	return $license_string;
}
sub getDemoLicense()
{
	my $crypt = Crypt::Lite->new(debug=>0);
	(my $sec,my $min,my $hour,my $mday,my $mon,my $year,my $wday,my $yday,my $isdst) =localtime(time);
	$mon+= 2;
	$year +=1900;
	my $demoString = '#)).e3a]=/';
	my $dateString = "Demo$year$mon$mday";
	print $dateString , "\n";
	return $crypt->encrypt($dateString,$demoString);
}