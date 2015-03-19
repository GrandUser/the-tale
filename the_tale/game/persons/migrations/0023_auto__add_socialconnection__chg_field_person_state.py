# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SocialConnection'
        db.create_table(u'persons_socialconnection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_at_turn', self.gf('django.db.models.fields.BigIntegerField')()),
            ('out_game_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('out_game_at_turn', self.gf('django.db.models.fields.BigIntegerField')(default=None, null=True)),
            ('person_1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['persons.Person'])),
            ('person_2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['persons.Person'])),
            ('connection', self.gf('rels.django.RelationIntegerField')()),
            ('state', self.gf('rels.django.RelationIntegerField')()),
        ))
        db.send_create_signal(u'persons', ['SocialConnection'])


        # Changing field 'Person.state'
        db.alter_column(u'persons_person', 'state', self.gf('rels.django.RelationIntegerField')())

    def backwards(self, orm):
        # Deleting model 'SocialConnection'
        db.delete_table(u'persons_socialconnection')


        # Changing field 'Person.state'
        db.alter_column(u'persons_person', 'state', self.gf('django.db.models.fields.IntegerField')())

    models = {
        u'persons.person': {
            'Meta': {'object_name': 'Person'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2000, 1, 1, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'created_at_turn': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "u'{}'"}),
            'enemies_number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'friends_number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'gender': ('rels.django.RelationIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'out_game_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2000, 1, 1, 0, 0)'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'persons'", 'on_delete': 'models.PROTECT', 'to': u"orm['places.Place']"}),
            'race': ('rels.django.RelationIntegerField', [], {}),
            'state': ('rels.django.RelationIntegerField', [], {}),
            'type': ('rels.django.RelationIntegerField', [], {})
        },
        u'persons.socialconnection': {
            'Meta': {'object_name': 'SocialConnection'},
            'connection': ('rels.django.RelationIntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_at_turn': ('django.db.models.fields.BigIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'out_game_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'out_game_at_turn': ('django.db.models.fields.BigIntegerField', [], {'default': 'None', 'null': 'True'}),
            'person_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['persons.Person']"}),
            'person_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['persons.Person']"}),
            'state': ('rels.django.RelationIntegerField', [], {})
        },
        u'places.place': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Place'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1970, 1, 1, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'created_at_turn': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "u'{}'"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'expected_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'freedom': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'goods': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'habit_honor': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'habit_honor_negative': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'habit_honor_positive': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'habit_peacefulness': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'habit_peacefulness_negative': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'habit_peacefulness_positive': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'heroes_number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_frontier': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'keepers_goods': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modifier': ('rels.django.RelationIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_index': 'True'}),
            'persons_changed_at_turn': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'production': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'race': ('rels.django.RelationIntegerField', [], {}),
            'safety': ('django.db.models.fields.FloatField', [], {'default': '0.75'}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'stability': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'tax': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'transport': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_at_turn': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'x': ('django.db.models.fields.BigIntegerField', [], {}),
            'y': ('django.db.models.fields.BigIntegerField', [], {})
        }
    }

    complete_apps = ['persons']