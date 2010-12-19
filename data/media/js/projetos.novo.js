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


String.prototype.capitalize = function(){
    return this.replace(/(^|\s)([a-z])/g,
                        function(m,p1,p2){return p1+p2.toUpperCase();});
};

var load = function () {
    if (this.checked || this.selected) $(this).change();
};

var VALIDATOR, CURRENT_STEP;

function carregar () {
    if ($('body.project_register').length == 0) return;
    verifyStepErrors();
    CURRENT_STEP = $('input[name=step]').val();
    configValidator();
    createStepButtons();
    configStepButtons();
    configFields();
}

function verifyStepErrors() {
    var steps = ['dadosProjeto', 'localizacaoGeoProjeto', 'entidadeProponente',
                 'comunicacaoCulturaDigital', 'atividadesExercidasProjeto',
                 'publico', 'indiceAcessoCultura'];
    var first = true;
    var someError = false;
    for (var k = 0; k < steps.length; k++) {
        var errors = $('.error:not(label)', '#' + steps[k]).length;

        if (errors) {
            someError = true;
            $('.' + steps[k], '#headsteps').addClass('steperrors');
            if (first) {
                $('.' + steps[k], '#headsteps').addClass('active');
                $('input[name=step]').val(steps[k]);
                first = false;
            }
        }
    }
    if (someError) {
        $('<div class="site-message error">Existem erros nos passos do formulário ' + 
          'indicados em vermelho.</div>').insertBefore($('#novoProjeto'));
    }
}

function clearStep(id) {
    $('.' + id, '#headsteps').removeClass('steperrors');
}

function configValidator() {
    var rules = {parcerias: {atLeastOne: true},
                 acao_cultura_viva: {atLeastOne: true},
                 atividade: {atLeastOne: true}};
    VALIDATOR = $('#content form').validate({rules: rules, debug: true});
}

function configStepButtons() {
    if ($('div#' + CURRENT_STEP).prev().length) {
        $('div.step div.buttons a.previous').show();
    } else {
        $('div.step div.buttons a.previous').hide();
    }
    if ($('div#' + CURRENT_STEP).next().length) {
        $('div.step div.buttons a.next').show();
        $('div.step div.buttons a.cadastrar').hide();
    } else {
        $('div.step div.buttons a.next').hide();
        $('div.step div.buttons a.cadastrar').show();
    }
}

function createStepButtons() {
    var prev = $('<a href="#">').addClass('previous').text('Voltar');
    var nex = $('<a href="#">').addClass('next').text('Próximo');
    var cadastrar = $('<a href="#">').addClass('cadastrar').text('Cadastrar');
    $('div.step').hide()
    $('div.step div.buttons').append(prev);
    $('div.step div.buttons').append(nex);
    $('div.step div.buttons').append(cadastrar);
    cadastrar.hide();
    $('#project_index').show();
    $('div#' + CURRENT_STEP).show();
    $('ul.steps li.active').removeClass('active');
    $('ul.steps li.' + CURRENT_STEP).addClass('active');

    $('div#' + CURRENT_STEP + "Tip").removeClass('hidden');

    $('div.step div.buttons a.next').click(next);
    $('div.step div.buttons a.previous').click(previous);
    $('div.step div.buttons a.cadastrar').click(submit);
}

function configFields() {
    supportsPlaceholder();
    $('input.cep').unmask();
    $('input.phone').unmask();
    $('input.cep').mask('99.999-999');
    $('input.phone').mask('(99) 9999-9999');
}

function validateStep() {

    var valid = true;
    var selector = "div#" + CURRENT_STEP + " input, " +
                   "div#" + CURRENT_STEP + " select, " +
                   "div#" + CURRENT_STEP + " textarea";

    $(selector).each(function () {
        var ret = false;
        // Não validar campos que estão escondidos
        $(this).parents().each(function () {
            if ($(this).is(':hidden')) ret = true;
        });
        if (ret) return;
        if (VALIDATOR.element($(this)) == false) valid = false;
    });
    return valid;
}

function next(e) {
    var current = $("div#" + CURRENT_STEP);
    var next = current.next();
    var next_step = next.attr('id');
    var children, theForm;
    
    function afterServerValidation(data) {
        var current = $("div#" + CURRENT_STEP);
        $("div#ajaxsplash").fadeOut('fast');
        if (data.error) {

            current.html($(data.html).children());
            try {
                eval("load" + CURRENT_STEP.capitalize() + "()");
            } catch (e) {
                alert(e);
            }
            novosCamposLista(data.values_list);
            preencherCamposLista(data.values_list, data.errors_list);
            configFields();
        } else {
            
            current.append(children);
                        
            $('label[generated=true]', current).remove();
            $('.error', current).removeClass('error');
            children.find("input[type=pseudofile]").each( function () {
                var $inpfile = $('input[name=' + this.name + ']', '#fileaux');
                $inpfile.insertAfter($(this));
                $(this).remove();
            });
            
            $('div#' + CURRENT_STEP).fadeOut('fast', function() {
                $('div#' + next_step).fadeIn('fast');
                $('ul.steps li.active').removeClass('active');
                $('ul.steps li.' + next_step).addClass('active');
                $('input[name=step]').val(next_step);
                $('div#' + CURRENT_STEP + "Tip").addClass('hidden');
                $('div#' + next_step + "Tip").removeClass('hidden');
                clearStep(CURRENT_STEP);
                CURRENT_STEP = next_step;
                configStepButtons();
                configFields();
            });
        }
        configValidator();
    }
 
    var options = {
        success: afterServerValidation,
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
    clearPlaceholders();
    var valid = validateStep();
            
    // COMENTE A LINHA ABAIXO PARA DEBUGAR A VALIDACAO DO SERVIDOR
    //var valid = true;
    
    if (valid) {
        children = current.children();
        theForm = $("<form></form>").append(children);
        theForm.find("input[type=file]").each( function () {
            //this.type = 'pseudofile';
            $('<input type="pseudofile" name="' + this.name + '">').insertAfter($(this));
            $('#fileaux').append($(this));
        });
        $("div#ajaxsplash").fadeIn('fast');
        $(theForm).ajaxSubmit(options);
    } else {
        $('html, body').animate({scrollTop: 0}, 'slow');
    }
    
    $('.site-message').remove();
    
    e.preventDefault();
}

function previous(e) {
    var previous_step = $('div#' + CURRENT_STEP).prev().attr('id');
    $('div#' + CURRENT_STEP).fadeOut('fast', function() {
        $('div#' + previous_step).fadeIn('fast');
        $('ul.steps li.active').removeClass('active');
        $('ul.steps li.' + previous_step).addClass('active');
        $('input[name=step]').val(previous_step);
        CURRENT_STEP = previous_step;
        configStepButtons();
        configFields();
    });
    e.preventDefault();
}

function submit(e) {
    clearPlaceholders();
    document.getElementById("novoProjeto").submit();
}

function loadDadosProjeto() {
    $("input[name=participa_cultura_viva]").change(function () {
        loadRadioMultipleExtra(this, 'sim', 'participa_cultura_viva_sim');
    });

    $("input[name=estabeleceu_parcerias]").change(function () {
        loadRadioMultipleExtra(this, 'sim', 'parcerias_sim');
    });
    
    loadRadioMultipleExtra($("input[name=participa_cultura_viva]:checked"),
                           'sim', 'participa_cultura_viva_sim');
    loadRadioMultipleExtra($("input[name=estabeleceu_parcerias]:checked"),
                           'sim', 'parcerias_sim');

}

function loadLocalizacaoGeoProjeto() {
    $('#local_proj').change(function () {
        var li = $(this).parents("li")[0];
        if ($(this).val () == 'outros') {
            $(li).addClass("subhead");
            toogleSingle(true, $('#local_proj_outros'));
            toogleSingle(true, $('#local_proj_outros_novo'));

        } else {
            $(li).removeClass("subhead");
            toogleSingle(false, $('#local_proj_outros'));
            toogleSingle(false, $('#local_proj_outros_novo'));
        }
    });
    $('#local_proj').change();
}

function loadComunicacaoCulturaDigital() {
    $("input[name=sede_possui_tel]").change(function () {
        loadRadioSingleExtra(this, 'sim', 'sede_possui_tel_sim', 'sede_possui_tel_nao');
    });

    $("input[name=sede_possui_net]").change(function () {
        loadRadioSingleExtra(this, 'sim', 'sede_possui_net_sim', 'sede_possui_net_nao');
    });
    
    $('#pq_sem_tel').change(function () {
        if ($(this).val () == 'outro') {
            toogleSingle(true, $('#pq_sem_tel_outro_escolhido'));
        } else {
            toogleSingle(false, $('#pq_sem_tel_outro_escolhido'));
        }
    });

    $('#pq_sem_internet').change(function () {
        
        if ($(this).val () == 'outro') {
            toogleSingle(true, $('#pq_sem_internet_outro_escolhido'));
        } else {
            toogleSingle(false, $('#pq_sem_internet_outro_escolhido'));
        }
    });

    loadRadioSingleExtra($("input[name=sede_possui_tel]:checked"),
                         'sim', 'sede_possui_tel_sim', 'sede_possui_tel_nao');
    loadRadioSingleExtra($("input[name=sede_possui_net]:checked"),
                         'sim', 'sede_possui_net_sim', 'sede_possui_net_nao');
    
    var change = function (id) {
        if ($('#' + id).val () == 'outro') {
            toogleSingle(true, $('#' + id + '_outro_escolhido'));
        } else {
            toogleSingle(false, $('#' + id + '_outro_escolhido'));
        }
    
    }
    change('pq_sem_tel');
    change('pq_sem_internet');

}

function loadEntidadeProponente() {
    $("input[name=convenio_ent]").change(function () {
        loadRadioSingleExtra(this, 'sim', 'convenio_ent_sim');
    });

    $("input[name=endereco_ent_proj]").change(function () {
        loadRadioMultipleExtra(this, 'nao', 'endereco_ent_proj_nao');
    });
    loadRadioSingleExtra($("input[name=convenio_ent]:checked"), 'sim', 'convenio_ent_sim');
    loadRadioMultipleExtra($("input[name=endereco_ent_proj]:checked"), 'nao', 'endereco_ent_proj_nao');
}

function loadAtividadesExercidasProjeto() {
    //nothing yet
}

function loadPublico() {
    //nothing yet
}

function loadIndiceAcessoCultura() {
    //nothing yet
}

$(document).ready (function () {

    decorateRequiredLabels('novoProjeto');

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
    
    loadDadosProjeto();
    loadLocalizacaoGeoProjeto();
    loadComunicacaoCulturaDigital();
    loadEntidadeProponente();
    loadAtividadesExercidasProjeto();
    
    carregar();
        
});

function novoEndereco () {
    var $newElement = $($('#local_proj_outros')[0].children[0].cloneNode (true));
    $('input, select', $newElement).val ('');
    $('.error-message', $newElement).remove();
    $('.error', $newElement).removeClass('error');

    function remClick (evt) {
        function rem() {
            $newElement.parent().remove();
        }
        toogleSingle(false, $newElement.parent(), rem);
    }

    var $remove = removeButton(remClick);
    var title = $('<a>Outro endereço</a>');
    title.css('padding', '0px');
    title.css('margin', '0px');
    $newElement.css('margin', '20px 0px 0px 0px');


    $newElement.removeClass ('subbody');
    $newElement.removeAttr('id');
    var $end = $('<div class="subadded">')
                .append (title)
                .append ($newElement);
    animatedAppendTo($end, $('#local_proj_outros'));
    $('<div style="text-align: right;">')
        .append($remove)
        .appendTo ($newElement.parent());
    //atualizarEnderecos ();
}

function atualizarEnderecos () {
    var $select = $('select[name=local_projeto]');
    var selected = $select.val ();
    $('option', $select).each (function () {
        alert($(this).val());
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
    var $remove = removeButton();
    var $input = $('<input type="file" name="documentacoes"/>');
    var $doc = $('<li>')
                .append ($input)
                .append ($remove)
   animatedAppendTo($doc, $parent);
}

function novoConvenio ($parent) {
    var $remove = removeButton();
    var $input = $('<input type="text" name="outro_convenio" ' + 
                   'class="textarea" />');
    var $conv = $('<li>')
                 .append ($input)
                 .append ($remove)
    animatedAppendTo($conv, $parent);    
}

function novoParceiro ($parent) {
    var $remove =  removeButton();
    var $input = $('<input type="text" name="parcerias" class="required textarea" />');
    var $parc = $('<li>')
                 .append($input)
                 .append($remove);
    animatedAppendTo($parc, $parent);
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
                 'sede_tel': novoTelefone,
                 'ent_tel': novoTelefone,
                 'end_outro_bairro': novoEndereco};
    var blocksSet = {'rs_nome': $('#redesSociais'),
                     'feed_nome': $('#feeds'),
                     'sede_tel': $('#sede_tel'),
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
    var current = $("#" + CURRENT_STEP);
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
    $(theForm).ajaxSubmit(options);
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

////////////////////////////////////////////////////////////////////////////////

function loadRadioSingleExtra(o, v, id1, id2) {
    $('#' + id1).hide();
    $('#' + id2).hide();
    if ($(o).length && $(o).val()) {
        if ($(o).val () == v) {
            if (id2) {
                toogle($('#' + id1), $('#' + id2));
            } else {
                toogleSingle(true, $('#' + id1));
            }
        } else {
            if (id2) {
                toogle($('#' + id2), $('#' + id1));
            } else {
                toogleSingle(false, $('#' + id1));
            }
        }
    }

}

function loadRadioMultipleExtra(o, v, id1, id2) {
    var li = $(o).parents("li")[0];
    $('#' + id1).hide();
    $('#' + id2).hide();
    if ($(o).length && $(o).val()) {
        if ($(o).val () == v) {
            $(li).addClass("subhead");
            if (id2) {
                toogle($('#' + id1), $('#' + id2));
            } else {
                toogleSingle(true, $('#' + id1));
            }
        } else {
            $(li).removeClass("subhead");
            if (id2) {
                toogle($('#' + id2), $('#' + id1));
            } else {
                toogleSingle(false, $('#' + id1));
            }
        }
    }
    $(li).removeClass("subhead");
}

