/* Copyright (C) 2010  Lincoln de Sousa <lincoln@comum.org>
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

function novaEntrada ($ul) {
    var $remove = $('<a href="javascript:;">Remover</a>');
    $remove.click (function (evt) {
        var $parent = $(this).parent ();
        $parent.prev ().prev ().remove ();
        $parent.prev ().remove ();
        $parent.remove ();
    });

    $('<li>')
        .append ($('<label>Nome</label>'))
        .append ($('<input type="text" name="rs_nome">'))
        .appendTo ($ul);
    $('<li>')
        .append ($('<label>Endereço</label>'))
        .append ($('<input type="text" name="rs_link">'))
        .appendTo ($ul);
    $('<li>')
        .append($remove)
        .addClass ('bottomBorder')
        .appendTo ($ul);
}
