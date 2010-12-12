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
    var duration = 500;
    if ($tr.is(':hidden')) {
        /* Formatando a linha corrente */
        $cur.addClass('selecionada');

        /* Formatando a linha que tem os detalhes */
        if ($('.logradouro', $tr).html() == '') {
            $.getJSON(pid + '.json', function (data) {
                /* Endereço */
                $('.logradouro', $tr).html(data.endereco.logradouro);
                $('.bairro', $tr).html(data.endereco.bairro);
                $('.cidade', $tr).html(data.endereco.cidade);
                $('.uf', $tr).html(data.endereco.uf);

                /* Telefones */
                $('.telefones').html('');
                if (data.telefones.length > 0) {
                    for (var i = 0; i < data.telefones.length; i++) {
                        $('<li>')
                            .append($('<a>').html(data.telefones[i]))
                            .appendTo($('.telefones ul'));
                    }
                } else {
                    $('.telefones').hide();
                }

                /* Email e site */
                if (data.email) {
                    $('.email a', $tr)
                        .html(data.email)
                        .attr('href', 'mailto:' + data.email);
                } else {
                    $('.email').hide();
                }

                if (data.site) {
                    $('.site a', $tr)
                        .attr('href', data.site)
                        .html(data.site);
                } else {
                    $('.site').hide();
                }

                $tr.animate({opacity: '+=1', height: 'toggle'}, duration);
            });
        } else {
            $tr.animate({opacity: '+=1', height: 'toggle'}, duration);
        }
    } else {
        $cur.removeClass('selecionada');
        //$tr.fadeOut();
        $tr.animate({opacity: '-=1', height: 'toggle'}, duration);
    }
}
