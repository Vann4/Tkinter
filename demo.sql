PGDMP  7                    |            demo    16.2    16.2 1    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    24590    demo    DATABASE     x   CREATE DATABASE demo WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE demo;
                postgres    false                        3079    25092 	   uuid-ossp 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;
    DROP EXTENSION "uuid-ossp";
                   false            �           0    0    EXTENSION "uuid-ossp"    COMMENT     W   COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';
                        false    2            �            1255    25465    check_email_validity() 	   PROCEDURE     m  CREATE PROCEDURE public.check_email_validity()
    LANGUAGE plpgsql
    AS $_$
DECLARE
    rec RECORD;
    valid BOOLEAN;
BEGIN
    FOR rec IN SELECT "clientID", Email FROM Clients LOOP
        -- Проверяем адрес электронной почты на корректность
        valid := rec.Email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' AND
                 rec.Email !~ '[\"\<>]';
                 
        -- Выводим результат
        RAISE NOTICE 'clientID: %, Email: %, Valid: %', rec."clientID", rec.Email, CASE WHEN valid THEN 1 ELSE 0 END;
    END LOOP;
END;
$_$;
 .   DROP PROCEDURE public.check_email_validity();
       public          postgres    false            �            1255    25276    log_order_status_change()    FUNCTION     k  CREATE FUNCTION public.log_order_status_change() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Вставляем запись в таблицу History
    INSERT INTO History (OrderID, OrderDate, OldStatus, NewStatus)
    VALUES (
        NEW.OrderID,
        NEW.OrderDate,
        OLD.Status,
        NEW.Status
    );

    RETURN NEW;
END;
$$;
 0   DROP FUNCTION public.log_order_status_change();
       public          postgres    false            �            1259    25104    clients    TABLE     �   CREATE TABLE public.clients (
    "clientID" bigint NOT NULL,
    client text,
    phone character varying(15) NOT NULL,
    email text NOT NULL
);
    DROP TABLE public.clients;
       public         heap    postgres    false            �            1259    25103    clients_clientID_seq    SEQUENCE        CREATE SEQUENCE public."clients_clientID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public."clients_clientID_seq";
       public          postgres    false    217            �           0    0    clients_clientID_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public."clients_clientID_seq" OWNED BY public.clients."clientID";
          public          postgres    false    216            �            1259    25112 	   employees    TABLE     *  CREATE TABLE public.employees (
    employeeid uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    employee text NOT NULL,
    birthdate date NOT NULL,
    phone character varying(15) NOT NULL,
    city text NOT NULL,
    street text NOT NULL,
    housenumber text NOT NULL,
    apartment text
);
    DROP TABLE public.employees;
       public         heap    postgres    false    2            �            1259    25267    history    TABLE       CREATE TABLE public.history (
    changedate timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    orderid integer NOT NULL,
    orderdate timestamp without time zone NOT NULL,
    oldstatus character varying(10) NOT NULL,
    newstatus character varying(10) NOT NULL
);
    DROP TABLE public.history;
       public         heap    postgres    false            �            1259    25411    orders    TABLE       CREATE TABLE public.orders (
    orderid integer NOT NULL,
    quantity_product integer,
    quantity_service integer,
    orderdate date NOT NULL,
    paymentmethod text NOT NULL,
    status character varying(10) NOT NULL,
    productid integer,
    serviceid integer,
    employeeid uuid,
    "clientID" bigint NOT NULL,
    CONSTRAINT orders2_status_check CHECK (((status)::text = ANY ((ARRAY['Создан'::character varying, 'Отклонен'::character varying, 'Выполнен'::character varying])::text[])))
);
    DROP TABLE public.orders;
       public         heap    postgres    false            �            1259    25410    orders2_clientID_seq    SEQUENCE        CREATE SEQUENCE public."orders2_clientID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public."orders2_clientID_seq";
       public          postgres    false    226            �           0    0    orders2_clientID_seq    SEQUENCE OWNED BY     P   ALTER SEQUENCE public."orders2_clientID_seq" OWNED BY public.orders."clientID";
          public          postgres    false    225            �            1259    25409    orders2_orderid_seq    SEQUENCE     �   CREATE SEQUENCE public.orders2_orderid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.orders2_orderid_seq;
       public          postgres    false    226            �           0    0    orders2_orderid_seq    SEQUENCE OWNED BY     J   ALTER SEQUENCE public.orders2_orderid_seq OWNED BY public.orders.orderid;
          public          postgres    false    224            �            1259    25121    products    TABLE     �   CREATE TABLE public.products (
    productid integer NOT NULL,
    article text NOT NULL,
    name text NOT NULL,
    price numeric(10,2) NOT NULL,
    countryoforigin text NOT NULL,
    image character varying(255)
);
    DROP TABLE public.products;
       public         heap    postgres    false            �            1259    25120    products_productid_seq    SEQUENCE     �   CREATE SEQUENCE public.products_productid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.products_productid_seq;
       public          postgres    false    220            �           0    0    products_productid_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.products_productid_seq OWNED BY public.products.productid;
          public          postgres    false    219            �            1259    25130    services    TABLE     �   CREATE TABLE public.services (
    serviceid bigint NOT NULL,
    article text NOT NULL,
    name text NOT NULL,
    price numeric(10,2) NOT NULL
);
    DROP TABLE public.services;
       public         heap    postgres    false            �            1259    25129    services_serviceid_seq    SEQUENCE        CREATE SEQUENCE public.services_serviceid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.services_serviceid_seq;
       public          postgres    false    222            �           0    0    services_serviceid_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.services_serviceid_seq OWNED BY public.services.serviceid;
          public          postgres    false    221            ?           2604    25107    clients clientID    DEFAULT     x   ALTER TABLE ONLY public.clients ALTER COLUMN "clientID" SET DEFAULT nextval('public."clients_clientID_seq"'::regclass);
 A   ALTER TABLE public.clients ALTER COLUMN "clientID" DROP DEFAULT;
       public          postgres    false    216    217    217            D           2604    25414    orders orderid    DEFAULT     q   ALTER TABLE ONLY public.orders ALTER COLUMN orderid SET DEFAULT nextval('public.orders2_orderid_seq'::regclass);
 =   ALTER TABLE public.orders ALTER COLUMN orderid DROP DEFAULT;
       public          postgres    false    226    224    226            E           2604    25415    orders clientID    DEFAULT     w   ALTER TABLE ONLY public.orders ALTER COLUMN "clientID" SET DEFAULT nextval('public."orders2_clientID_seq"'::regclass);
 @   ALTER TABLE public.orders ALTER COLUMN "clientID" DROP DEFAULT;
       public          postgres    false    225    226    226            A           2604    25124    products productid    DEFAULT     x   ALTER TABLE ONLY public.products ALTER COLUMN productid SET DEFAULT nextval('public.products_productid_seq'::regclass);
 A   ALTER TABLE public.products ALTER COLUMN productid DROP DEFAULT;
       public          postgres    false    220    219    220            B           2604    25133    services serviceid    DEFAULT     x   ALTER TABLE ONLY public.services ALTER COLUMN serviceid SET DEFAULT nextval('public.services_serviceid_seq'::regclass);
 A   ALTER TABLE public.services ALTER COLUMN serviceid DROP DEFAULT;
       public          postgres    false    222    221    222            �          0    25104    clients 
   TABLE DATA           C   COPY public.clients ("clientID", client, phone, email) FROM stdin;
    public          postgres    false    217   A<       �          0    25112 	   employees 
   TABLE DATA           q   COPY public.employees (employeeid, employee, birthdate, phone, city, street, housenumber, apartment) FROM stdin;
    public          postgres    false    218   l=       �          0    25267    history 
   TABLE DATA           W   COPY public.history (changedate, orderid, orderdate, oldstatus, newstatus) FROM stdin;
    public          postgres    false    223   @       �          0    25411    orders 
   TABLE DATA           �   COPY public.orders (orderid, quantity_product, quantity_service, orderdate, paymentmethod, status, productid, serviceid, employeeid, "clientID") FROM stdin;
    public          postgres    false    226   l@       �          0    25121    products 
   TABLE DATA           [   COPY public.products (productid, article, name, price, countryoforigin, image) FROM stdin;
    public          postgres    false    220   2B       �          0    25130    services 
   TABLE DATA           C   COPY public.services (serviceid, article, name, price) FROM stdin;
    public          postgres    false    222   9C       �           0    0    clients_clientID_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public."clients_clientID_seq"', 10, true);
          public          postgres    false    216            �           0    0    orders2_clientID_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public."orders2_clientID_seq"', 1, false);
          public          postgres    false    225            �           0    0    orders2_orderid_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.orders2_orderid_seq', 10, true);
          public          postgres    false    224            �           0    0    products_productid_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.products_productid_seq', 15, true);
          public          postgres    false    219            �           0    0    services_serviceid_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.services_serviceid_seq', 10, true);
          public          postgres    false    221            H           2606    25111    clients clients_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY ("clientID");
 >   ALTER TABLE ONLY public.clients DROP CONSTRAINT clients_pkey;
       public            postgres    false    217            J           2606    25119    employees employees_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (employeeid);
 B   ALTER TABLE ONLY public.employees DROP CONSTRAINT employees_pkey;
       public            postgres    false    218            P           2606    25420    orders orders2_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders2_pkey PRIMARY KEY (orderid);
 =   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders2_pkey;
       public            postgres    false    226            L           2606    25128    products products_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (productid);
 @   ALTER TABLE ONLY public.products DROP CONSTRAINT products_pkey;
       public            postgres    false    220            N           2606    25137    services services_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_pkey PRIMARY KEY (serviceid);
 @   ALTER TABLE ONLY public.services DROP CONSTRAINT services_pkey;
       public            postgres    false    222            Q           2606    25436    orders orders_clientID_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT "orders_clientID_fkey" FOREIGN KEY ("clientID") REFERENCES public.clients("clientID");
 G   ALTER TABLE ONLY public.orders DROP CONSTRAINT "orders_clientID_fkey";
       public          postgres    false    226    217    4680            R           2606    25431    orders orders_employeeid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_employeeid_fkey FOREIGN KEY (employeeid) REFERENCES public.employees(employeeid);
 G   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_employeeid_fkey;
       public          postgres    false    226    218    4682            S           2606    25458    orders orders_productid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_productid_fkey FOREIGN KEY (productid) REFERENCES public.products(productid) ON DELETE CASCADE NOT VALID;
 F   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_productid_fkey;
       public          postgres    false    226    220    4684            T           2606    25426    orders orders_serviceid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_serviceid_fkey FOREIGN KEY (serviceid) REFERENCES public.services(serviceid);
 F   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_serviceid_fkey;
       public          postgres    false    226    222    4686            �     x�u��j�@��'O�}a0�bv}�n�f�Cn�Hp����"}Vk�����"$~f5���|6a�#���l�w��t&�8{RK�%^���(ʏ���ӥ�4W�ĠF�/���Tۖ�܈�4ԉ�7&�pE�K��wQ�+��c���S���bo8q��d�%&8%ly�O������[��S
��*u`l���_+G�w-8]�!/ԋD�3�W^��fw��egi?������N<�q}7��x��@z�e�ۃ��C��>�'����e%��,,����\      �   �  x�e�MN�@���Sp�����{ n�Mw�} B�"�&� �d�F!Hd��}�<{�03�x=r�W�ճ��^&��H���s��CI��R+Q/�S}������~��
ސ4�F� WfQ/��xX��W]����J���l��U!�zKZ���.SgT�6h_J7�x����e�W��k�j�$-)�AU;���������D�
+�ܻ�tQ�|1���Y���I��Y��(�=��/�z3Kܑڔ����a�u�����4D�d|����(xx퍶z��vB?�Ɲ��z�8��Ԫwp���.�\��R�ƺ���^Cm��)�H���gϪ� �:<�GмxCߴ�|V���M�y�\`���]V���1C4	��+�a�JQ��8�Ai�D��v�ػ��͊�ۙ�;�[����y__���6.��E0�A�RJ�EXm��X��.ƣ��x�?����ۓ^���X��O�=^�tR��u��Rk$i�=%-�	�61�P]MPX�4~yU{���v�j;N~W-�| ��s4W��5K=ye�7R�\O�}\�E[?=������Z�E�'<�ĵ���5m����� Eh��I�wo���R"+)=G���崧m�Y�	&�=I�1ؿ�����?Wg�W�l>�M��^�      �   U   x�3202�50�54Q02�22�24�305��0�4�4�J*X�煅�]�~a˅�r^�t���~���{/l���+F��� ��      �   �  x��SK�1\;��F��N���ɯ�1bÂK$��o�hF3\!�F���<���厒T���pd��0�O��u\_����u���֍�+_`]����w�d�[,8�2Jm��gD+�mDlQ(�z�aX���Iޭ���u����G�u֣�'�k��.<Qx$1E����-�9����@��o/����Ɖ���.h�<�	��;��6����y�:wj��~��K�Q�G���6�^)�Z�(7,�~�J�T�HO A��[_���2����{�8L\Gs�Z��Z݈g,�!y�B����ԥ���Wm�c��Sa�F5���;g�R�ni�������&��gi)!'��[k�0=�2v$���������T��&�[gbOQ(l�/�ϙ֦���9�_i?���߳����݆4A����>&o�f%�Ѩz1�yB�	wibh      �   �   x�=��N�@D�돉�o��F�:���B<D�"E!傈bb����?b��ƍ-����n.W���w}�;x�%wn��ᨽ��I�Y�B�!v��#)��'�,#X
����\/e��L���k`��ܓ��sN������/��u�j�Zz�#��R'�q�?M���9�4	~c�3�F���}1}��I���iN��
�<�mN7�`o�ex��֡ٳ�
x�Qx	�w�f�gY��"J��      �      x�Uл1��x\�f�v�DD3�+��i��Ȼ�F|���� �u�{��3�7����գ��h�ԓ��d�ճ��l^ԋ��b^ի��j�ԛ��f�ջ��n>ԇ��a.\���@\��幅~�%{c     