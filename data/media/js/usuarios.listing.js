/* Copyright (C) 2010  Rogerio Hilbert Lima <rogerhil@gmail.com>
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


function mostraPessoa(pid, o) {
    var $cur = $(o);
    var colspan = $cur.children().length;
    var trid = 'projeto_' + pid;
    var duration = 1000;
    if (!$cur.next().hasClass('detalhes')) {
        if ($cur.hasClass('loading')) return;
        $cur.addClass('selecionada');
        $cur.addClass('loading');
        $.getJSON(pid + '.quickview.json', function (data) {
            if (data.error) {
                alert(data.error);
            } else {
                var html = '<tr class="detalhes"><td colspan="' + colspan + '">' +
                           '<div class="hidden">' + data.content +
                           '</div></td></tr>';
                var $thbef = $('<tr>');
                var $tdbef = $('<td>');
                $thbef.addClass('borderbottom');
                $tdbef.attr('colspan', colspan);
                $thbef.append($tdbef);
                $cur.after(html);
                $cur.before($thbef);
            }
            $cur.next().children().children().slideDown('slow', function(){
                $cur.removeClass('loading');    
            });
        });
    } else {
        if ($cur.hasClass('loading')) return;
        $cur.addClass('loading');
        $cur.next().children().children().slideUp('slow', function(){
            $cur.removeClass('selecionada');
            $cur.removeClass('loading');    
            $cur.next().remove();
            $cur.prev().remove();
        });
    }
    
}
