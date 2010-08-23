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

function novoEndereco () {
    var $newElement = $($('div.formEndereco')[0].cloneNode (true));
    $('input, select', $newElement).val ('');

    var $remove = $('<a href="javascript:;">Remover</a>');
    $remove.click (function (evt) {
        $newElement.remove ();
    });

    $('*', $newElement).removeClass ('bottomBorder');

    $('<li>')
        .addClass ('subForm')
        .append ($newElement)
        .appendTo ($('ul.enderecos'));
    $('<li>')
        .append($remove)
        .addClass ('bottomBorder')
        .appendTo ($('ul', $newElement));

    atualizarEnderecos ();
}

function atualizarEnderecos () {
    var $select = $('select[name=local_projeto]');
    var selected = $select.val ();
    $('option', $select).each (function () {
        if ($(this).val () != '' &&
            $(this).val () != 'itinerante') {
            $(this).remove()
        }
    });
    $('div.formEndereco').each (function () {
        var $div = $(this);
        var nome = $('input[name=end_nome]', $div).val ();
        if (nome != '') {
            var $opt = $('<option>')
                .val(nome)
                .html(nome)
                .attr('value', nome)
                .appendTo($select);
            if (nome == selected)
                $opt.attr('selected', 'selected');
        }
    });
}
