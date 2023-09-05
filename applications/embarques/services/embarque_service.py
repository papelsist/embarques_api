from ..models import Embarque,Entrega,EntregaDet,Envio,EnvioDet



def salvar_embarque(embarque_dict):
 
    embarque = Embarque.objects.get(id = embarque_dict['embarqueId'])
    embarque.cp = embarque_dict['foraneo']
    
    embarque.save()

    for ent in embarque_dict['partidas']:
        envio = Envio.objects.get(id = ent['envioId'])
        entrega = Entrega(
                    envio=envio,
                    embarque=embarque,
                    sucursal = embarque.sucursal.nombre,
                    destinatario = ent['destinatario'],
                    operador = embarque.operador.nombre,
                    entidad = ent['entidad'],
                    fecha_documento = ent['fechaDocumento'],
                    documento = ent['documento'],
                    tipo_documento = ent['tipoDocumento'],
                    origen = ent['tipoDocumento']
                    )
        
        entrega.save()

        for det in ent['detalles']:
            envio_det = EnvioDet.objects.get(id = det['id'])
            entrega_det = EntregaDet(
                entrega= entrega,
                envio_det = envio_det,
                clave = det['clave'],
                descripcion = det['me_descripcion'],
                cantidad = det['enviar'],
                valor = det['valor']
            )

            entrega_det.save()

           
