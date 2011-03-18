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

var VALIDATOR;

$(document).ready (function () {
    if (ERRORS_LIST || VALUES_LIST) {
        novosCamposLista(VALUES_LIST);
        preencherCamposLista(VALUES_LIST, ERRORS_LIST);
    }
    VALIDATOR = $('#novoUsuario').validate();
    configFields();
});

function configFields() {
    decorateRequiredLabels('novoUsuario');
    supportsPlaceholder();
    $('input.cpf').unmask();
    $('input.phone').unmask();
    $('input.cep').unmask();
    $('input.data').unmask();
    $('input.cpf').mask('999.999.999-99');
    $('input.phone').mask('(99) 9999-9999');
    $('input.cep').mask('99.999-999');
    $('input.data').mask('99/99/9999');
}

function submit() {
    var valid;
    clearPlaceholders();
    valid = VALIDATOR.form();
    //valid = true;
    if (valid) {
        document.getElementById('novoUsuario').submit();
    } else {
        $('html, body').animate({scrollTop: 0}, 'slow');
    }
}

function preencherCamposLista(values, errors) {
    var thee, thev;

    for (var key in values) {
        thev = values[key];
        $('input[name=' + key + ']').each(function () {
            $(this).val(thev.splice(0,1));
        });
        $('select[name=' + key + ']').each(function () {
            $(this).val(thev.splice(0,1));
        });
    }
    
    if (!errors) return;
    
    for (var key in errors) {
        $('input[name=' + key + ']').each(function () {
            thee = errors[key].splice(0,1);
            if (thee != '') {
                $(this).addClass("error");
                $('<div class="error-message">' + thee + '</div>').insertAfter($(this));
            }
        });
    }
}

function novosCamposLista(values) {
    var funcs = {'rs_nome': novaEntrada,
                 'feed_nome': novaEntrada,
                 'pessoa_tel': novoTelefone};
    var blocksSet = {'rs_nome': $('#redesSociais'),
                     'feed_nome': $('#feeds'),
                     'pessoa_tel': $('#pessoa_tel')};
    var items;
    for (var id in values) {
        items = values[id];
        for (var k = 0; k < items.length; k++) {
            if (k < 1) continue;
            if (funcs[id]) {
                funcs[id](blocksSet[id], id.split('_')[0]);
            }
        }
    }
}

function makeErrorField(id, msg) {
    var label = '<label id="' + id + '" class="error">' + msg + '</label>';
    return $(label).css('', '');
}

function trocarSenha(o) {
    var $par = $(o).parent();
    var url = '/usuarios/meusdados/trocarsenha/trocarsenha.json';
    var data = {senha_antiga: $('input[name=senha_antiga]').val(),
                senha_nova: $('input[name=trocar_senha]').val(),
                confirmar_senha: $('input[name=confirmar_trocar_senha]').val()};
    var err, elid, msg;
    var errid = 'erro-trocar-senhar';
    var suc = '<span id="success_msg">Senha modificada com sucesso.</span>'
    function success(rdata) {
        $('input[name=senha_antiga]').removeClass('error');
        $('input[name=trocar_senha]').removeClass('error');
        $('input[name=confirmar_trocar_senha]').removeClass('error');
        if (!rdata.success) {
            elid = rdata.msg[0];
            msg = rdata.msg[1];
            err = makeErrorField(errid, msg);
            $('#' + errid).remove();
            $('#' + elid).before(err);
            $('#' + elid).addClass('error');
        } else {
            $('#' + errid).remove();
            toogleSingle(false, $('#bloco_trocar_senha'));
            $('input[name=senha_antiga]').val('');
            $('input[name=trocar_senha]').val('');
            $('input[name=confirmar_trocar_senha]').val('');
            suc = $(suc).css('color', '#9ACB44').css('font-size', '14px');
            $('#bloco_trocar_senha').parent().append(suc);
        }
    }
    $.post(url, data, success, 'json');
}

