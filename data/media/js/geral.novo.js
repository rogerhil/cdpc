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

function cepWebService (cep) {
    $.getJSON ('../../cadastro/consulta_cep/', {cep: cep}, function (data) {
        var form = $('#novoUsuario')[0];
        $(form.end_logradouro).val (data.rua);
        $(form.end_logradouro).focusout ();

        $(form.end_bairro).val (data.bairro);
        $(form.end_bairro).focusout ();

        $(form.end_cidade).val (data.cidade);
        $(form.end_cidade).focusout ();

        $(form.end_uf).val (data.uf);
        $(form.end_uf).focusout ();
    });

    $.getJSON ('../../cadastro/consulta_geo/', {cep: cep}, function (data) {
	var form = $('#novoUsuario')[0];
	$(form.end_latitude).val (data.lat);
	$(form.end_longitude).val (data.lng);
    });
}

function novaEntrada ($ul, prefix) {
    var $remove = $('<a href="javascript:;">Remover</a>');
    $remove.click (function (evt) {
        var $parent = $(this).parent ();
        $parent.prev ().prev ().remove ();
        $parent.prev ().remove ();
        $parent.remove ();
    });

    $('<li>')
        .append ($('<label>Nome</label>'))
        .append ($('<input type="text" name="' + prefix + '_nome" />'))
        .appendTo ($ul);
    $('<li>')
        .append ($('<label>Endereço </label>'))
        .append ($('<input type="text" name="' + prefix + '_link" />'))
        .appendTo ($ul);
    $('<li>')
        .append($remove)
        .addClass ('bottomBorder')
        .appendTo ($ul);
}

function novoTelefone ($parent, value) {
    var $remove = $('<a href="javascript:;">Remover</a>');
    $remove.click (function (evt) {
        $(this).parent().remove();
    });
    var attrValue = '';
    if (value) {
        attrValue = ' value="' + value + '"';
    }
    var $label = $('<input type="text" name="telefone">');
    $('<li>')
        .append ($label)
        .append ($remove)
        .addClass ('bottomBorder')
        .addClass ('extra')
        .appendTo ($parent);
}
