/* Copyright (C) 2010  Rogério Hilbert Lima <rogerhil@gmail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

if (typeof(String.prototype.strip) === "undefined") {
    String.prototype.trim = function () {
        return String(this).replace(/^\s+|\s+$/g, '');
    };
}

function minimun(l) {
    var aux = l[0];
    for (var k = 0; k < l.length; k++) {
        if (l[k] < aux) {
            aux = l[k];
        }
    }
    return aux;
}

function startWaitCursor() {
    var $loadcursor = $('<div class="loadcursor" id="loadcursor">');
    $($("body")[0]).append($loadcursor); 
    $(document).bind('mousemove',function(e){ 
        $loadcursor.css("left", Number(e.pageX) + 12 + 'px');
        $loadcursor.css("top", Number(e.pageY) + 8 + 'px');
    });
}

function stopWaitCursor() {
    $(document).unbind('mousemove');
    $('#loadcursor').remove();
}

function overlay(v) {
    if (v == 'hide') {
        $.ui.dialog.overlay.destroy($.ui.dialog.overlay.instances[0]);
        $("div#ajaxsplash").hide();
    } else {
        $.ui.dialog.overlay();
        $("div#ajaxsplash").show();
    }
}

function start() {
    
    // config buttons
    $('div.btcontent').hover(function () {
        $(this).prev().css('opacity', 0.7);
        $(this).next().css('opacity', 0.7);
    }, function () {
        $(this).prev().css('opacity', 1);
        $(this).next().css('opacity', 1);
    });
}

$(document).ready(start);
