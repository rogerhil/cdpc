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
    VALIDATOR = $('#novoUsuario').validate();
    configFields();
});

function configFields() {
    decorateRequiredLabels();
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



