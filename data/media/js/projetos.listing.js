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

function showProject(pid, line) {
    var $cur = $(line);
    var $tr = $(line).next();

    if ($tr.css('display') == 'none') {
        /* Formatando a linha corrente */
        $cur.addClass('selecionada');

        /* Formatando a linha que tem os detalhes */
        if ($('.logradouro', $tr).html() == '') {
            $.getJSON(pid + '.json', function (data) {
                $('.logradouro', $tr).html(data.endereco.logradouro);
                $('.bairro', $tr).html(data.endereco.bairro);
                $('.cidade', $tr).html(data.endereco.cidade);
                $('.uf', $tr).html(data.endereco.uf);
                $tr.fadeIn('slow');
            });
        } else {
            $tr.fadeIn('slow');
        }
    } else {
        $cur.removeClass('selecionada');
        $tr.fadeOut();
    }
}
