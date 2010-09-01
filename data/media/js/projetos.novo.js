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

$(document).ready (function () {
    $('#local_proj').change(function () {
        if ($(this).val () == 'outros') {
            $('#local_proj_outros').show ();
        } else {
            $('#local_proj_outros').hide ();
        }
    });

    $("input[name=sede_possui_tel]").change(function () {
        if ($(this).val () == 'sim') {
            $('#sede_possui_tel_sim').show ();
            $('#sede_possui_tel_nao').hide ();
        }
        else if (
            $(this).val () == 'nao') {
            $('#sede_possui_tel_nao').show ();
            $('#sede_possui_tel_sim').hide ();
        }
        else {
            $('#sede_possui_tel_sim').hide ();
            $('#sede_possui_tel_nao').hide ();
        }
    });

    $("input[name=sede_possui_net]").change(function () {
        if ($(this).val () == 'sim') {
            $('#sede_possui_net_sim').show ();
            $('#sede_possui_net_nao').hide ();
        }
        else if (
            $(this).val () == 'nao') {
            $('#sede_possui_net_nao').show ();
            $('#sede_possui_net_sim').hide ();
        }
        else {
            $('#sede_possui_net_sim').hide ();
            $('#sede_possui_net_nao').hide ();
        }
    });

    $("input[name=endereco_ent_proj]").change(function () {
        if ($(this).val () == 'sim') {
            $('#endereco_ent_proj_sim').show ();
        } else {
            $('#endereco_ent_proj_sim').hide ();
        }
    });

    $("input[name=convenio_ent]").change(function () {
        if ($(this).val () == 'sim') {
            $('#convenio_ent_sim').show ();
        } else {
            $('#convenio_ent_sim').hide ();
        }
    });

    $("input[name=participa_cultura_viva]").change(function () {
        if ($(this).val () == 'sim') {
            $('#participa_cultura_viva_sim').show ();
        } else {
            $('#participa_cultura_viva_sim').hide ();
        }
    });
});

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
