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
    if (ERRORS_LIST) {
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

