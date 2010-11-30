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


String.prototype.capitalize = function(){
    return this.replace(/(^|\s)([a-z])/g,
                        function(m,p1,p2){return p1+p2.toUpperCase();});
};

var load = function () {
    if (this.checked || this.selected) $(this).change();
};

function loadLocalizacaoGeoProjeto() {
    $('#local_proj').change(function () {
        if ($(this).val () == 'outros') {
            $('#local_proj_outros').show ();
        } else {
            $('#local_proj_outros').hide ();
        }
    });
    $('#local_proj').change();
}

function loadComunicacaoCulturaDigital() {
    $("input[name=sede_possui_tel]").change(function () {
        if ($(this).val () == 'sim') {
   
            $('#sede_possui_tel_sim').show ();

            $('#sede_possui_tel_nao').hide ();
        }
        else if ($(this).val () == 'nao') {

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

    $("input[name=sede_possui_tel]").each(load);
    $("input[name=sede_possui_net]").each(load);
    
    var change = function (id) {
        if ($('#'+id).val () == 'outro') {
            $('#' + id + '_outro_escolhido').show ();
        } else {
            $('#' + id + '_outro_escolhido').hide ();
        }
    
    }
    change('pq_sem_tel');
    change('pq_sem_internet');

}

function loadEntidadeProponente() {
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

    $("input[name=endereco_ent_proj]").each(load);
    $("input[name=convenio_ent]").each(load);

}

function loadParceriasProjeto() {
    $("input[name=estabeleceu_parcerias]").change(function () {
        if ($(this).val () == 'sim') {
            $('#parcerias_sim').show ();
        } else {
            $('#parcerias_sim').hide ();
        }
    });
    $("input[name=estabeleceu_parcerias]").each(load);
}

function loadAtividadesExercidasProjeto() {
    $("input[name=participa_cultura_viva]").change(function () {
        if ($(this).val () == 'sim') {
            $('#participa_cultura_viva_sim').show ();
        } else {
            $('#participa_cultura_viva_sim').hide ();
        }
    });
    $("input[name=participa_cultura_viva]").each(load);
}

$(document).ready (function () {
    /*
    $('#novoProjeto').validate({
        debug: true,
        invalidHandler: function (form, validator) {
            var errors = validator.numberOfInvalids();
            if (errors) {
                alert (errors);
                return false;
            }
        }
    });
    */

    loadLocalizacaoGeoProjeto();
    loadComunicacaoCulturaDigital();
    loadEntidadeProponente();
    loadParceriasProjeto();
    loadAtividadesExercidasProjeto();

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
    var $newElement = $($('div.formEndereco')[1].cloneNode (true));
    $('input, select', $newElement).val ('');
    $('.error-message', $newElement).remove();
    $('.error', $newElement).removeClass('error');

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
                .appendTo($select);
            $opt.val(nome);
            $opt.attr('value', nome)
            $opt.html(nome)
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
        '<input type="text" name="outro_convenio" ' +
        '       placeholder="Ex.: Pontão Vila Pangéia"/>' +
        '</label>');
    $('<li>')
        .append ($label)
        .append ($remove)
        .addClass ('bottomBorder')
        .appendTo ($parent);
}

function novoParceiro ($parent) {
    var $remove = $('<a href="javascript:;">Remover</a>');
    $remove.click (function (evt) {
        $(this).parent().remove();
    });

    var $label = $('<label>' +
        '<span>Nome do Parceiro</span>' +
        '<input type="text" name="parcerias" placeholder="Ex.: Sesc São Carlos"/>' +
        '</label>');
    $('<li>')
        .append ($label)
        .append ($remove)
        .addClass ('bottomBorder')
        .appendTo ($parent);
}

function preencherCamposLista(values, errors) {
    var thee, thev;

    for (var key in values) {
        thev = values[key];
        $('input[name=' + key + ']').each(function () {
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
                 'proj_tel': novoTelefone,
                 'ent_tel': novoTelefone,
                 'end_outro_bairro': novoEndereco};
    var blocksSet = {'rs_nome': $('#redesSociais'),
                     'feed_nome': $('#feeds'),
                     'proj_tel': $('#proj_tel'),
                     'ent_tel': $('#ent_tel'),
                     'end_proj_complemento': $('#localizacaoGeoProjetoSection')};
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

function proximo() {
    var current = $("#"+currentTab);
    var next = current.next();
    var children = current.children();
    var theForm = $("<form></form>").append(children);
    var success = function (data) {

        if (data.error) {
             current.html($(data.html).children());
            try {
                eval("load" + currentTab.capitalize() + "()");
            } catch (e) {
            
            }
            novosCamposLista(data.values_list);
            preencherCamposLista(data.values_list, data.errors_list);
        } else {
            current.append(children);
            try {
                eval("load" + currentTab.capitalize() + "()");
            } catch (e) {
            
            }
            $('.error-message', current).remove();
            $('.error', current).removeClass('error');
            currentTab = next[0].id;
            current.css("display", "none");
            next.css("display", "block");
            $("#botaoAnterior").css("display", "inline");
            if (currentTab == fim) {
                $("#botaoProximo").css("display", "none");
                $("#submitButton").css("display", "inline");
            }
        }
    }
    var options = {
        success: success,
        url: "/projetos/validar/",
        type: 'post',
        data: {'step_name': current[0].id},
        dataType:  'json'
        //target:        '#output1',   // target element(s) to be updated with server response
        //beforeSubmit:  showRequest,  // pre-submit callback
        //clearForm: true        // clear all form fields after successful submit
        //resetForm: true        // reset the form after successful submit
        // $.ajax options can be used here too, for example:
        //timeout:   3000
    };

    theForm.find("input[type=file]").each( function () {
        this.type = 'text';
    });
    theForm.ajaxSubmit(options);
}

function anterior() {
    var current = $("#"+currentTab);
    var previous = current.prev();
    current.css("display", "none");
    $("#submitButton").css("display", "none");
    currentTab = previous[0].id;
    previous.css("display", "block");
    $("#botaoProximo").css("display", "inline");
    if (currentTab == inicio) {
        $("#botaoAnterior").css("display", "none");
    }
}
