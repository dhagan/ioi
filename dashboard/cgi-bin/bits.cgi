#!/usr/bin/perl

################################################################################
#
#       File Name: bits.cgi
#
#       Purpose: This file is used for calculating between different orders of bits/bytes
#
#       Copyright © 2007 IOIntegration Inc. Internal use only.
#
#       Revision History:
#
#       Date            Author          Action
#       ----            ------          ------
#       06/11/2007      B. Scarborough  Created this file
#
################################################################################

use CGI;
$cgi = new CGI;

print $cgi->header();
print $cgi->start_html(-title=>'IO Integration');
print "
    <body>
         <script type='text/javascript' language='javascript'>
            function calculate() {
                var amt = document.getElementById('amt').value;
                var units = document.getElementById('units').selectedIndex;

                document.getElementById('bit').innerHTML = calculateAmt(0, units, amt);
                document.getElementById('B').innerHTML = calculateAmt(1, units, amt);
                document.getElementById('Kbit').innerHTML = calculateAmt(2, units, amt);
                document.getElementById('KB').innerHTML = calculateAmt(3, units, amt);
                document.getElementById('Mbit').innerHTML = calculateAmt(4, units, amt);
                document.getElementById('MB').innerHTML = calculateAmt(5, units, amt);
                document.getElementById('Gbit').innerHTML = calculateAmt(6, units, amt);
                document.getElementById('GB').innerHTML = calculateAmt(7, units, amt);
                document.getElementById('Tbit').innerHTML = calculateAmt(8, units, amt);
                document.getElementById('TB').innerHTML = calculateAmt(9, units, amt);
                document.getElementById('Pbit').innerHTML = calculateAmt(10, units, amt);
                document.getElementById('PB').innerHTML = calculateAmt(11, units, amt);
            }
            function calculateAmt (index, units, amt) {
                var bits_in_byte = 8;
                var kilo = 1024;
                if (units == index) {
                    return amt;
                } else if (units > index) {
                    var diff = units - index;
                    
                    var mod = 1;
                    if (diff % 2 != 0) {
                        mod = bits_in_byte;
                    }
                    
                    var mul = Math.ceil(diff / 2);
                    mul = Math.pow(kilo, mul);
                    
                    amt = amt / mod * mul;
                    return amt;
                } else {
                    var diff = index - units;
                    
                    var mod = 1;
                    if (diff % 2 != 0) {
                        mod = bits_in_byte;
                    }
                    
                    var mul = Math.floor(diff / 2);
                    mul = Math.pow(kilo, mul);
                    
                    amt = amt / mod / mul;
                    return amt;
                }
            }
        </script>
        <b>Enter the amount and units below, then select \"Calculate\".</b><br />
        Amount: <input type='text' name='amt' id='amt' /> Units:
        <select name='units' id='units'>
            <option value='bit'>bits</option>
            <option value='B'>Bytes</option>
            <option value='Kbit'>Kilobits</option>
            <option value='KB'>KiloBytes</option>
            <option value='Mbit'>Megabits</option>
            <option value='MB'>MegaBytes</option>
            <option value='Gbit'>Gigabits</option>
            <option value='GB'>GigaBytes</option>
            <option value='Tbit'>Terabits</option>
            <option value='TB'>TeraBytes</option>
            <option value='Pbit'>Petabits</option>
            <option value='PB'>PetaBytes</option>
        </select>
        <input type='button' onclick='calculate()' value='Calculate' />
        <br />
        <br />
        <table border='1' rules='rows'>
            <tr>
                <td id='bit' style='width:175px'></td><td style='width:50px'>bits</td>
            </tr/>
            <tr>
                <td id='B'></td><td>Bytes</td>
            </tr/>
            <tr>
                <td id='Kbit'></td><td>Kilobits</td>
            </tr/>
            <tr>
                <td id='KB'></td><td>KiloBytes</td>
            </tr/>
            <tr>
                <td id='Mbit'></td><td>Megabits</td>
            </tr/>
            <tr>
                <td id='MB'></td><td>MegaBytes</td>
            </tr/>
            <tr>
                <td id='Gbit'></td><td>Gigabits</td>
            </tr/>
            <tr>
                <td id='GB'></td><td>GigaBytes</td>
            </tr/>
            <tr>
                <td id='Tbit'></td><td>Terabits</td>
            </tr/>
            <tr>
                <td id='TB'></td><td>TeraBytes</td>
            </tr/>
            <tr>
                <td id='Pbit'></td><td>Petabits</td>
            </tr/>
            <tr>
                <td id='PB'></td><td>PetaBytes</td>
            </tr/>
        </table>
    </body>";
print $cgi->end_html();