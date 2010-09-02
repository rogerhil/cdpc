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
        if ($(this).val () == 'nao') {
            $('#endereco_ent_proj_nao').show ();
        } else {
            $('#endereco_ent_proj_nao').hide ();
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

    $("input[name=parcerias]").change(function () {
        if ($(this).val () == 'sim') {
            $('#parcerias_sim').show ();
        } else {
            $('#parcerias_sim').hide ();
        }
    });

    $('#pq_sem_tel').change(function () {
        if ($(this).val () == 'outro') {
            $('#pq_sem_tel_outro_escolhido').show ();
        } else {
            $('#pq_sem_tel_outro_escolhido').hide ();
        }
    });

    $('#pq_sem_internet').change(function () {
        if ($(this).val () == 'outro') {
            $('#pq_sem_internet_outro_escolhido').show ();
        } else {
            $('#pq_sem_internet_outro_escolhido').hide ();
        }
    });

    $('input[name=outras_atividades]').change(function () {
        if ($(this).is (':checked')) {
            $('#outras_atividades_escolhido').show ();
        } else {
            $('#outras_atividades_escolhido').hide ();
        }
    });

    $('input[name=outras_culturas]').change(function () {
        if ($(this).is (':checked')) {
            $('#outras_culturas_escolhido').show ();
        } else {
            $('#outras_culturas_escolhido').hide ();
        }
    });

    $('input[name=outra_ocupacao]').change(function () {
        if ($(this).is (':checked')) {
            $('#outra_ocupacao_escolhido').show ();
        } else {
            $('#outra_ocupacao_escolhido').hide ();
        }
    });

    $('input[name=outras_manifestacoes]').change(function () {
        if ($(this).is (':checked')) {
            $('#outras_manifestacoes_escolhido').show ();
        } else {
            $('#outras_manifestacoes_escolhido').hide ();
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
            $(this).remove();
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

function novaDocumentacao ($parent) {
    var $remove = $('<a href="javascript:;">Remover</a>');
    $remove.click (function (evt) {
        $(this).parent().remove();
    });

    var $label = $('<label>' +
        'Upload de <b>Plano de trabalho e documentações do Projeto</b>' +
        '<input type="file" name="documentacoes"/>' +
        '</label>');
    $('<li>')
        .append ($label)
        .append ($remove)
        .addClass ('bottomBorder')
        .appendTo ($parent);
}

function novoConvenio ($parent) {
    var $remove = $('<a href="javascript:;">Remover</a>');
    $remove.click (function (evt) {
        $(this).parent().remove();
    });

    var $label = $('<label>' +
        'Qual?' +
        '<input type="text" name="outro_convenio" placeholder="Ex.: Pontão Vila Pangéia"/>' +
        '</label>');
    $('<li>')
        .append ($label)
        .append ($remove)
        .addClass ('bottomBorder')
        .appendTo ($parent);
}
