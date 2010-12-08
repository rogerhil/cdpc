/* Copyright (C) 2010  Lincoln de Sousa <lincoln@comum.org>
 * Copyright (C) 2010  Rogério Hilbert Lima <rogerhil@gmail.com>
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

function cepWebService (cep, form, prefix) {
    var cepre = /^(\d{2})\.(\d{3})-(\d{3})$/;
    var matched = cep.match(cepre);
    if (matched) {
        cep = matched[1]+matched[2]+matched[3];
        $.getJSON ('../../cadastro/consulta_cep/', {cep: cep}, function (data) {
            $(form[prefix+'_logradouro']).val (data.rua);
            $(form[prefix+'_logradouro']).focusout ();

            $(form[prefix+'_bairro']).val (data.bairro);
            $(form[prefix+'_bairro']).focusout ();

            $(form[prefix+'_cidade']).val (data.cidade);
            $(form[prefix+'_cidade']).focusout ();

            $(form[prefix+'_uf']).val (data.uf);
            $(form[prefix+'_uf']).focusout ();

            if (data.uf != "") {
                $('#'+prefix+'_numero').focus();
            }
        });

        $.getJSON ('../../cadastro/consulta_geo/', {cep: cep}, function (data) {
	        $(form[prefix+'_latitude']).val (data.lat);
	        $(form[prefix+'_longitude']).val (data.lng);
        });
    }
}

function novaEntrada ($container, prefix) {
    var $remove = $('<a href="javascript:;" class="remove">Remover</a>');
    $remove.click (function (evt) {
        var $parent = $(this).parent().parent().parent();
        //$parent.prev ().prev ().remove ();
        //$parent.prev ().remove ();
        $parent.remove ();
    });
    var $div = $('<div class="subadded">');
    var $ul = $('<ul>');
    $('<li style="margin-top: 5px;">')
        .append ($('<label>Nome</label>'))
        .append ($('<input type="text" name="' + prefix + '_nome" class="textarea large required" />'))
        .appendTo ($ul);
    $('<li>')
        .append ($('<label>Endereço </label>'))
        .append ($('<input type="text" name="' + prefix + '_link" class="textarea large required" />'))
        .appendTo ($ul);
    $('<li>')
        .append($remove)
        .addClass ('bottomBorder')
        .appendTo ($ul);
    
    $ul.appendTo($div);
    $div.appendTo($container);
}

function novoTelefone ($parent, prefix, value) {
    var $remove = $('<a href="javascript:;">Remover</a>');
    $remove.click (function (evt) {
        $(this).parent().remove();
    });
    var attrValue = '';
    if (value) {
        attrValue = ' value="' + value + '"';
    }
    var $label = $('<input type="text" name="' + prefix + '_tel"' +
                   'class="textarea phone" placeholder="(00) 0000-0000">');
    $('<li class="extra">')
        .append ($label)
        .append ($remove)
        .appendTo ($parent);
    configFields();
}
