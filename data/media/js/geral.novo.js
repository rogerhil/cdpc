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
        $(form.end_bairro).val (data.bairro);
        $(form.end_cidade).val (data.cidade);
        $(form.end_uf).val (data.uf);
    });

    $.getJSON ('../../cadastro/consulta_geo/', {cep: cep}, function (data) {
	var form = $('#novoUsuario')[0];
	$(form.end_latitude).val (data.lat);
	$(form.end_longitude).val (data.lng);
    });
}

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

function novoTelefone ($parent) {
    var $remove = $('<a href="javascript:;">Remover</a>');
    $remove.click (function (evt) {
        $(this).parent().remove()
    });

    var $label = $('<label>' +
        '<span>Telefone</span>' +
        '<input type="text" name="telefone">' +
        '</label>');
    $('<li>')
        .append ($label)
        .append ($remove)
        .addClass ('bottomBorder')
        .appendTo ($parent);
}
