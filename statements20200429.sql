SELECT "name",id FROM "giscedata_polissa" WHERE id in (13) ORDER BY id
select ref, sum(coalesce(debit, 0) - coalesce(credit, 0)) from account_move_line where product_id = 222 and ref in ('0000013') and account_id = 101299 group by ref
SELECT "name",id FROM "res_partner" WHERE id in (2273) ORDER BY name
SELECT "name",id FROM "res_partner" WHERE id in (2273) ORDER BY name
SELECT MAX(CASE WHEN perm_read THEN 1 ELSE 0 END)   FROM ir_model_access a   JOIN ir_model m ON (m.id = a.model_id)   JOIN res_groups_users_rel gu ON (gu.gid = a.group_id)  WHERE m.model = 'giscedata.tensions.tensio'    AND gu.uid = 64 
SELECT "name",id FROM "giscedata_tensions_tensio" WHERE id in (4) ORDER BY id
SELECT "name",id FROM "giscedata_tensions_tensio" WHERE id in (4) ORDER BY id
SELECT "name",id FROM "res_partner" WHERE id in (2108) ORDER BY name
SELECT "name",id FROM "res_partner" WHERE id in (2108) ORDER BY name
SELECT giscedata_polissa_category_rel.category_id, giscedata_polissa_category_rel.polissa_id                    FROM giscedata_polissa_category_rel, giscedata_polissa_category                   WHERE giscedata_polissa_category_rel.polissa_id in (13)                     AND giscedata_polissa_category_rel.category_id = giscedata_polissa_category.id                                                        ORDER BY giscedata_polissa_category.parent_id,name                  OFFSET 0
SELECT "coef_repartiment","comercialitzadora","ref_dist","direccio_pagament","autoconsumo","versio_primera_factura","data_ultima_lectura","active","empowering_profile_id","pending_state","name_auto","cups","notificacio","donatiu","agree_dh","user_id","no_cessio_sips","payment_mode_id","soci","empowering_last_update","data_alta","bono_social_disponible","tg","tipus_vivenda","tensio","facturacio_suspesa","fiscal_position_id","nocutoff","modcontractual_activa","empowering_service","refacturacio_pendent","mode_facturacio","process_id","agree_tipus","facturae_filereference","condicions_generals_id","tarifa","bank","name","renovacio_auto","enviament","state_post_facturacio","cie","lot_facturacio","observacions_estimacio","data_baixa","no_cessio_sips_data","coeficient_k","cnae","pending_amount","data_ultima_lectura_estimada","tipo_pago","expected_consumption","contract_type","no_estimable","is_autoconsum_collectiu","pagador_sel","data_ultima_lectura_perfilada","proxima_facturacio","titular","altre_p","unpaid_invoices","llista_preu","lectura_en_baja","state","etag","potencia","data_firma_contracte","trafo","direccio_notificacio","distribuidora","coeficient_d","agree_tensio","observacions","facturacio","facturacio_potencia","tensio_normalitzada","print_observations","debt_amount","agree_tarifa","pagador","facturacio_distri","empowering_profile",id FROM "giscedata_polissa" WHERE id in (13) ORDER BY id
SELECT "apartat_correus","aclarador","street","partner_id","es","city","pt","title","tv","country_id","type","email","nv","function","fax","zip","pnp","street2","phone","bq","active","id_municipi","name","ref_catastral","cpo","mobile","cpa","notes","pu","id_poblacio","birthdate","state_id",id FROM "res_partner_address" WHERE id in (1880, 63) ORDER BY id
COMMIT
BEGIN ISOLATION LEVEL READ COMMITTED
select distinct res_model from ir_attachment where id in (4480385, 5956819, 10463181, 10444935)
SELECT MAX(CASE WHEN perm_read THEN 1 ELSE 0 END)   FROM ir_model_access a   JOIN ir_model m ON (m.id = a.model_id)   JOIN res_groups_users_rel gu ON (gu.gid = a.group_id)  WHERE m.model = 'giscedata.polissa'    AND gu.uid = 64 
SELECT MAX(CASE WHEN perm_read THEN 1 ELSE 0 END)   FROM ir_model_access a   JOIN ir_model m ON (m.id = a.model_id)   JOIN res_groups_users_rel gu ON (gu.gid = a.group_id)  WHERE m.model = 'ir.attachment'    AND gu.uid = 64 
SELECT COALESCE(write_date, create_date, now())::timestamp AS __last_update,"create_uid",date_trunc('second', create_date) as create_date,"name","category_id","datas_fname",id FROM "ir_attachment" WHERE id in (4480385, 5956819, 10463181, 10444935) ORDER BY id
SELECT "name",id FROM "res_users" WHERE id in (1) ORDER BY id
SELECT "name",id FROM "res_users" WHERE id in (1) ORDER BY id
select distinct res_model from ir_attachment where id in (4480385, 5956819, 10444935, 10463181)
SELECT MAX(CASE WHEN perm_read THEN 1 ELSE 0 END)   FROM ir_model_access a   JOIN ir_model m ON (m.id = a.model_id)   JOIN res_groups_users_rel gu ON (gu.gid = a.group_id)  WHERE m.model = 'giscedata.polissa'    AND gu.uid = 64 
SELECT "res_model","res_id",id FROM "ir_attachment" WHERE id in (4480385, 5956819, 10444935, 10463181) ORDER BY id
select ir_model.id from "ir_model" where (ir_model.model = 'giscedata.polissa') order by id
SELECT MAX(CASE WHEN perm_read THEN 1 ELSE 0 END)   FROM ir_model_access a   JOIN ir_model m ON (m.id = a.model_id)   JOIN res_groups_users_rel gu ON (gu.gid = a.group_id)  WHERE m.model = 'ir.model'    AND gu.uid = 64 
SELECT "info","state","name","model",id FROM "ir_model" WHERE id in (170) ORDER BY id
SELECT indexrelname, cast(idx_tup_read AS numeric) / idx_scan AS avg_tuples, idx_scan,idx_tup_read FROM pg_stat_user_indexes WHERE idx_scan > 0 order by avg_tuples desc
SELECT "info","state","name","model",id FROM "ir_model" WHERE id in (172) ORDER BY id
SELECT "info","state","name","model",id FROM "ir_model" WHERE id in (173) ORDER BY id
