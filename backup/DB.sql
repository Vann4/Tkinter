PGDMP  $                      |            DB    16.2    16.2     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    25482    DB    DATABASE     x   CREATE DATABASE "DB" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE "DB";
                postgres    false            �            1259    25484    Users    TABLE     [   CREATE TABLE public."Users" (
    id bigint NOT NULL,
    login text,
    password text
);
    DROP TABLE public."Users";
       public         heap    postgres    false            �            1259    25483    Users_id_seq    SEQUENCE     w   CREATE SEQUENCE public."Users_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public."Users_id_seq";
       public          postgres    false    216            �           0    0    Users_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public."Users_id_seq" OWNED BY public."Users".id;
          public          postgres    false    215                       2604    25487    Users id    DEFAULT     h   ALTER TABLE ONLY public."Users" ALTER COLUMN id SET DEFAULT nextval('public."Users_id_seq"'::regclass);
 9   ALTER TABLE public."Users" ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    216    215    216            �          0    25484    Users 
   TABLE DATA           6   COPY public."Users" (id, login, password) FROM stdin;
    public          postgres    false    216   
       �           0    0    Users_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public."Users_id_seq"', 11, true);
          public          postgres    false    215                       2606    25491    Users Users_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_pkey" PRIMARY KEY (id);
 >   ALTER TABLE ONLY public."Users" DROP CONSTRAINT "Users_pkey";
       public            postgres    false    216            �     x�e��r�8����L!鰘E�%1"t�� ��A`'����5�^y�:+U}��9��vp�����P,��~T2�h�ؾSx�\r�w1��S:��sn��K%إ��T�v�-��>�( f~%�����IA�b�+
�D��	s�TNM����ܜ�M�C��IN$2S�>k�`��Z�^���$~ƩoFz�#AY���ߊ�,M�z���'�R�_x����r������AsR��O������q7g���0�-�Vz
�حz��X���bfJ���<�v An����鵰	���Ɩ1|U�o�LfG��Vg�v����dc�$[6�����os��h��]�cB�p���hm�E�J���pG��եu	ү� H�C�f�G�����͡��c�6^�����K�㞛*�j!�dN��t|�q�ߜ�;�r!}-_`%����[�x_� �YB[������欦����SR�r��B�v��75,�
{ʄ�f�_��Z��S	ے*�g;��^�m/~h7��;�h7���@���{T���}�*���8��TN3qD��2d�>��:R����C�v�FV7���c����P��}�m�q-��A�S��3��ԯ���[���':e�[𣣝�.=��j��ﮰ4���Wݶk*sȼ
��L��,��v��G֛����v�/�%G��BG��������tG��>��5��NB��iч��P:�̈ ��#pM.�����I��i�ܵ{W%:nb����\9#qS-��H�n��)���Q;?��sp��E{�04'��k.h�Rl+�֑-l��z*R���a� b��o�����|R���t|i�����R��f�7;�j��?� g=�}�Yyܝ���uEDp ��qƜ�G�i�!��/YD��a��D �f��I�R+�CD�~��U5���Ӫ�xd"Y�'��>/̈́Q��`广ǜ����۞2���HUQs����:�U|�r����t!.j8��U�N\�y�{}ѱ�2�D�Z��^�m*���:GD k�$�����w��     