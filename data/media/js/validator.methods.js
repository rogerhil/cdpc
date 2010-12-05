/* Copyright (C) 2010  Rogério Hilbert Lima <rogerhil@gmail.com>
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

$.extend($.validator.messages, {
    required: "Campo obrigatório",
    email: "Formato de e-mail inválido",
    cep: "Formato de CEP inválido"
});

function cepMethod(value, element) {
    var cepre = /^(\d{2})\.(\d{3})-(\d{3})$/;
    var matched = value.match(cepre);
    if (matched) {
        return true;
    }
    return false;
}

$.validator.addMethod("cep", cepMethod);


    

