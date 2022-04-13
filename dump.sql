--
-- PostgreSQL database dump
--

-- Dumped from database version 14.0 (Debian 14.0-1.pgdg110+1)
-- Dumped by pg_dump version 14.0 (Debian 14.0-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: pg_trgm; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;


--
-- Name: EXTENSION pg_trgm; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';


--
-- Name: unaccent; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS unaccent WITH SCHEMA public;


--
-- Name: EXTENSION unaccent; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION unaccent IS 'text search dictionary that removes accents';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO postgres;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: calculator_crop; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.calculator_crop (
    id bigint NOT NULL,
    notes character varying(500),
    object_id integer NOT NULL,
    area_id bigint NOT NULL,
    content_type_id integer NOT NULL,
    CONSTRAINT calculator_crop_object_id_check CHECK ((object_id >= 0))
);


ALTER TABLE public.calculator_crop OWNER TO postgres;

--
-- Name: calculator_crop_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.calculator_crop_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calculator_crop_id_seq OWNER TO postgres;

--
-- Name: calculator_crop_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.calculator_crop_id_seq OWNED BY public.calculator_crop.id;


--
-- Name: calculator_cropparameter; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.calculator_cropparameter (
    id bigint NOT NULL,
    value double precision NOT NULL,
    url_ref character varying(200),
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    crop_id bigint NOT NULL,
    parameter_id integer NOT NULL
);


ALTER TABLE public.calculator_cropparameter OWNER TO postgres;

--
-- Name: calculator_cropparameter_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.calculator_cropparameter_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calculator_cropparameter_id_seq OWNER TO postgres;

--
-- Name: calculator_cropparameter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.calculator_cropparameter_id_seq OWNED BY public.calculator_cropparameter.id;


--
-- Name: calculator_management; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.calculator_management (
    id bigint NOT NULL,
    date date NOT NULL,
    notes text,
    type_id bigint NOT NULL,
    crop_id bigint NOT NULL
);


ALTER TABLE public.calculator_management OWNER TO postgres;

--
-- Name: calculator_management_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.calculator_management_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calculator_management_id_seq OWNER TO postgres;

--
-- Name: calculator_management_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.calculator_management_id_seq OWNED BY public.calculator_management.id;


--
-- Name: calculator_managementtype; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.calculator_managementtype (
    id bigint NOT NULL,
    code character varying(30) NOT NULL,
    name character varying(100) NOT NULL,
    description text
);


ALTER TABLE public.calculator_managementtype OWNER TO postgres;

--
-- Name: calculator_managementtype_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.calculator_managementtype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calculator_managementtype_id_seq OWNER TO postgres;

--
-- Name: calculator_managementtype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.calculator_managementtype_id_seq OWNED BY public.calculator_managementtype.id;


--
-- Name: collect_cart; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.collect_cart (
    id bigint NOT NULL,
    created_at date NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.collect_cart OWNER TO postgres;

--
-- Name: collect_cart_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.collect_cart_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.collect_cart_id_seq OWNER TO postgres;

--
-- Name: collect_cart_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.collect_cart_id_seq OWNED BY public.collect_cart.id;


--
-- Name: collect_cartitem; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.collect_cartitem (
    id bigint NOT NULL,
    weight double precision NOT NULL,
    cart_id bigint NOT NULL,
    sample_id bigint NOT NULL
);


ALTER TABLE public.collect_cartitem OWNER TO postgres;

--
-- Name: collect_cartitem_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.collect_cartitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.collect_cartitem_id_seq OWNER TO postgres;

--
-- Name: collect_cartitem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.collect_cartitem_id_seq OWNED BY public.collect_cartitem.id;


--
-- Name: collect_germinability; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.collect_germinability (
    id bigint NOT NULL,
    germinability integer NOT NULL,
    after_days integer,
    performed_at date,
    seedsample_id bigint NOT NULL
);


ALTER TABLE public.collect_germinability OWNER TO postgres;

--
-- Name: collect_germinability_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.collect_germinability_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.collect_germinability_id_seq OWNER TO postgres;

--
-- Name: collect_germinability_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.collect_germinability_id_seq OWNED BY public.collect_germinability.id;


--
-- Name: collect_sampleweight; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.collect_sampleweight (
    id bigint NOT NULL,
    weight double precision NOT NULL,
    seedsample_id bigint NOT NULL,
    created_at date NOT NULL
);


ALTER TABLE public.collect_sampleweight OWNER TO postgres;

--
-- Name: collect_sampleweight_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.collect_sampleweight_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.collect_sampleweight_id_seq OWNER TO postgres;

--
-- Name: collect_sampleweight_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.collect_sampleweight_id_seq OWNED BY public.collect_sampleweight.id;


--
-- Name: collect_seedsample; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.collect_seedsample (
    id bigint NOT NULL,
    notes character varying(500),
    growing_season integer,
    variety_id integer NOT NULL,
    position_id bigint NOT NULL,
    sample_id integer NOT NULL,
    CONSTRAINT collect_seedsample_sample_id_check CHECK ((sample_id >= 0))
);


ALTER TABLE public.collect_seedsample OWNER TO postgres;

--
-- Name: collect_seedsample_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.collect_seedsample_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.collect_seedsample_id_seq OWNER TO postgres;

--
-- Name: collect_seedsample_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.collect_seedsample_id_seq OWNED BY public.collect_seedsample.id;


--
-- Name: collect_storage; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.collect_storage (
    id bigint NOT NULL,
    name character varying(200) NOT NULL
);


ALTER TABLE public.collect_storage OWNER TO postgres;

--
-- Name: collect_storage_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.collect_storage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.collect_storage_id_seq OWNER TO postgres;

--
-- Name: collect_storage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.collect_storage_id_seq OWNED BY public.collect_storage.id;


--
-- Name: collect_storageposition; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.collect_storageposition (
    id bigint NOT NULL,
    name character varying(200) NOT NULL,
    storage_id bigint NOT NULL
);


ALTER TABLE public.collect_storageposition OWNER TO postgres;

--
-- Name: collect_storageposition_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.collect_storageposition_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.collect_storageposition_id_seq OWNER TO postgres;

--
-- Name: collect_storageposition_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.collect_storageposition_id_seq OWNED BY public.collect_storageposition.id;


--
-- Name: describe_description; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.describe_description (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    protocol_id integer NOT NULL,
    variety_id integer NOT NULL
);


ALTER TABLE public.describe_description OWNER TO postgres;

--
-- Name: describe_description_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.describe_description_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.describe_description_id_seq OWNER TO postgres;

--
-- Name: describe_description_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.describe_description_id_seq OWNED BY public.describe_description.id;


--
-- Name: describe_expression; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.describe_expression (
    id integer NOT NULL,
    description_id integer NOT NULL,
    state_of_expression_id integer NOT NULL
);


ALTER TABLE public.describe_expression OWNER TO postgres;

--
-- Name: describe_expression_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.describe_expression_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.describe_expression_id_seq OWNER TO postgres;

--
-- Name: describe_expression_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.describe_expression_id_seq OWNED BY public.describe_expression.id;


--
-- Name: describe_protocol; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.describe_protocol (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    specie_id integer NOT NULL,
    url_ref character varying(200)
);


ALTER TABLE public.describe_protocol OWNER TO postgres;

--
-- Name: describe_protocol_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.describe_protocol_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.describe_protocol_id_seq OWNER TO postgres;

--
-- Name: describe_protocol_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.describe_protocol_id_seq OWNED BY public.describe_protocol.id;


--
-- Name: describe_state; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.describe_state (
    id integer NOT NULL,
    numeric_id integer,
    description character varying(200) NOT NULL,
    trait_id integer NOT NULL
);


ALTER TABLE public.describe_state OWNER TO postgres;

--
-- Name: describe_state_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.describe_state_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.describe_state_id_seq OWNER TO postgres;

--
-- Name: describe_state_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.describe_state_id_seq OWNED BY public.describe_state.id;


--
-- Name: describe_trait; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.describe_trait (
    id integer NOT NULL,
    numeric_id integer,
    description character varying(200) NOT NULL,
    protocol_id integer
);


ALTER TABLE public.describe_trait OWNER TO postgres;

--
-- Name: describe_trait_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.describe_trait_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.describe_trait_id_seq OWNER TO postgres;

--
-- Name: describe_trait_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.describe_trait_id_seq OWNED BY public.describe_trait.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: parameters_speciesparameter; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.parameters_speciesparameter (
    id integer NOT NULL,
    url_ref character varying(200),
    value double precision NOT NULL,
    specie_id integer NOT NULL,
    parameter_id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.parameters_speciesparameter OWNER TO postgres;

--
-- Name: parameters_cropparameter_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.parameters_cropparameter_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.parameters_cropparameter_id_seq OWNER TO postgres;

--
-- Name: parameters_cropparameter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.parameters_cropparameter_id_seq OWNED BY public.parameters_speciesparameter.id;


--
-- Name: parameters_measure; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.parameters_measure (
    id integer NOT NULL,
    georeference_lat double precision NOT NULL,
    georeference_lon double precision NOT NULL,
    measure_unit character varying(50) NOT NULL,
    value double precision NOT NULL,
    trait_id integer NOT NULL,
    variety_id integer NOT NULL
);


ALTER TABLE public.parameters_measure OWNER TO postgres;

--
-- Name: parameters_measure_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.parameters_measure_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.parameters_measure_id_seq OWNER TO postgres;

--
-- Name: parameters_measure_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.parameters_measure_id_seq OWNED BY public.parameters_measure.id;


--
-- Name: parameters_parameter; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.parameters_parameter (
    id integer NOT NULL,
    code character varying(50) NOT NULL,
    name character varying(200) NOT NULL,
    description character varying(200) NOT NULL,
    measure_unit character varying(50) NOT NULL
);


ALTER TABLE public.parameters_parameter OWNER TO postgres;

--
-- Name: parameters_parameter_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.parameters_parameter_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.parameters_parameter_id_seq OWNER TO postgres;

--
-- Name: parameters_parameter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.parameters_parameter_id_seq OWNED BY public.parameters_parameter.id;


--
-- Name: parameters_varietalparameter; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.parameters_varietalparameter (
    id integer NOT NULL,
    url_ref character varying(200),
    value double precision NOT NULL,
    variety_id integer NOT NULL,
    parameter_id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.parameters_varietalparameter OWNER TO postgres;

--
-- Name: parameters_varietalparameter_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.parameters_varietalparameter_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.parameters_varietalparameter_id_seq OWNER TO postgres;

--
-- Name: parameters_varietalparameter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.parameters_varietalparameter_id_seq OWNED BY public.parameters_varietalparameter.id;


--
-- Name: register_plantspecies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.register_plantspecies (
    id integer NOT NULL,
    common_name character varying(100) NOT NULL,
    latin_name character varying(100) NOT NULL,
    plant_type character varying(100) NOT NULL
);


ALTER TABLE public.register_plantspecies OWNER TO postgres;

--
-- Name: register_plantspecies_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.register_plantspecies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.register_plantspecies_id_seq OWNER TO postgres;

--
-- Name: register_plantspecies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.register_plantspecies_id_seq OWNED BY public.register_plantspecies.id;


--
-- Name: register_plantvariety; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.register_plantvariety (
    id integer NOT NULL,
    species_id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.register_plantvariety OWNER TO postgres;

--
-- Name: register_plantvariety_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.register_plantvariety_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.register_plantvariety_id_seq OWNER TO postgres;

--
-- Name: register_plantvariety_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.register_plantvariety_id_seq OWNED BY public.register_plantvariety.id;


--
-- Name: register_plantvarietyname; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.register_plantvarietyname (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    variety_id integer NOT NULL,
    change_date date
);


ALTER TABLE public.register_plantvarietyname OWNER TO postgres;

--
-- Name: register_plantvarietyname_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.register_plantvarietyname_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.register_plantvarietyname_id_seq OWNER TO postgres;

--
-- Name: register_plantvarietyname_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.register_plantvarietyname_id_seq OWNED BY public.register_plantvarietyname.id;


--
-- Name: spaces_area; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.spaces_area (
    id bigint NOT NULL,
    name character varying(30) NOT NULL,
    length double precision NOT NULL,
    width double precision NOT NULL,
    temp_offset integer NOT NULL,
    location_id bigint NOT NULL
);


ALTER TABLE public.spaces_area OWNER TO postgres;

--
-- Name: spaces_area_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.spaces_area_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.spaces_area_id_seq OWNER TO postgres;

--
-- Name: spaces_area_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.spaces_area_id_seq OWNED BY public.spaces_area.id;


--
-- Name: spaces_location; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.spaces_location (
    id bigint NOT NULL,
    name character varying(30) NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL
);


ALTER TABLE public.spaces_location OWNER TO postgres;

--
-- Name: spaces_location_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.spaces_location_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.spaces_location_id_seq OWNER TO postgres;

--
-- Name: spaces_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.spaces_location_id_seq OWNED BY public.spaces_location.id;


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: calculator_crop id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calculator_crop ALTER COLUMN id SET DEFAULT nextval('public.calculator_crop_id_seq'::regclass);


--
-- Name: calculator_cropparameter id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calculator_cropparameter ALTER COLUMN id SET DEFAULT nextval('public.calculator_cropparameter_id_seq'::regclass);


--
-- Name: calculator_management id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calculator_management ALTER COLUMN id SET DEFAULT nextval('public.calculator_management_id_seq'::regclass);


--
-- Name: calculator_managementtype id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calculator_managementtype ALTER COLUMN id SET DEFAULT nextval('public.calculator_managementtype_id_seq'::regclass);


--
-- Name: collect_cart id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_cart ALTER COLUMN id SET DEFAULT nextval('public.collect_cart_id_seq'::regclass);


--
-- Name: collect_cartitem id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_cartitem ALTER COLUMN id SET DEFAULT nextval('public.collect_cartitem_id_seq'::regclass);


--
-- Name: collect_germinability id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_germinability ALTER COLUMN id SET DEFAULT nextval('public.collect_germinability_id_seq'::regclass);


--
-- Name: collect_sampleweight id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_sampleweight ALTER COLUMN id SET DEFAULT nextval('public.collect_sampleweight_id_seq'::regclass);


--
-- Name: collect_seedsample id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_seedsample ALTER COLUMN id SET DEFAULT nextval('public.collect_seedsample_id_seq'::regclass);


--
-- Name: collect_storage id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_storage ALTER COLUMN id SET DEFAULT nextval('public.collect_storage_id_seq'::regclass);


--
-- Name: collect_storageposition id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_storageposition ALTER COLUMN id SET DEFAULT nextval('public.collect_storageposition_id_seq'::regclass);


--
-- Name: describe_description id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.describe_description ALTER COLUMN id SET DEFAULT nextval('public.describe_description_id_seq'::regclass);


--
-- Name: describe_expression id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.describe_expression ALTER COLUMN id SET DEFAULT nextval('public.describe_expression_id_seq'::regclass);


--
-- Name: describe_protocol id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.describe_protocol ALTER COLUMN id SET DEFAULT nextval('public.describe_protocol_id_seq'::regclass);


--
-- Name: describe_state id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.describe_state ALTER COLUMN id SET DEFAULT nextval('public.describe_state_id_seq'::regclass);


--
-- Name: describe_trait id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.describe_trait ALTER COLUMN id SET DEFAULT nextval('public.describe_trait_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: parameters_measure id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parameters_measure ALTER COLUMN id SET DEFAULT nextval('public.parameters_measure_id_seq'::regclass);


--
-- Name: parameters_parameter id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parameters_parameter ALTER COLUMN id SET DEFAULT nextval('public.parameters_parameter_id_seq'::regclass);


--
-- Name: parameters_speciesparameter id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parameters_speciesparameter ALTER COLUMN id SET DEFAULT nextval('public.parameters_cropparameter_id_seq'::regclass);


--
-- Name: parameters_varietalparameter id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parameters_varietalparameter ALTER COLUMN id SET DEFAULT nextval('public.parameters_varietalparameter_id_seq'::regclass);


--
-- Name: register_plantspecies id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.register_plantspecies ALTER COLUMN id SET DEFAULT nextval('public.register_plantspecies_id_seq'::regclass);


--
-- Name: register_plantvariety id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.register_plantvariety ALTER COLUMN id SET DEFAULT nextval('public.register_plantvariety_id_seq'::regclass);


--
-- Name: register_plantvarietyname id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.register_plantvarietyname ALTER COLUMN id SET DEFAULT nextval('public.register_plantvarietyname_id_seq'::regclass);


--
-- Name: spaces_area id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.spaces_area ALTER COLUMN id SET DEFAULT nextval('public.spaces_area_id_seq'::regclass);


--
-- Name: spaces_location id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.spaces_location ALTER COLUMN id SET DEFAULT nextval('public.spaces_location_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
25	Can add plant species	7	add_plantspecies
26	Can change plant species	7	change_plantspecies
27	Can delete plant species	7	delete_plantspecies
28	Can view plant species	7	view_plantspecies
29	Can add plant variety	8	add_plantvariety
30	Can change plant variety	8	change_plantvariety
31	Can delete plant variety	8	delete_plantvariety
32	Can view plant variety	8	view_plantvariety
33	Can add description	9	add_description
34	Can change description	9	change_description
35	Can delete description	9	delete_description
36	Can view description	9	view_description
37	Can add protocol	10	add_protocol
38	Can change protocol	10	change_protocol
39	Can delete protocol	10	delete_protocol
40	Can view protocol	10	view_protocol
41	Can add trait	11	add_trait
42	Can change trait	11	change_trait
43	Can delete trait	11	delete_trait
44	Can view trait	11	view_trait
45	Can add state	12	add_state
46	Can change state	12	change_state
47	Can delete state	12	delete_state
48	Can view state	12	view_state
49	Can add expression	13	add_expression
50	Can change expression	13	change_expression
51	Can delete expression	13	delete_expression
52	Can view expression	13	view_expression
53	Can add varietal parameter	14	add_varietalparameter
54	Can change varietal parameter	14	change_varietalparameter
55	Can delete varietal parameter	14	delete_varietalparameter
56	Can view varietal parameter	14	view_varietalparameter
57	Can add measure	15	add_measure
58	Can change measure	15	change_measure
59	Can delete measure	15	delete_measure
60	Can view measure	15	view_measure
61	Can add crop parameter	16	add_cropparameter
62	Can change crop parameter	16	change_cropparameter
63	Can delete crop parameter	16	delete_cropparameter
64	Can view crop parameter	16	view_cropparameter
65	Can add parameter	17	add_parameter
66	Can change parameter	17	change_parameter
67	Can delete parameter	17	delete_parameter
68	Can view parameter	17	view_parameter
69	Can add location	18	add_location
70	Can change location	18	change_location
71	Can delete location	18	delete_location
72	Can view location	18	view_location
73	Can add garden	19	add_garden
74	Can change garden	19	change_garden
75	Can delete garden	19	delete_garden
76	Can view garden	19	view_garden
77	Can add area	20	add_area
78	Can change area	20	change_area
79	Can delete area	20	delete_area
80	Can view area	20	view_area
81	Can add crop	21	add_crop
82	Can change crop	21	change_crop
83	Can delete crop	21	delete_crop
84	Can view crop	21	view_crop
85	Can add seed sample	22	add_seedsample
86	Can change seed sample	22	change_seedsample
87	Can delete seed sample	22	delete_seedsample
88	Can view seed sample	22	view_seedsample
89	Can add germinability	23	add_germinability
90	Can change germinability	23	change_germinability
91	Can delete germinability	23	delete_germinability
92	Can view germinability	23	view_germinability
93	Can add sample weight	24	add_sampleweight
94	Can change sample weight	24	change_sampleweight
95	Can delete sample weight	24	delete_sampleweight
96	Can view sample weight	24	view_sampleweight
97	Can add species parameter	16	add_speciesparameter
98	Can change species parameter	16	change_speciesparameter
99	Can delete species parameter	16	delete_speciesparameter
100	Can view species parameter	16	view_speciesparameter
101	Can add crop parameter	25	add_cropparameter
102	Can change crop parameter	25	change_cropparameter
103	Can delete crop parameter	25	delete_cropparameter
104	Can view crop parameter	25	view_cropparameter
105	Can add storage	26	add_storage
106	Can change storage	26	change_storage
107	Can delete storage	26	delete_storage
108	Can view storage	26	view_storage
109	Can add storage position	27	add_storageposition
110	Can change storage position	27	change_storageposition
111	Can delete storage position	27	delete_storageposition
112	Can view storage position	27	view_storageposition
113	Can add plant variety name	28	add_plantvarietyname
114	Can change plant variety name	28	change_plantvarietyname
115	Can delete plant variety name	28	delete_plantvarietyname
116	Can view plant variety name	28	view_plantvarietyname
117	Can add management type	29	add_managementtype
118	Can change management type	29	change_managementtype
119	Can delete management type	29	delete_managementtype
120	Can view management type	29	view_managementtype
121	Can add management	30	add_management
122	Can change management	30	change_management
123	Can delete management	30	delete_management
124	Can view management	30	view_management
125	Can add cart	31	add_cart
126	Can change cart	31	change_cart
127	Can delete cart	31	delete_cart
128	Can view cart	31	view_cart
129	Can add cart item	32	add_cartitem
130	Can change cart item	32	change_cartitem
131	Can delete cart item	32	delete_cartitem
132	Can view cart item	32	view_cartitem
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$260000$jDwDA8Dt72lzmIygjmnFxU$RjWHdFx+yqwkqnCxfdiJpsYFOOawMRI1qEwfKgmJt04=	2022-04-11 07:14:41.883842+00	t	kofm				t	t	2022-02-15 20:50:49.300263+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: calculator_crop; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.calculator_crop (id, notes, object_id, area_id, content_type_id) FROM stdin;
5		34	316	7
6		3	286	7
7		35	296	7
8		35	296	7
11		27	267	7
12		25	268	7
13		28	269	7
14		39	270	7
15		39	271	7
16		24	272	7
17		44	273	7
18		23	274	7
19		19	275	7
20		19	276	7
21		37	277	7
22		37	278	7
23		23	279	7
24		44	280	7
25		44	281	7
26		44	282	7
27		19	283	7
28		43	284	7
29		43	285	7
30		43	286	7
31		43	287	7
32		43	288	7
33		43	289	7
34		43	290	7
35		43	291	7
36		1	292	7
37		45	293	7
38		45	294	7
39		27	295	7
40		27	296	7
41		48	297	7
42		48	298	7
43		48	299	7
44		27	302	7
45		27	302	7
46		27	302	7
47		45	303	7
48		45	304	7
49		45	305	7
50		45	306	7
51		45	307	7
52		45	308	7
53		45	309	7
54		45	310	7
55		27	311	7
56		27	312	7
57		27	313	7
58		27	314	7
60		1	316	7
61		28	317	7
62		28	318	7
63		28	319	7
64		43	320	7
65		1	321	7
66		1	322	7
68		19	324	7
69		19	325	7
70		19	326	7
71		44	327	7
72		44	328	7
73		44	329	7
74		44	330	7
75		31	331	7
76		31	332	7
3		35	315	7
67		5	323	7
4		40	323	7
59	This is my rice crop!	6998	315	8
\.


--
-- Data for Name: calculator_cropparameter; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.calculator_cropparameter (id, value, url_ref, created_at, updated_at, crop_id, parameter_id) FROM stdin;
6	0.15	https://mater.cc	2022-03-06 21:10:56.02805+00	2022-03-06 21:10:56.028075+00	4	5
7	0.15	https://mater.cc	2022-03-06 21:10:56.033144+00	2022-03-06 21:10:56.033166+00	4	4
8	3	https://mater.cc	2022-03-06 21:10:56.037307+00	2022-03-06 21:10:56.037328+00	4	6
9	0.3	https://mater.cc	2022-03-08 21:19:21.519211+00	2022-03-08 21:19:21.519283+00	5	5
10	0.25	https://mater.cc	2022-03-08 21:19:21.535912+00	2022-03-08 21:19:21.535972+00	5	4
12	0.35	https://mater.cc	2022-03-08 21:32:15.814604+00	2022-03-08 21:32:15.814684+00	6	5
13	0.15	https://mater.cc	2022-03-08 21:32:15.830406+00	2022-03-08 21:32:15.830507+00	6	4
14	1	https://mater.cc	2022-03-08 21:32:15.844209+00	2022-03-08 21:32:15.84426+00	6	6
15	0.25	https://mater.cc	2022-03-08 23:05:47.615387+00	2022-03-08 23:05:47.615468+00	7	5
16	0.25	https://mater.cc	2022-03-08 23:05:47.630996+00	2022-03-08 23:05:47.631059+00	7	4
17	0.25	https://mater.cc	2022-03-08 23:05:48.493864+00	2022-03-08 23:05:48.493944+00	8	5
18	0.25	https://mater.cc	2022-03-08 23:05:48.511027+00	2022-03-08 23:05:48.511127+00	8	4
37	2		2022-03-19 13:33:39.134133+00	2022-03-19 13:33:39.134188+00	3	6
38	0.2		2022-03-19 13:36:23.416499+00	2022-03-19 13:36:23.416529+00	3	4
39	0.25		2022-03-19 13:36:30.251285+00	2022-03-19 13:36:30.251321+00	3	5
41	1		2022-03-20 13:15:43.405051+00	2022-03-20 13:15:43.405073+00	11	4
42	1		2022-03-20 13:15:43.410299+00	2022-03-20 13:15:43.410321+00	11	5
43	8		2022-03-20 13:15:43.41595+00	2022-03-20 13:15:43.41597+00	11	6
44	1		2022-03-20 13:15:43.424122+00	2022-03-20 13:15:43.424144+00	12	4
45	1		2022-03-20 13:15:43.429033+00	2022-03-20 13:15:43.429071+00	12	5
46	2		2022-03-20 13:15:43.435421+00	2022-03-20 13:15:43.435457+00	12	6
47	0.8		2022-03-20 13:15:43.448174+00	2022-03-20 13:15:43.448195+00	13	4
48	1		2022-03-20 13:15:43.452153+00	2022-03-20 13:15:43.45217+00	13	5
49	5		2022-03-20 13:15:43.456113+00	2022-03-20 13:15:43.456131+00	13	6
50	0.2		2022-03-20 13:15:43.464624+00	2022-03-20 13:15:43.464646+00	14	4
51	0.7		2022-03-20 13:15:43.468682+00	2022-03-20 13:15:43.468699+00	14	5
52	1		2022-03-20 13:15:43.475862+00	2022-03-20 13:15:43.475879+00	14	6
53	0.2		2022-03-20 13:15:43.503141+00	2022-03-20 13:15:43.503201+00	15	4
54	0.7		2022-03-20 13:15:43.517749+00	2022-03-20 13:15:43.517831+00	15	5
55	1		2022-03-20 13:15:43.527386+00	2022-03-20 13:15:43.527414+00	15	6
56	1		2022-03-20 13:15:43.539867+00	2022-03-20 13:15:43.53989+00	16	4
57	1		2022-03-20 13:15:43.54398+00	2022-03-20 13:15:43.544+00	16	5
58	16		2022-03-20 13:15:43.547766+00	2022-03-20 13:15:43.547783+00	16	6
59	0.5		2022-03-20 13:15:43.554277+00	2022-03-20 13:15:43.554293+00	17	4
60	0.9		2022-03-20 13:15:43.557639+00	2022-03-20 13:15:43.557654+00	17	5
61	4		2022-03-20 13:15:43.561216+00	2022-03-20 13:15:43.561233+00	17	6
62	0.5		2022-03-20 13:15:43.567695+00	2022-03-20 13:15:43.567712+00	18	4
63	0.7		2022-03-20 13:15:43.570795+00	2022-03-20 13:15:43.570809+00	18	5
64	0.5		2022-03-20 13:15:43.573821+00	2022-03-20 13:15:43.573834+00	18	6
65	0.5		2022-03-20 13:15:43.579574+00	2022-03-20 13:15:43.579589+00	19	4
66	0.5		2022-03-20 13:15:43.582625+00	2022-03-20 13:15:43.582638+00	19	5
67	2		2022-03-20 13:15:43.585597+00	2022-03-20 13:15:43.58561+00	19	6
68	0.5		2022-03-20 13:15:43.591698+00	2022-03-20 13:15:43.591713+00	20	4
69	0.5		2022-03-20 13:15:43.595219+00	2022-03-20 13:15:43.595234+00	20	5
70	2		2022-03-20 13:15:43.598718+00	2022-03-20 13:15:43.598733+00	20	6
71	0.25		2022-03-20 13:15:43.60505+00	2022-03-20 13:15:43.605065+00	21	4
72	0.25		2022-03-20 13:15:43.608022+00	2022-03-20 13:15:43.608035+00	21	5
73	1.5		2022-03-20 13:15:43.611015+00	2022-03-20 13:15:43.611028+00	21	6
74	0.25		2022-03-20 13:15:43.619568+00	2022-03-20 13:15:43.619585+00	22	4
75	0.25		2022-03-20 13:15:43.623521+00	2022-03-20 13:15:43.623538+00	22	5
76	1.5		2022-03-20 13:15:43.627465+00	2022-03-20 13:15:43.627484+00	22	6
77	0.5		2022-03-20 13:15:43.634202+00	2022-03-20 13:15:43.634218+00	23	4
78	0.7		2022-03-20 13:15:43.637736+00	2022-03-20 13:15:43.637753+00	23	5
79	0.5		2022-03-20 13:15:43.640948+00	2022-03-20 13:15:43.640961+00	23	6
80	0.5		2022-03-20 13:15:43.646714+00	2022-03-20 13:15:43.646728+00	24	4
81	0.9		2022-03-20 13:15:43.649773+00	2022-03-20 13:15:43.649787+00	24	5
82	4		2022-03-20 13:15:43.652751+00	2022-03-20 13:15:43.652765+00	24	6
83	0.5		2022-03-20 13:15:43.658706+00	2022-03-20 13:15:43.65872+00	25	4
84	0.9		2022-03-20 13:15:43.661702+00	2022-03-20 13:15:43.661716+00	25	5
85	4		2022-03-20 13:15:43.664763+00	2022-03-20 13:15:43.664777+00	25	6
86	0.5		2022-03-20 13:15:43.670496+00	2022-03-20 13:15:43.67051+00	26	4
87	0.9		2022-03-20 13:15:43.673445+00	2022-03-20 13:15:43.673458+00	26	5
88	4		2022-03-20 13:15:43.676387+00	2022-03-20 13:15:43.676399+00	26	6
89	0.5		2022-03-20 13:15:43.682163+00	2022-03-20 13:15:43.682178+00	27	4
90	0.5		2022-03-20 13:15:43.68517+00	2022-03-20 13:15:43.685183+00	27	5
91	2		2022-03-20 13:15:43.688124+00	2022-03-20 13:15:43.688137+00	27	6
92	0.4		2022-03-20 13:15:43.693818+00	2022-03-20 13:15:43.693832+00	28	4
93	1		2022-03-20 13:15:43.696868+00	2022-03-20 13:15:43.696882+00	28	5
94	3.5		2022-03-20 13:15:43.699791+00	2022-03-20 13:15:43.699804+00	28	6
95	0.4		2022-03-20 13:15:43.705635+00	2022-03-20 13:15:43.70565+00	29	4
96	1		2022-03-20 13:15:43.708563+00	2022-03-20 13:15:43.708577+00	29	5
97	3.5		2022-03-20 13:15:43.711221+00	2022-03-20 13:15:43.711234+00	29	6
98	0.4		2022-03-20 13:15:43.716584+00	2022-03-20 13:15:43.716599+00	30	4
99	1		2022-03-20 13:15:43.719625+00	2022-03-20 13:15:43.719638+00	30	5
100	3.5		2022-03-20 13:15:43.722661+00	2022-03-20 13:15:43.722674+00	30	6
101	0.4		2022-03-20 13:15:43.728353+00	2022-03-20 13:15:43.728367+00	31	4
102	1		2022-03-20 13:15:43.731381+00	2022-03-20 13:15:43.731395+00	31	5
103	3.5		2022-03-20 13:15:43.734281+00	2022-03-20 13:15:43.734295+00	31	6
104	0.4		2022-03-20 13:15:43.739713+00	2022-03-20 13:15:43.739727+00	32	4
105	1		2022-03-20 13:15:43.742332+00	2022-03-20 13:15:43.742345+00	32	5
106	3.5		2022-03-20 13:15:43.745037+00	2022-03-20 13:15:43.745049+00	32	6
107	0.4		2022-03-20 13:15:43.750271+00	2022-03-20 13:15:43.750297+00	33	4
108	1		2022-03-20 13:15:43.753363+00	2022-03-20 13:15:43.753376+00	33	5
109	3.5		2022-03-20 13:15:43.756304+00	2022-03-20 13:15:43.756317+00	33	6
110	0.4		2022-03-20 13:15:43.76224+00	2022-03-20 13:15:43.762256+00	34	4
111	1		2022-03-20 13:15:43.765385+00	2022-03-20 13:15:43.765398+00	34	5
112	3.5		2022-03-20 13:15:43.768392+00	2022-03-20 13:15:43.768405+00	34	6
113	0.4		2022-03-20 13:15:43.774213+00	2022-03-20 13:15:43.774228+00	35	4
114	1		2022-03-20 13:15:43.777196+00	2022-03-20 13:15:43.777209+00	35	5
115	3.5		2022-03-20 13:15:43.780271+00	2022-03-20 13:15:43.780296+00	35	6
116	0.2		2022-03-20 13:15:43.786067+00	2022-03-20 13:15:43.786081+00	36	4
117	0.2		2022-03-20 13:15:43.789028+00	2022-03-20 13:15:43.78904+00	36	5
118	3		2022-03-20 13:15:43.792054+00	2022-03-20 13:15:43.792068+00	36	6
119	0.4		2022-03-20 13:15:43.797923+00	2022-03-20 13:15:43.797938+00	37	4
120	0.6		2022-03-20 13:15:43.800977+00	2022-03-20 13:15:43.80099+00	37	5
121	3		2022-03-20 13:15:43.803977+00	2022-03-20 13:15:43.80399+00	37	6
122	0.4		2022-03-20 13:15:43.809979+00	2022-03-20 13:15:43.809994+00	38	4
123	0.6		2022-03-20 13:15:43.813186+00	2022-03-20 13:15:43.813201+00	38	5
124	3		2022-03-20 13:15:43.816254+00	2022-03-20 13:15:43.816268+00	38	6
125	1		2022-03-20 13:15:43.822183+00	2022-03-20 13:15:43.822198+00	39	4
126	1		2022-03-20 13:15:43.825243+00	2022-03-20 13:15:43.825257+00	39	5
127	8		2022-03-20 13:15:43.828063+00	2022-03-20 13:15:43.828076+00	39	6
128	1		2022-03-20 13:15:43.833545+00	2022-03-20 13:15:43.83356+00	40	4
129	1		2022-03-20 13:15:43.836301+00	2022-03-20 13:15:43.836315+00	40	5
130	8		2022-03-20 13:15:43.840287+00	2022-03-20 13:15:43.840304+00	40	6
131	0.03		2022-03-20 13:15:43.846206+00	2022-03-20 13:15:43.846221+00	41	4
132	0.1		2022-03-20 13:15:43.8493+00	2022-03-20 13:15:43.849314+00	41	5
133	0.3		2022-03-20 13:15:43.852262+00	2022-03-20 13:15:43.852275+00	41	6
134	0.03		2022-03-20 13:15:43.858109+00	2022-03-20 13:15:43.858126+00	42	4
135	0.1		2022-03-20 13:15:43.861209+00	2022-03-20 13:15:43.861223+00	42	5
136	0.3		2022-03-20 13:15:43.864556+00	2022-03-20 13:15:43.864572+00	42	6
137	0.03		2022-03-20 13:15:43.871678+00	2022-03-20 13:15:43.871695+00	43	4
138	0.1		2022-03-20 13:15:43.875634+00	2022-03-20 13:15:43.875651+00	43	5
139	0.3		2022-03-20 13:15:43.879682+00	2022-03-20 13:15:43.879698+00	43	6
140	1		2022-03-20 13:15:43.886603+00	2022-03-20 13:15:43.886619+00	44	4
141	1		2022-03-20 13:15:43.889978+00	2022-03-20 13:15:43.889996+00	44	5
142	8		2022-03-20 13:15:43.893513+00	2022-03-20 13:15:43.893528+00	44	6
143	1		2022-03-20 13:15:43.899482+00	2022-03-20 13:15:43.899496+00	45	4
144	1		2022-03-20 13:15:43.902472+00	2022-03-20 13:15:43.902486+00	45	5
145	8		2022-03-20 13:15:43.905461+00	2022-03-20 13:15:43.905475+00	45	6
146	1		2022-03-20 13:15:43.911254+00	2022-03-20 13:15:43.911268+00	46	4
147	1		2022-03-20 13:15:43.914592+00	2022-03-20 13:15:43.914607+00	46	5
148	8		2022-03-20 13:15:43.918034+00	2022-03-20 13:15:43.918049+00	46	6
149	0.4		2022-03-20 13:15:43.92385+00	2022-03-20 13:15:43.923864+00	47	4
150	0.6		2022-03-20 13:15:43.926948+00	2022-03-20 13:15:43.926962+00	47	5
151	3		2022-03-20 13:15:43.930253+00	2022-03-20 13:15:43.930271+00	47	6
152	0.4		2022-03-20 13:15:43.938087+00	2022-03-20 13:15:43.938103+00	48	4
153	0.6		2022-03-20 13:15:43.941435+00	2022-03-20 13:15:43.94145+00	48	5
154	3		2022-03-20 13:15:43.944726+00	2022-03-20 13:15:43.944742+00	48	6
155	0.4		2022-03-20 13:15:43.951181+00	2022-03-20 13:15:43.951196+00	49	4
156	0.6		2022-03-20 13:15:43.954238+00	2022-03-20 13:15:43.954251+00	49	5
157	3		2022-03-20 13:15:43.95719+00	2022-03-20 13:15:43.957203+00	49	6
158	0.4		2022-03-20 13:15:43.962922+00	2022-03-20 13:15:43.962937+00	50	4
159	0.6		2022-03-20 13:15:43.966004+00	2022-03-20 13:15:43.966018+00	50	5
160	3		2022-03-20 13:15:43.969046+00	2022-03-20 13:15:43.96906+00	50	6
161	0.4		2022-03-20 13:15:43.974813+00	2022-03-20 13:15:43.974828+00	51	4
162	0.6		2022-03-20 13:15:43.977936+00	2022-03-20 13:15:43.977949+00	51	5
163	3		2022-03-20 13:15:43.981059+00	2022-03-20 13:15:43.981074+00	51	6
164	0.4		2022-03-20 13:15:43.986971+00	2022-03-20 13:15:43.986986+00	52	4
165	0.6		2022-03-20 13:15:43.989761+00	2022-03-20 13:15:43.989774+00	52	5
166	3		2022-03-20 13:15:43.992411+00	2022-03-20 13:15:43.992424+00	52	6
167	0.4		2022-03-20 13:15:43.997745+00	2022-03-20 13:15:43.99776+00	53	4
168	0.6		2022-03-20 13:15:44.000686+00	2022-03-20 13:15:44.0007+00	53	5
169	3		2022-03-20 13:15:44.003551+00	2022-03-20 13:15:44.003563+00	53	6
170	0.4		2022-03-20 13:15:44.008735+00	2022-03-20 13:15:44.00875+00	54	4
171	0.6		2022-03-20 13:15:44.011507+00	2022-03-20 13:15:44.01152+00	54	5
172	3		2022-03-20 13:15:44.014263+00	2022-03-20 13:15:44.014278+00	54	6
173	1		2022-03-20 13:15:44.019624+00	2022-03-20 13:15:44.01964+00	55	4
174	1		2022-03-20 13:15:44.022478+00	2022-03-20 13:15:44.022492+00	55	5
175	8		2022-03-20 13:15:44.025355+00	2022-03-20 13:15:44.02537+00	55	6
176	1		2022-03-20 13:15:44.031053+00	2022-03-20 13:15:44.031069+00	56	4
177	1		2022-03-20 13:15:44.034186+00	2022-03-20 13:15:44.034201+00	56	5
178	8		2022-03-20 13:15:44.03722+00	2022-03-20 13:15:44.037234+00	56	6
179	1		2022-03-20 13:15:44.043826+00	2022-03-20 13:15:44.043843+00	57	4
180	1		2022-03-20 13:15:44.047783+00	2022-03-20 13:15:44.047799+00	57	5
181	8		2022-03-20 13:15:44.051174+00	2022-03-20 13:15:44.05119+00	57	6
182	1		2022-03-20 13:15:44.057232+00	2022-03-20 13:15:44.057247+00	58	4
183	1		2022-03-20 13:15:44.061182+00	2022-03-20 13:15:44.061199+00	58	5
184	8		2022-03-20 13:15:44.06549+00	2022-03-20 13:15:44.065506+00	58	6
188	0.2		2022-03-20 13:15:44.084137+00	2022-03-20 13:15:44.084152+00	60	4
189	0.2		2022-03-20 13:15:44.087097+00	2022-03-20 13:15:44.087117+00	60	5
190	3		2022-03-20 13:15:44.090212+00	2022-03-20 13:15:44.090226+00	60	6
191	0.8		2022-03-20 13:15:44.095702+00	2022-03-20 13:15:44.095716+00	61	4
192	1		2022-03-20 13:15:44.098689+00	2022-03-20 13:15:44.098704+00	61	5
193	5		2022-03-20 13:15:44.101556+00	2022-03-20 13:15:44.101568+00	61	6
194	0.8		2022-03-20 13:15:44.106977+00	2022-03-20 13:15:44.106991+00	62	4
195	1		2022-03-20 13:15:44.109733+00	2022-03-20 13:15:44.109746+00	62	5
196	5		2022-03-20 13:15:44.112632+00	2022-03-20 13:15:44.112647+00	62	6
197	0.8		2022-03-20 13:15:44.118466+00	2022-03-20 13:15:44.118481+00	63	4
198	1		2022-03-20 13:15:44.121345+00	2022-03-20 13:15:44.121358+00	63	5
199	5		2022-03-20 13:15:44.124224+00	2022-03-20 13:15:44.124238+00	63	6
200	0.4		2022-03-20 13:15:44.129857+00	2022-03-20 13:15:44.129871+00	64	4
201	1		2022-03-20 13:15:44.133128+00	2022-03-20 13:15:44.133141+00	64	5
202	3.5		2022-03-20 13:15:44.136166+00	2022-03-20 13:15:44.136178+00	64	6
203	0.2		2022-03-20 13:15:44.141949+00	2022-03-20 13:15:44.141963+00	65	4
204	0.2		2022-03-20 13:15:44.144939+00	2022-03-20 13:15:44.144952+00	65	5
205	3		2022-03-20 13:15:44.148071+00	2022-03-20 13:15:44.148085+00	65	6
206	0.2		2022-03-20 13:15:44.153979+00	2022-03-20 13:15:44.153994+00	66	4
207	0.2		2022-03-20 13:15:44.156833+00	2022-03-20 13:15:44.156846+00	66	5
208	3		2022-03-20 13:15:44.159884+00	2022-03-20 13:15:44.159897+00	66	6
212	0.5		2022-03-20 13:15:44.176633+00	2022-03-20 13:15:44.176647+00	68	4
213	0.5		2022-03-20 13:15:44.179389+00	2022-03-20 13:15:44.179403+00	68	5
214	2		2022-03-20 13:15:44.182064+00	2022-03-20 13:15:44.182077+00	68	6
215	0.5		2022-03-20 13:15:44.187477+00	2022-03-20 13:15:44.187491+00	69	4
216	0.5		2022-03-20 13:15:44.190213+00	2022-03-20 13:15:44.190225+00	69	5
217	2		2022-03-20 13:15:44.192935+00	2022-03-20 13:15:44.192948+00	69	6
218	0.5		2022-03-20 13:15:44.198657+00	2022-03-20 13:15:44.198673+00	70	4
219	0.5		2022-03-20 13:15:44.201467+00	2022-03-20 13:15:44.20148+00	70	5
221	0.5		2022-03-20 13:15:44.209385+00	2022-03-20 13:15:44.209399+00	71	4
222	0.9		2022-03-20 13:15:44.212034+00	2022-03-20 13:15:44.212047+00	71	5
223	4		2022-03-20 13:15:44.214719+00	2022-03-20 13:15:44.214733+00	71	6
224	0.5		2022-03-20 13:15:44.220099+00	2022-03-20 13:15:44.220113+00	72	4
225	0.9		2022-03-20 13:15:44.222827+00	2022-03-20 13:15:44.22284+00	72	5
226	4		2022-03-20 13:15:44.225409+00	2022-03-20 13:15:44.225423+00	72	6
227	0.5		2022-03-20 13:15:44.234366+00	2022-03-20 13:15:44.234381+00	73	4
228	0.9		2022-03-20 13:15:44.240481+00	2022-03-20 13:15:44.240495+00	73	5
229	4		2022-03-20 13:15:44.246638+00	2022-03-20 13:15:44.246652+00	73	6
230	0.5		2022-03-20 13:15:44.255781+00	2022-03-20 13:15:44.255796+00	74	4
231	0.9		2022-03-20 13:15:44.258772+00	2022-03-20 13:15:44.258785+00	74	5
232	4		2022-03-20 13:15:44.261841+00	2022-03-20 13:15:44.261854+00	74	6
233	0.25		2022-03-20 13:15:44.267717+00	2022-03-20 13:15:44.267733+00	75	4
234	0.4		2022-03-20 13:15:44.270748+00	2022-03-20 13:15:44.270763+00	75	5
235	3.5		2022-03-20 13:15:44.273776+00	2022-03-20 13:15:44.27379+00	75	6
236	0.25		2022-03-20 13:15:44.279587+00	2022-03-20 13:15:44.279603+00	76	4
237	0.4		2022-03-20 13:15:44.282666+00	2022-03-20 13:15:44.28268+00	76	5
238	3.5		2022-03-20 13:15:44.285638+00	2022-03-20 13:15:44.285652+00	76	6
265	1500	\N	2022-03-28 20:32:47.66366+00	2022-03-28 20:32:47.663715+00	62	7
266	6	\N	2022-03-28 20:34:02.431211+00	2022-03-28 20:34:02.431267+00	68	1
267	19	\N	2022-03-28 20:34:09.977565+00	2022-03-28 20:34:09.977636+00	68	2
268	27	\N	2022-03-28 20:34:16.17604+00	2022-03-28 20:34:16.17609+00	68	3
269	1500	\N	2022-03-28 20:34:29.541053+00	2022-03-28 20:34:29.541139+00	68	7
271	4	\N	2022-03-29 20:49:49.162096+00	2022-03-29 20:49:49.16212+00	66	1
251	2	\N	2022-03-24 21:33:29.22969+00	2022-03-24 21:33:29.229746+00	70	6
272	18	\N	2022-03-29 20:49:55.553472+00	2022-03-29 20:49:55.553513+00	66	2
273	30	\N	2022-03-29 20:50:00.472267+00	2022-03-29 20:50:00.47229+00	66	3
253	25	\N	2022-03-27 20:05:50.335731+00	2022-03-27 20:40:30.014319+00	18	2
274	1000	\N	2022-03-29 20:50:09.398254+00	2022-03-29 20:50:09.398275+00	66	7
275	10	\N	2022-03-29 21:03:03.54303+00	2022-03-29 21:03:03.543088+00	61	1
276	28	\N	2022-03-29 21:03:08.307694+00	2022-03-29 21:03:08.307734+00	61	2
252	12	\N	2022-03-27 20:05:43.84146+00	2022-03-27 21:11:19.006549+00	18	1
277	38	\N	2022-03-29 21:03:11.98642+00	2022-03-29 21:03:11.986479+00	61	3
278	1500	\N	2022-03-29 21:03:41.636395+00	2022-03-29 21:03:41.636418+00	61	7
254	32	\N	2022-03-27 20:06:05.301215+00	2022-03-27 21:15:41.848726+00	18	3
255	1700	\N	2022-03-27 20:06:13.007719+00	2022-03-27 21:15:53.40264+00	18	7
256	12	\N	2022-03-27 21:24:36.790031+00	2022-03-27 21:24:36.790104+00	28	1
257	28	\N	2022-03-27 21:24:44.436885+00	2022-03-27 21:24:44.436956+00	28	2
258	38	\N	2022-03-27 21:24:51.823728+00	2022-03-27 21:24:51.823793+00	28	3
259	1500	\N	2022-03-27 21:24:58.999651+00	2022-03-28 07:05:28.107763+00	28	7
279	6	\N	2022-04-02 20:36:19.478413+00	2022-04-02 20:36:19.478471+00	70	1
270	19	\N	2022-03-29 08:38:45.318825+00	2022-04-02 20:36:24.442061+00	70	2
280	27	\N	2022-04-02 20:36:28.236053+00	2022-04-02 20:36:28.236107+00	70	3
262	10	\N	2022-03-28 20:32:18.62725+00	2022-03-28 20:32:18.627301+00	62	1
263	28	\N	2022-03-28 20:32:23.548776+00	2022-03-28 20:32:23.548884+00	62	2
264	38	\N	2022-03-28 20:32:31.378643+00	2022-03-28 20:32:31.378695+00	62	3
281	1300	\N	2022-04-02 20:36:38.059967+00	2022-04-02 20:36:38.060062+00	70	7
\.


--
-- Data for Name: calculator_management; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.calculator_management (id, date, notes, type_id, crop_id) FROM stdin;
5	2022-09-01		2	59
3	2022-05-14	Primavera!!	1	59
6	2022-09-07	.	2	59
10	2022-06-24	\N	2	4
9	2022-04-04	\N	1	4
\.


--
-- Data for Name: calculator_managementtype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.calculator_managementtype (id, code, name, description) FROM stdin;
1	sowing	Sowing	Sowing
2	harvest	Harvest	
\.


--
-- Data for Name: collect_cart; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.collect_cart (id, created_at, user_id) FROM stdin;
\.


--
-- Data for Name: collect_cartitem; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.collect_cartitem (id, weight, cart_id, sample_id) FROM stdin;
\.


--
-- Data for Name: collect_germinability; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.collect_germinability (id, germinability, after_days, performed_at, seedsample_id) FROM stdin;
30	82	7	2022-03-30	1130
31	70	7	2022-03-30	1131
32	90	7	2022-03-30	1132
33	82	7	2022-03-30	1133
34	90	7	2022-03-30	1134
35	90	7	2022-03-30	1135
36	94	7	2022-03-30	1136
37	77	7	2022-03-30	1137
38	83	7	2022-03-30	1138
39	80	7	2022-03-30	1139
40	78	7	2022-03-30	1140
41	66	7	2022-03-30	1141
42	94	7	2022-03-30	1142
43	88	7	2022-03-30	1143
44	89	7	2022-03-30	1144
45	92	7	2022-03-30	1145
46	90	7	2022-03-30	1146
47	81	7	2022-03-30	1147
48	91	7	2022-03-30	1148
49	90	7	2022-03-30	1149
50	62	7	2022-03-30	1150
51	92	7	2022-03-30	1151
52	66	7	2022-03-30	1152
53	80	7	2022-03-30	1153
54	90	7	2022-03-30	1154
55	91	7	2022-03-30	1155
56	80	7	2022-03-30	1156
57	77	7	2022-03-30	1157
58	90	7	2022-03-30	1158
59	83	7	2022-03-30	1159
60	84	7	2022-03-30	1160
61	90	7	2022-03-30	1161
62	90	7	2022-03-30	1162
63	61	7	2022-03-30	1163
64	90	7	2022-03-30	1164
65	92	7	2022-03-30	1165
66	72	7	2022-03-30	1166
67	92	7	2022-03-30	1167
68	94	7	2022-03-30	1168
69	91	7	2022-03-30	1169
70	78	7	2022-03-30	1170
71	94	7	2022-03-30	1171
72	87	7	2022-03-30	1172
73	58	7	2022-03-30	1173
74	78	7	2022-03-30	1174
75	92	7	2022-03-30	1175
76	66	7	2022-03-30	1176
77	93	7	2022-03-30	1179
79	80	7	2022-03-30	1181
80	82	7	2022-03-30	1182
81	88	7	2022-03-30	1183
82	92	7	2022-03-30	1184
83	86	7	2022-03-30	1185
84	94	7	2022-03-30	1186
85	71	7	2022-03-30	1187
86	88	7	2022-03-30	1188
87	84	7	2022-03-30	1189
88	74	7	2022-03-30	1190
89	86	7	2022-03-30	1191
90	94	7	2022-03-30	1192
91	88	7	2022-03-30	1193
92	61	7	2022-03-30	1194
93	92	7	2022-03-30	1195
94	84	7	2022-03-30	1196
95	86	7	2022-03-30	1197
96	80	7	2022-03-30	1198
97	64	7	2022-03-30	1199
98	76	7	2022-03-30	1201
99	85	7	2022-03-30	1203
100	88	7	2022-03-30	1204
101	92	7	2022-03-30	1205
102	83	7	2022-03-30	1206
103	79	7	2022-03-30	1207
104	94	7	2022-03-30	1208
105	88	7	2022-03-30	1209
106	92	7	2022-03-30	1210
107	88	7	2022-03-30	1211
108	93	7	2022-03-30	1212
109	82	7	2022-03-30	1213
110	93	7	2022-03-30	1214
111	90	7	2022-03-30	1215
112	76	7	2022-03-30	1216
145	82	7	2022-04-06	1239
146	86	7	2022-04-06	1240
147	83	7	2022-04-06	1241
148	88	7	2022-04-06	1242
149	86	7	2022-04-06	1243
124	80	7	2022-04-02	1217
150	88	7	2022-04-06	1244
126	82	7	2022-04-06	1220
127	90	7	2022-04-06	1221
128	88	7	2022-04-06	1222
129	78	7	2022-04-06	1223
130	82	7	2022-04-06	1224
131	90	7	2022-04-06	1225
132	86	7	2022-04-06	1226
133	85	7	2022-04-06	1227
134	86	7	2022-04-06	1228
135	92	7	2022-04-06	1229
136	81	7	2022-04-06	1230
137	90	7	2022-04-06	1231
138	88	7	2022-04-06	1232
139	95	7	2022-04-06	1233
140	72	7	2022-04-06	1234
141	77	7	2022-04-06	1235
142	90	7	2022-04-06	1236
143	63	7	2022-04-06	1237
144	84	7	2022-04-06	1238
151	91	7	2022-04-06	1245
152	86	7	2022-04-06	1246
153	94	7	2022-04-06	1247
154	88	7	2022-04-06	1248
155	86	7	2022-04-06	1249
156	87	7	2013-01-01	1256
157	88	7	2013-01-01	1271
158	90	7	2013-04-08	1328
159	86	7	2013-04-08	1331
\.


--
-- Data for Name: collect_sampleweight; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.collect_sampleweight (id, weight, seedsample_id, created_at) FROM stdin;
4900	550	198	2022-03-29
4901	550	199	2022-03-29
4902	550	200	2022-03-29
4903	550	201	2022-03-29
4904	550	202	2022-03-29
4905	550	203	2022-03-29
4906	550	204	2022-03-29
4907	550	205	2022-03-29
4908	550	206	2022-03-29
4909	550	207	2022-03-29
4910	550	208	2022-03-29
4911	550	209	2022-03-29
4912	412	210	2022-03-29
4913	550	211	2022-03-29
4914	550	212	2022-03-29
4915	550	213	2022-03-29
4916	550	214	2022-03-29
4917	550	215	2022-03-29
4918	550	216	2022-03-29
4919	550	217	2022-03-29
4920	550	218	2022-03-29
4921	550	219	2022-03-29
4922	550	220	2022-03-29
4923	550	221	2022-03-29
4924	400	222	2022-03-29
4925	400	223	2022-03-29
4926	550	224	2022-03-29
4927	550	225	2022-03-29
4928	550	226	2022-03-29
4929	550	227	2022-03-29
4930	550	228	2022-03-29
4931	550	229	2022-03-29
4932	550	230	2022-03-29
4933	550	231	2022-03-29
4934	550	232	2022-03-29
4935	550	233	2022-03-29
4936	550	234	2022-03-29
4937	100	235	2022-03-29
4938	550	236	2022-03-29
4939	530	237	2022-03-29
4940	500	238	2022-03-29
4941	700	239	2022-03-29
4942	550	240	2022-03-29
4943	100	241	2022-03-29
4944	550	242	2022-03-29
4945	500	243	2022-03-29
4946	90	244	2022-03-29
4947	500	245	2022-03-29
4948	500	246	2022-03-29
4949	500	247	2022-03-29
4950	500	248	2022-03-29
4951	500	249	2022-03-29
4952	500	250	2022-03-29
4953	500	251	2022-03-29
4954	500	252	2022-03-29
4955	500	253	2022-03-29
4956	500	254	2022-03-29
4957	450	255	2022-03-29
4958	500	256	2022-03-29
4959	500	257	2022-03-29
4960	500	258	2022-03-29
4961	500	259	2022-03-29
4962	500	260	2022-03-29
4963	500	261	2022-03-29
4964	500	262	2022-03-29
4965	500	263	2022-03-29
4966	400	264	2022-03-29
4967	500	265	2022-03-29
4968	500	266	2022-03-29
4969	500	267	2022-03-29
4970	500	268	2022-03-29
4971	500	269	2022-03-29
4972	500	270	2022-03-29
4973	500	271	2022-03-29
4974	500	272	2022-03-29
4975	500	273	2022-03-29
4976	500	274	2022-03-29
4977	500	275	2022-03-29
4978	500	276	2022-03-29
4979	500	277	2022-03-29
4980	500	278	2022-03-29
4981	500	279	2022-03-29
4982	500	280	2022-03-29
4983	500	281	2022-03-29
4984	500	282	2022-03-29
4985	500	283	2022-03-29
4986	500	284	2022-03-29
4987	500	285	2022-03-29
4988	500	286	2022-03-29
4989	500	287	2022-03-29
4990	500	288	2022-03-29
4991	500	289	2022-03-29
4992	500	290	2022-03-29
4993	500	291	2022-03-29
4994	500	292	2022-03-29
4995	500	293	2022-03-29
4996	500	294	2022-03-29
4997	500	295	2022-03-29
4998	500	296	2022-03-29
4999	500	297	2022-03-29
5000	500	298	2022-03-29
5001	500	299	2022-03-29
5002	500	300	2022-03-29
5003	500	301	2022-03-29
5004	500	302	2022-03-29
5005	500	303	2022-03-29
5006	500	304	2022-03-29
5007	500	305	2022-03-29
5008	500	306	2022-03-29
5009	500	307	2022-03-29
5010	500	308	2022-03-29
5011	500	309	2022-03-29
5012	500	310	2022-03-29
5013	500	311	2022-03-29
5014	500	312	2022-03-29
5015	500	313	2022-03-29
5016	500	314	2022-03-29
5017	500	315	2022-03-29
5018	500	316	2022-03-29
5019	500	317	2022-03-29
5020	500	318	2022-03-29
5021	500	319	2022-03-29
5022	500	320	2022-03-29
5023	500	321	2022-03-29
5024	500	322	2022-03-29
5025	500	323	2022-03-29
5026	400	324	2022-03-29
5027	500	325	2022-03-29
5028	500	326	2022-03-29
5029	500	327	2022-03-29
5030	300	328	2022-03-29
5031	500	329	2022-03-29
5032	500	330	2022-03-29
5033	500	331	2022-03-29
5034	500	332	2022-03-29
5035	500	333	2022-03-29
5036	500	334	2022-03-29
5037	500	335	2022-03-29
5038	500	336	2022-03-29
5039	500	337	2022-03-29
5040	500	338	2022-03-29
5041	500	339	2022-03-29
5042	500	340	2022-03-29
5043	500	341	2022-03-29
5044	500	342	2022-03-29
5045	500	343	2022-03-29
5046	350	344	2022-03-29
5047	500	345	2022-03-29
5048	500	346	2022-03-29
5049	500	347	2022-03-29
5050	500	348	2022-03-29
5051	250	349	2022-03-29
5052	500	350	2022-03-29
5053	200	351	2022-03-29
5054	500	352	2022-03-29
5055	500	353	2022-03-29
5056	500	354	2022-03-29
5057	500	355	2022-03-29
5058	500	356	2022-03-29
5059	500	357	2022-03-29
5060	500	358	2022-03-29
5061	500	359	2022-03-29
5062	500	360	2022-03-29
5063	500	361	2022-03-29
5064	501	362	2022-03-29
5065	502	363	2022-03-29
5066	503	364	2022-03-29
5067	504	365	2022-03-29
5068	505	366	2022-03-29
5069	506	367	2022-03-29
5070	50	368	2022-03-29
5071	100	369	2022-03-29
5072	290	370	2022-03-29
5073	290	371	2022-03-29
5074	550	372	2022-03-29
5075	500	373	2022-03-29
5076	500	374	2022-03-29
5077	500	375	2022-03-29
5078	100	376	2022-03-29
5079	450	377	2022-03-29
5080	500	378	2022-03-29
5081	150	379	2022-03-29
5082	150	380	2022-03-29
5083	250	381	2022-03-29
5084	450	382	2022-03-29
5085	500	383	2022-03-29
5086	100	384	2022-03-29
5087	350	385	2022-03-29
5088	600	386	2022-03-29
5089	80	387	2022-03-29
5090	40	388	2022-03-29
5091	500	389	2022-03-29
5092	500	390	2022-03-29
5093	500	391	2022-03-29
5094	500	392	2022-03-29
5095	500	393	2022-03-29
5096	500	394	2022-03-29
5097	500	395	2022-03-29
5098	200	396	2022-03-29
5099	500	397	2022-03-29
5100	500	398	2022-03-29
5101	400	399	2022-03-29
5102	500	400	2022-03-29
5103	500	401	2022-03-29
5104	500	402	2022-03-29
5105	500	403	2022-03-29
5106	190	404	2022-03-29
5107	500	405	2022-03-29
5108	500	406	2022-03-29
5109	500	407	2022-03-29
5110	500	408	2022-03-29
5111	500	409	2022-03-29
5112	500	410	2022-03-29
5113	500	411	2022-03-29
5114	500	412	2022-03-29
5115	500	413	2022-03-29
5116	500	414	2022-03-29
5117	500	415	2022-03-29
5118	450	416	2022-03-29
5119	300	417	2022-03-29
5120	450	418	2022-03-29
5121	200	419	2022-03-29
5122	500	420	2022-03-29
5123	500	421	2022-03-29
5124	300	422	2022-03-29
5125	450	423	2022-03-29
5126	500	424	2022-03-29
5127	200	425	2022-03-29
5128	500	426	2022-03-29
5129	500	427	2022-03-29
5130	350	428	2022-03-29
5131	500	429	2022-03-29
5132	500	430	2022-03-29
5133	500	431	2022-03-29
5134	200	432	2022-03-29
5135	300	433	2022-03-29
5136	500	434	2022-03-29
5137	500	435	2022-03-29
5138	300	436	2022-03-29
5139	450	437	2022-03-29
5140	500	438	2022-03-29
5141	300	439	2022-03-29
5142	500	440	2022-03-29
5143	500	441	2022-03-29
5144	500	442	2022-03-29
5145	500	443	2022-03-29
5146	500	444	2022-03-29
5147	900	445	2022-03-29
5148	500	446	2022-03-29
5149	320	447	2022-03-29
5150	550	448	2022-03-29
5151	200	449	2022-03-29
5152	400	450	2022-03-29
5153	500	451	2022-03-29
5154	600	452	2022-03-29
5155	600	453	2022-03-29
5156	500	454	2022-03-29
5157	500	455	2022-03-29
5158	500	456	2022-03-29
5159	500	457	2022-03-29
5160	500	458	2022-03-29
5161	500	459	2022-03-29
5162	70	460	2022-03-29
5163	400	461	2022-03-29
5164	500	462	2022-03-29
5165	200	463	2022-03-29
5166	40	464	2022-03-29
5167	400	465	2022-03-29
5168	600	466	2022-03-29
5169	400	467	2022-03-29
5170	600	468	2022-03-29
5171	300	469	2022-03-29
5172	600	470	2022-03-29
5173	300	471	2022-03-29
5174	500	472	2022-03-29
5175	500	473	2022-03-29
5176	270	474	2022-03-29
5177	500	475	2022-03-29
5178	80	476	2022-03-29
5179	500	477	2022-03-29
5180	260	478	2022-03-29
5181	500	479	2022-03-29
5182	400	480	2022-03-29
5183	470	481	2022-03-29
5184	330	482	2022-03-29
5185	480	483	2022-03-29
5186	350	484	2022-03-29
5187	500	485	2022-03-29
5188	380	486	2022-03-29
5189	500	487	2022-03-29
5190	500	488	2022-03-29
5191	500	489	2022-03-29
5192	500	490	2022-03-29
5193	500	491	2022-03-29
5194	500	492	2022-03-29
5195	500	493	2022-03-29
5196	260	494	2022-03-29
5197	500	495	2022-03-29
5198	400	496	2022-03-29
5199	380	497	2022-03-29
5200	500	498	2022-03-29
5201	420	499	2022-03-29
5202	930	500	2022-03-29
5203	580	501	2022-03-29
5204	500	502	2022-03-29
5205	340	503	2022-03-29
5206	500	504	2022-03-29
5207	500	505	2022-03-29
5208	500	506	2022-03-29
5209	500	507	2022-03-29
5210	500	508	2022-03-29
5211	500	509	2022-03-29
5212	500	510	2022-03-29
5213	500	511	2022-03-29
5214	500	512	2022-03-29
5215	500	513	2022-03-29
5216	500	514	2022-03-29
5217	500	515	2022-03-29
5218	500	516	2022-03-29
5219	500	517	2022-03-29
5220	500	518	2022-03-29
5221	500	519	2022-03-29
5222	500	520	2022-03-29
5223	500	521	2022-03-29
5224	500	522	2022-03-29
5225	450	523	2022-03-29
5226	500	524	2022-03-29
5227	500	525	2022-03-29
5228	500	526	2022-03-29
5229	500	527	2022-03-29
5230	500	528	2022-03-29
5231	500	529	2022-03-29
5232	150	530	2022-03-29
5233	170	531	2022-03-29
5234	500	532	2022-03-29
5235	350	533	2022-03-29
5236	500	534	2022-03-29
5237	NaN	535	2022-03-29
5238	600	536	2022-03-29
5239	450	537	2022-03-29
5240	450	538	2022-03-29
5241	500	539	2022-03-29
5242	600	540	2022-03-29
5243	600	541	2022-03-29
5244	600	542	2022-03-29
5245	500	543	2022-03-29
5246	300	544	2022-03-29
5247	500	545	2022-03-29
5248	600	546	2022-03-29
5249	300	547	2022-03-29
5250	700	548	2022-03-29
5251	450	549	2022-03-29
5252	450	550	2022-03-29
5253	328	551	2022-03-29
5254	500	552	2022-03-29
5255	150	553	2022-03-29
5256	300	554	2022-03-29
5257	300	555	2022-03-29
5258	500	556	2022-03-29
5259	450	557	2022-03-29
5260	500	558	2022-03-29
5261	250	559	2022-03-29
5262	250	560	2022-03-29
5263	600	561	2022-03-29
5264	400	562	2022-03-29
5265	250	563	2022-03-29
5266	600	564	2022-03-29
5267	600	565	2022-03-29
5268	600	566	2022-03-29
5269	500	567	2022-03-29
5270	500	568	2022-03-29
5271	600	569	2022-03-29
5272	300	570	2022-03-29
5273	250	571	2022-03-29
5274	500	572	2022-03-29
5275	500	573	2022-03-29
5276	500	574	2022-03-29
5277	450	575	2022-03-29
5278	400	576	2022-03-29
5279	600	577	2022-03-29
5280	450	578	2022-03-29
5281	500	579	2022-03-29
5282	600	580	2022-03-29
5283	500	581	2022-03-29
5284	600	582	2022-03-29
5285	500	583	2022-03-29
5286	600	584	2022-03-29
5287	500	585	2022-03-29
5288	400	586	2022-03-29
5289	600	587	2022-03-29
5290	500	588	2022-03-29
5291	430	589	2022-03-29
5292	450	590	2022-03-29
5293	600	591	2022-03-29
5294	300	592	2022-03-29
5295	550	593	2022-03-29
5296	600	594	2022-03-29
5297	600	595	2022-03-29
5298	400	596	2022-03-29
5299	500	597	2022-03-29
5300	550	598	2022-03-29
5301	500	599	2022-03-29
5302	600	600	2022-03-29
5303	100	601	2022-03-29
5304	1000	602	2022-03-29
5305	900	603	2022-03-29
5306	900	604	2022-03-29
5307	900	605	2022-03-29
5308	900	606	2022-03-29
5309	900	607	2022-03-29
5310	950	608	2022-03-29
5311	800	609	2022-03-29
5312	1000	610	2022-03-29
5313	1000	611	2022-03-29
5314	900	612	2022-03-29
5315	950	613	2022-03-29
5316	950	614	2022-03-29
5317	900	615	2022-03-29
5318	600	616	2022-03-29
5319	800	617	2022-03-29
5320	1000	618	2022-03-29
5321	600	619	2022-03-29
5322	500	620	2022-03-29
5323	650	621	2022-03-29
5324	700	622	2022-03-29
5325	650	623	2022-03-29
5326	800	624	2022-03-29
5327	250	625	2022-03-29
5328	600	626	2022-03-29
5329	400	627	2022-03-29
5330	600	628	2022-03-29
5331	700	629	2022-03-29
5332	700	630	2022-03-29
5333	650	631	2022-03-29
5334	800	632	2022-03-29
5335	650	633	2022-03-29
5336	600	634	2022-03-29
5337	500	635	2022-03-29
5338	500	636	2022-03-29
5339	500	637	2022-03-29
5340	650	638	2022-03-29
5341	450	639	2022-03-29
5342	500	640	2022-03-29
5343	650	641	2022-03-29
5344	700	642	2022-03-29
5345	750	643	2022-03-29
5346	700	644	2022-03-29
5347	600	645	2022-03-29
5348	600	646	2022-03-29
5349	700	647	2022-03-29
5350	800	648	2022-03-29
5351	600	649	2022-03-29
5352	700	650	2022-03-29
5353	730	651	2022-03-29
5354	1000	652	2022-03-29
5355	650	653	2022-03-29
5356	700	654	2022-03-29
5357	700	655	2022-03-29
5358	800	656	2022-03-29
5359	850	657	2022-03-29
5360	800	658	2022-03-29
5361	700	659	2022-03-29
5362	600	660	2022-03-29
5363	350	661	2022-03-29
5364	700	662	2022-03-29
5365	700	663	2022-03-29
5366	700	664	2022-03-29
5367	510	665	2022-03-29
5368	700	666	2022-03-29
5369	300	667	2022-03-29
5370	620	668	2022-03-29
5371	730	669	2022-03-29
5372	700	670	2022-03-29
5373	750	671	2022-03-29
5374	630	672	2022-03-29
5375	650	673	2022-03-29
5376	670	674	2022-03-29
5377	700	675	2022-03-29
5378	600	676	2022-03-29
5379	600	677	2022-03-29
5380	700	678	2022-03-29
5381	700	679	2022-03-29
5382	650	680	2022-03-29
5383	550	681	2022-03-29
5384	500	682	2022-03-29
5385	520	683	2022-03-29
5386	550	684	2022-03-29
5387	450	685	2022-03-29
5388	730	686	2022-03-29
5389	650	687	2022-03-29
5390	700	688	2022-03-29
5391	450	689	2022-03-29
5392	550	690	2022-03-29
5393	750	691	2022-03-29
5394	700	692	2022-03-29
5395	750	693	2022-03-29
5396	550	694	2022-03-29
5397	300	695	2022-03-29
5398	620	696	2022-03-29
5399	540	697	2022-03-29
5400	300	698	2022-03-29
5401	550	699	2022-03-29
5402	250	700	2022-03-29
5403	450	701	2022-03-29
5404	500	702	2022-03-29
5405	1000	703	2022-03-29
5406	1000	704	2022-03-29
5407	1000	705	2022-03-29
5408	1000	706	2022-03-29
5409	1000	707	2022-03-29
5410	1000	708	2022-03-29
5411	1000	709	2022-03-29
5412	1000	710	2022-03-29
5413	1000	711	2022-03-29
5414	1000	712	2022-03-29
5415	1000	713	2022-03-29
5416	1000	714	2022-03-29
5417	1000	715	2022-03-29
5418	1000	716	2022-03-29
5419	1000	717	2022-03-29
5420	1000	718	2022-03-29
5421	1000	719	2022-03-29
5422	1000	720	2022-03-29
5423	1000	721	2022-03-29
5424	1000	722	2022-03-29
5425	1000	723	2022-03-29
5426	1000	724	2022-03-29
5427	1000	725	2022-03-29
5428	1000	726	2022-03-29
5429	600	727	2022-03-29
5430	600	728	2022-03-29
5431	600	729	2022-03-29
5432	600	730	2022-03-29
5433	600	731	2022-03-29
5434	600	732	2022-03-29
5435	600	733	2022-03-29
5436	600	734	2022-03-29
5437	600	735	2022-03-29
5438	600	736	2022-03-29
5439	600	737	2022-03-29
5440	600	738	2022-03-29
5441	600	739	2022-03-29
5442	600	740	2022-03-29
5443	600	741	2022-03-29
5444	600	742	2022-03-29
5445	600	743	2022-03-29
5446	600	744	2022-03-29
5447	600	745	2022-03-29
5448	600	746	2022-03-29
5449	600	747	2022-03-29
5450	600	748	2022-03-29
5451	600	749	2022-03-29
5452	600	750	2022-03-29
5453	600	751	2022-03-29
5454	600	752	2022-03-29
5455	600	753	2022-03-29
5456	600	754	2022-03-29
5457	600	755	2022-03-29
5458	600	756	2022-03-29
5459	600	757	2022-03-29
5460	600	758	2022-03-29
5461	600	759	2022-03-29
5462	600	760	2022-03-29
5463	600	761	2022-03-29
5464	600	762	2022-03-29
5465	600	763	2022-03-29
5466	600	764	2022-03-29
5467	600	765	2022-03-29
5468	600	766	2022-03-29
5469	600	767	2022-03-29
5470	600	768	2022-03-29
5471	600	769	2022-03-29
5472	600	770	2022-03-29
5473	600	771	2022-03-29
5474	600	772	2022-03-29
5475	600	773	2022-03-29
5476	600	774	2022-03-29
5477	600	775	2022-03-29
5478	600	776	2022-03-29
5479	600	777	2022-03-29
5480	600	778	2022-03-29
5481	600	779	2022-03-29
5482	600	780	2022-03-29
5483	600	781	2022-03-29
5484	600	782	2022-03-29
5485	600	783	2022-03-29
5486	600	784	2022-03-29
5487	600	785	2022-03-29
5488	600	786	2022-03-29
5489	600	787	2022-03-29
5490	600	788	2022-03-29
5491	600	789	2022-03-29
5492	600	790	2022-03-29
5493	600	791	2022-03-29
5494	600	792	2022-03-29
5495	600	793	2022-03-29
5496	600	794	2022-03-29
5497	600	795	2022-03-29
5498	600	796	2022-03-29
5499	600	797	2022-03-29
5500	600	798	2022-03-29
5501	600	799	2022-03-29
5502	600	800	2022-03-29
5503	600	801	2022-03-29
5504	600	802	2022-03-29
5505	600	803	2022-03-29
5506	600	804	2022-03-29
5507	600	805	2022-03-29
5508	600	806	2022-03-29
5509	600	807	2022-03-29
5510	600	808	2022-03-29
5511	600	809	2022-03-29
5512	600	810	2022-03-29
5513	600	811	2022-03-29
5514	600	812	2022-03-29
5515	600	813	2022-03-29
5516	600	814	2022-03-29
5517	600	815	2022-03-29
5518	600	816	2022-03-29
5519	600	817	2022-03-29
5520	600	818	2022-03-29
5521	600	819	2022-03-29
5522	600	820	2022-03-29
5523	600	821	2022-03-29
5524	600	822	2022-03-29
5525	NaN	823	2022-03-29
5526	NaN	824	2022-03-29
5527	NaN	825	2022-03-29
5528	NaN	826	2022-03-29
5529	600	827	2022-03-29
5530	600	828	2022-03-29
5531	600	829	2022-03-29
5532	600	830	2022-03-29
5533	600	831	2022-03-29
5534	470	832	2022-03-29
5535	500	833	2022-03-29
5536	200	834	2022-03-29
5537	600	835	2022-03-29
5538	230	836	2022-03-29
5539	600	837	2022-03-29
5540	600	838	2022-03-29
5541	600	839	2022-03-29
5542	400	840	2022-03-29
5543	530	841	2022-03-29
5544	100	842	2022-03-29
5545	500	843	2022-03-29
5546	500	844	2022-03-29
5547	445	845	2022-03-29
5548	500	846	2022-03-29
5549	600	847	2022-03-29
5550	580	848	2022-03-29
5551	300	849	2022-03-29
5552	200	850	2022-03-29
5553	580	851	2022-03-29
5554	600	852	2022-03-29
5555	300	853	2022-03-29
5556	600	854	2022-03-29
5557	600	855	2022-03-29
5558	600	856	2022-03-29
5559	600	857	2022-03-29
5560	600	858	2022-03-29
5561	400	859	2022-03-29
5562	600	860	2022-03-29
5563	600	861	2022-03-29
5564	600	862	2022-03-29
5565	600	863	2022-03-29
5566	600	864	2022-03-29
5567	600	865	2022-03-29
5568	600	866	2022-03-29
5569	600	867	2022-03-29
5570	600	868	2022-03-29
5571	600	869	2022-03-29
5572	500	870	2022-03-29
5573	300	871	2022-03-29
5574	500	872	2022-03-29
5575	500	873	2022-03-29
5576	300	874	2022-03-29
5577	500	875	2022-03-29
5578	400	876	2022-03-29
5579	500	877	2022-03-29
5580	500	878	2022-03-29
5581	500	879	2022-03-29
5582	500	880	2022-03-29
5583	600	881	2022-03-29
5584	600	882	2022-03-29
5585	500	883	2022-03-29
5586	500	884	2022-03-29
5587	600	885	2022-03-29
5588	400	886	2022-03-29
5589	100	887	2022-03-29
5590	600	888	2022-03-29
5591	500	889	2022-03-29
5592	500	890	2022-03-29
5593	500	891	2022-03-29
5594	500	892	2022-03-29
5595	500	893	2022-03-29
5596	500	894	2022-03-29
5597	600	895	2022-03-29
5598	50	896	2022-03-29
5599	50	897	2022-03-29
5600	500	898	2022-03-29
5601	600	899	2022-03-29
5602	600	900	2022-03-29
5603	600	901	2022-03-29
5604	600	902	2022-03-29
5605	200	903	2022-03-29
5606	600	904	2022-03-29
5607	600	905	2022-03-29
5608	600	906	2022-03-29
5609	600	907	2022-03-29
5610	600	908	2022-03-29
5611	600	909	2022-03-29
5612	600	910	2022-03-29
5613	50	911	2022-03-29
5614	300	912	2022-03-29
5615	500	913	2022-03-29
5616	600	914	2022-03-29
5617	10	915	2022-03-29
5618	600	916	2022-03-29
5619	600	917	2022-03-29
5620	600	918	2022-03-29
5621	600	919	2022-03-29
5622	600	920	2022-03-29
5623	600	921	2022-03-29
5624	600	922	2022-03-29
5625	600	923	2022-03-29
5626	600	924	2022-03-29
5627	600	925	2022-03-29
5628	600	926	2022-03-29
5629	600	927	2022-03-29
5630	600	928	2022-03-29
5631	600	929	2022-03-29
5632	600	930	2022-03-29
5633	600	931	2022-03-29
5634	600	932	2022-03-29
5635	600	933	2022-03-29
5636	600	934	2022-03-29
5637	600	935	2022-03-29
5638	600	936	2022-03-29
5639	500	937	2022-03-29
5640	600	938	2022-03-29
5641	600	939	2022-03-29
5642	600	940	2022-03-29
5643	400	941	2022-03-29
5644	600	942	2022-03-29
5645	300	943	2022-03-29
5646	600	944	2022-03-29
5647	600	945	2022-03-29
5648	600	946	2022-03-29
5649	600	947	2022-03-29
5650	600	948	2022-03-29
5651	600	949	2022-03-29
5652	200	950	2022-03-29
5653	600	951	2022-03-29
5654	600	952	2022-03-29
5655	600	953	2022-03-29
5656	600	954	2022-03-29
5657	600	955	2022-03-29
5658	600	956	2022-03-29
5659	600	957	2022-03-29
5660	600	958	2022-03-29
5661	600	959	2022-03-29
5662	600	960	2022-03-29
5663	600	961	2022-03-29
5664	600	962	2022-03-29
5665	600	963	2022-03-29
5666	600	964	2022-03-29
5667	600	965	2022-03-29
5668	400	966	2022-03-29
5669	400	967	2022-03-29
5670	200	968	2022-03-29
5671	600	969	2022-03-29
5672	600	970	2022-03-29
5673	600	971	2022-03-29
5674	400	972	2022-03-29
5675	600	973	2022-03-29
5676	600	974	2022-03-29
5677	600	975	2022-03-29
5678	400	976	2022-03-29
5679	400	977	2022-03-29
5680	600	978	2022-03-29
5681	600	979	2022-03-29
5682	400	980	2022-03-29
5683	600	981	2022-03-29
5684	600	982	2022-03-29
5685	600	983	2022-03-29
5686	600	984	2022-03-29
5687	600	985	2022-03-29
5688	600	986	2022-03-29
5689	300	987	2022-03-29
5690	600	988	2022-03-29
5691	400	989	2022-03-29
5692	400	990	2022-03-29
5693	500	991	2022-03-29
5694	600	992	2022-03-29
5695	600	993	2022-03-29
5696	600	994	2022-03-29
5697	600	995	2022-03-29
5698	600	996	2022-03-29
5699	600	997	2022-03-29
5700	600	998	2022-03-29
5701	600	999	2022-03-29
5702	600	1000	2022-03-29
5703	600	1001	2022-03-29
5704	600	1002	2022-03-29
5705	600	1003	2022-03-29
5706	600	1004	2022-03-29
5707	600	1005	2022-03-29
5708	600	1006	2022-03-29
5709	600	1007	2022-03-29
5710	600	1008	2022-03-29
5711	600	1009	2022-03-29
5712	600	1010	2022-03-29
5713	600	1011	2022-03-29
5714	600	1012	2022-03-29
5715	600	1013	2022-03-29
5716	600	1014	2022-03-29
5717	600	1015	2022-03-29
5718	600	1016	2022-03-29
5719	600	1017	2022-03-29
5720	600	1018	2022-03-29
5721	600	1019	2022-03-29
5722	600	1020	2022-03-29
5723	600	1021	2022-03-29
5724	600	1022	2022-03-29
5725	600	1023	2022-03-29
5726	600	1024	2022-03-29
5727	600	1025	2022-03-29
5728	600	1026	2022-03-29
5729	600	1027	2022-03-29
5730	600	1028	2022-03-29
5731	600	1029	2022-03-29
5732	500	1030	2022-03-29
5733	600	1031	2022-03-29
5734	600	1032	2022-03-29
5735	700	1033	2022-03-29
5736	500	1034	2022-03-29
5737	600	1035	2022-03-29
5738	600	1036	2022-03-29
5739	350	1037	2022-03-29
5740	600	1038	2022-03-29
5741	600	1039	2022-03-29
5742	500	1040	2022-03-29
5743	600	1041	2022-03-29
5744	600	1042	2022-03-29
5745	600	1043	2022-03-29
5746	600	1044	2022-03-29
5747	600	1045	2022-03-29
5748	600	1046	2022-03-29
5749	500	1047	2022-03-29
5750	600	1048	2022-03-29
5751	600	1049	2022-03-29
5752	600	1050	2022-03-29
5753	580	1051	2022-03-29
5754	560	1052	2022-03-29
5755	500	1053	2022-03-29
5756	500	1054	2022-03-29
5757	600	1055	2022-03-29
5758	100	1056	2022-03-29
5759	400	1057	2022-03-29
5760	500	1058	2022-03-29
5761	240	1059	2022-03-29
5762	180	1060	2022-03-29
5763	500	1061	2022-03-29
5764	200	1062	2022-03-29
5765	50	1063	2022-03-29
5766	200	1064	2022-03-29
5767	600	1065	2022-03-29
5768	600	1066	2022-03-29
5769	600	1067	2022-03-29
5770	600	1068	2022-03-29
5771	400	1069	2022-03-29
5772	600	1070	2022-03-29
5773	600	1071	2022-03-29
5774	600	1072	2022-03-29
5775	600	1073	2022-03-29
5776	500	1074	2022-03-29
5777	500	1075	2022-03-29
5778	500	1076	2022-03-29
5779	600	1077	2022-03-29
5780	500	1078	2022-03-29
5781	100	1079	2022-03-29
5782	100	1080	2022-03-29
5783	400	1081	2022-03-29
5784	500	1082	2022-03-29
5785	100	1083	2022-03-29
5786	600	1084	2022-03-29
5787	500	1085	2022-03-29
5788	600	1086	2022-03-29
5789	500	1087	2022-03-29
5790	100	1088	2022-03-29
5791	500	1089	2022-03-29
5792	600	1090	2022-03-29
5793	600	1091	2022-03-29
5794	200	1092	2022-03-29
5795	500	1093	2022-03-29
5796	600	1094	2022-03-29
5797	400	1095	2022-03-29
5798	500	1096	2022-03-29
5799	300	1097	2022-03-29
5800	500	1098	2022-03-29
5801	600	1099	2022-03-29
5802	600	1100	2022-03-29
5803	600	1101	2022-03-29
5804	600	1102	2022-03-29
5805	600	1103	2022-03-29
5806	600	1104	2022-03-29
5807	600	1105	2022-03-29
5808	600	1106	2022-03-29
5809	600	1107	2022-03-29
5810	600	1108	2022-03-29
5811	600	1109	2022-03-29
5812	500	1110	2022-03-29
5813	600	1111	2022-03-29
5814	600	1112	2022-03-29
5815	600	1113	2022-03-29
5816	500	1114	2022-03-29
5817	600	1115	2022-03-29
5818	600	1116	2022-03-29
5833	500	1130	2022-03-30
5834	350	1131	2022-03-30
5835	327	1132	2022-03-30
5836	510	1133	2022-03-30
5837	285	1134	2022-03-30
5838	520	1135	2022-03-30
5839	475	1136	2022-03-30
5840	430	1137	2022-03-30
5841	455	1138	2022-03-30
5842	620	1139	2022-03-30
5843	380	1140	2022-03-30
5844	500	1141	2022-03-30
5845	410	1142	2022-03-30
5846	560	1143	2022-03-30
5847	400	1144	2022-03-30
5848	325	1145	2022-03-30
5849	450	1146	2022-03-30
5850	255	1147	2022-03-30
5851	515	1148	2022-03-30
5852	450	1149	2022-03-30
5853	450	1150	2022-03-30
5854	470	1151	2022-03-30
5855	280	1152	2022-03-30
5856	380	1153	2022-03-30
5857	450	1154	2022-03-30
5858	550	1155	2022-03-30
5859	440	1156	2022-03-30
5860	490	1157	2022-03-30
5861	480	1158	2022-03-30
5862	425	1159	2022-03-30
5863	475	1160	2022-03-30
5864	240	1161	2022-03-30
5865	300	1162	2022-03-30
5866	215	1163	2022-03-30
5867	355	1164	2022-03-30
5868	225	1165	2022-03-30
5869	285	1166	2022-03-30
5870	410	1167	2022-03-30
5871	340	1168	2022-03-30
5872	485	1169	2022-03-30
5873	365	1170	2022-03-30
5874	410	1171	2022-03-30
5875	510	1172	2022-03-30
5876	300	1173	2022-03-30
5877	360	1174	2022-03-30
5878	435	1175	2022-03-30
5879	150	1176	2022-03-30
5882	210	1179	2022-03-30
5884	375	1181	2022-03-30
5885	425	1182	2022-03-30
5886	140	1183	2022-03-30
5887	210	1184	2022-03-30
5888	590	1185	2022-03-30
5889	445	1186	2022-03-30
5890	520	1187	2022-03-30
5891	475	1188	2022-03-30
5892	500	1189	2022-03-30
5893	475	1190	2022-03-30
5894	500	1191	2022-03-30
5895	565	1192	2022-03-30
5896	330	1193	2022-03-30
5897	95	1194	2022-03-30
5898	50	1195	2022-03-30
5899	410	1196	2022-03-30
5900	345	1197	2022-03-30
5901	560	1198	2022-03-30
5902	590	1199	2022-03-30
5903	255	1200	2022-03-30
5904	540	1201	2022-03-30
5905	530	1202	2022-03-30
5906	320	1203	2022-03-30
5907	235	1204	2022-03-30
5908	225	1205	2022-03-30
5909	500	1206	2022-03-30
5910	450	1207	2022-03-30
5911	320	1208	2022-03-30
5912	260	1209	2022-03-30
5913	265	1210	2022-03-30
5914	415	1211	2022-03-30
5915	215	1212	2022-03-30
5916	325	1213	2022-03-30
5917	360	1214	2022-03-30
5918	515	1215	2022-03-30
5919	420	1216	2022-03-30
5920	215	1217	2022-03-30
5988	640	1279	2022-04-06
5989	470	1280	2022-04-06
5990	600	1281	2022-04-06
5991	535	1282	2022-04-06
5992	618	1283	2022-04-06
5993	585	1284	2022-04-06
5929	400	1220	2022-04-06
5930	450	1221	2022-04-06
5931	440	1222	2022-04-06
5932	420	1223	2022-04-06
5933	520	1224	2022-04-06
5934	465	1225	2022-04-06
5935	540	1226	2022-04-06
5936	384	1227	2022-04-06
5937	470	1228	2022-04-06
5938	422	1229	2022-04-06
5939	496	1230	2022-04-06
5940	441	1231	2022-04-06
5941	600	1232	2022-04-06
5942	394	1233	2022-04-06
5943	475	1234	2022-04-06
5944	375	1235	2022-04-06
5945	350	1236	2022-04-06
5946	445	1237	2022-04-06
5947	370	1238	2022-04-06
5948	371	1239	2022-04-06
5949	650	1240	2022-04-06
5950	325	1241	2022-04-06
5951	325	1242	2022-04-06
5952	450	1243	2022-04-06
5953	142	1244	2022-04-06
5954	320	1245	2022-04-06
5955	240	1246	2022-04-06
5956	366	1247	2022-04-06
5957	475	1248	2022-04-06
5958	480	1249	2022-04-06
5959	535	1250	2022-04-06
5960	510	1251	2022-04-06
5961	230	1252	2022-04-06
5962	675	1253	2022-04-06
5963	470	1254	2022-04-06
5964	170	1255	2022-04-06
5965	355	1256	2022-04-06
5966	480	1257	2022-04-06
5967	650	1258	2022-04-06
5968	480	1259	2022-04-06
5969	770	1260	2022-04-06
5970	525	1261	2022-04-06
5971	530	1262	2022-04-06
5972	470	1263	2022-04-06
5973	500	1264	2022-04-06
5974	700	1265	2022-04-06
5975	400	1266	2022-04-06
5976	380	1267	2022-04-06
5977	480	1268	2022-04-06
5978	636	1269	2022-04-06
5979	480	1270	2022-04-06
5980	200	1271	2022-04-06
5981	630	1272	2022-04-06
5982	640	1273	2022-04-06
5983	640	1274	2022-04-06
5984	640	1275	2022-04-06
5985	640	1276	2022-04-06
5986	635	1277	2022-04-06
5987	640	1278	2022-04-06
5994	630	1285	2022-04-06
5995	500	1286	2022-04-06
5996	600	1287	2022-04-06
5997	530	1288	2022-04-06
5998	510	1289	2022-04-06
5999	700	1290	2022-04-06
6000	510	1291	2022-04-06
6001	540	1292	2022-04-06
6002	500	1293	2022-04-06
6003	510	1294	2022-04-06
6004	560	1295	2022-04-06
6005	500	1296	2022-04-06
6006	200	1297	2022-04-07
6007	530	1298	2022-04-07
6008	570	1299	2022-04-07
6009	600	1300	2022-04-07
6010	530	1301	2022-04-07
6011	490	1302	2022-04-07
6012	640	1303	2022-04-07
6013	434	1304	2022-04-07
6014	642	1305	2022-04-07
6015	560	1306	2022-04-07
6016	580	1307	2022-04-07
6017	410	1308	2022-04-07
6018	610	1309	2022-04-07
6019	510	1310	2022-04-07
6020	520	1311	2022-04-07
6021	550	1312	2022-04-07
6022	630	1313	2022-04-07
6023	600	1314	2022-04-07
6024	650	1315	2022-04-07
6025	560	1316	2022-04-07
6026	450	221	2022-04-07
6027	450	1021	2022-04-07
6028	350	455	2022-04-07
6029	450	1086	2022-04-07
6030	450	646	2022-04-07
6031	485	1277	2022-04-08
6032	475	771	2022-04-08
6033	526	638	2022-04-08
6034	200	1317	2022-04-08
6035	648	1318	2022-04-08
6036	240	1319	2022-04-08
6037	550	1320	2022-04-08
6038	200	1321	2022-04-08
6039	550	1322	2022-04-08
6040	525	1323	2022-04-08
6041	500	1324	2022-04-08
6042	225	1325	2022-04-08
6043	650	1326	2022-04-08
6044	550	1327	2022-04-08
6045	350	1328	2022-04-08
6046	625	1329	2022-04-08
6047	350	1330	2022-04-08
6048	100	1331	2022-04-08
6049	495	1332	2022-04-08
6050	120	665	2022-04-08
6051	325	1333	2022-04-08
6052	640	1334	2022-04-08
6053	475	1335	2022-04-08
6054	515	1336	2022-04-08
6055	625	1337	2022-04-08
6056	525	1338	2022-04-08
6057	620	1339	2022-04-08
6058	465	1340	2022-04-08
6059	615	1341	2022-04-08
6060	500	1342	2022-04-08
6061	500	1343	2022-04-08
6124	750	1357	2022-04-13
6125	700	1358	2022-04-13
6126	640	1359	2022-04-13
6127	775	1360	2022-04-13
6128	825	1361	2022-04-13
6129	550	1362	2022-04-13
6068	400	198	2022-04-13
6069	400	200	2022-04-13
6070	400	205	2022-04-13
6071	400	206	2022-04-13
6072	400	207	2022-04-13
6073	400	211	2022-04-13
6074	400	224	2022-04-13
6075	350	294	2022-04-13
6076	350	431	2022-04-13
6077	150	469	2022-04-13
6078	350	504	2022-04-13
6079	350	524	2022-04-13
6080	200	533	2022-04-13
6081	250	562	2022-04-13
6082	350	567	2022-04-13
6083	500	631	2022-04-13
6084	500	653	2022-04-13
6085	550	654	2022-04-13
6086	650	656	2022-04-13
6087	470	668	2022-04-13
6088	550	675	2022-04-13
6089	850	726	2022-04-13
6090	450	732	2022-04-13
6091	450	818	2022-04-13
6092	450	819	2022-04-13
6093	450	847	2022-04-13
6094	450	914	2022-04-13
6095	450	949	2022-04-13
6096	450	954	2022-04-13
6097	450	983	2022-04-13
6098	150	987	2022-04-13
6099	450	992	2022-04-13
6100	450	996	2022-04-13
6101	450	1000	2022-04-13
6102	450	1003	2022-04-13
6103	450	1005	2022-04-13
6104	450	1009	2022-04-13
6105	450	1050	2022-04-13
6106	450	1065	2022-04-13
6107	325	1160	2022-04-13
6108	325	1190	2022-04-13
6109	320	1254	2022-04-13
6110	490	1275	2022-04-13
6111	480	1285	2022-04-13
6112	675	1345	2022-04-13
6113	765	1346	2022-04-13
6114	840	1347	2022-04-13
6115	100	1348	2022-04-13
6116	515	1349	2022-04-13
6117	700	1350	2022-04-13
6118	550	1351	2022-04-13
6119	750	1352	2022-04-13
6120	700	1353	2022-04-13
6121	675	1354	2022-04-13
6122	790	1355	2022-04-13
6123	675	1356	2022-04-13
6134	740	1367	2022-04-13
6135	730	1368	2022-04-13
6136	775	1369	2022-04-13
6137	700	1370	2022-04-13
\.


--
-- Data for Name: collect_seedsample; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.collect_seedsample (id, notes, growing_season, variety_id, position_id, sample_id) FROM stdin;
198		2020	6778	6087	1
199		2020	7053	6088	2
200		2020	6852	6089	3
201		2020	6742	6090	4
202		2020	7086	6091	5
203		2020	7482	6092	6
204		2020	6805	6093	7
205		2020	6783	6094	8
206		2020	6760	6095	9
207		2020	6872	6096	10
208		2020	6878	6097	11
209		2020	6838	6098	12
210		2020	7038	6099	13
211		2020	7128	6100	14
212		2020	7484	6101	15
213		2020	7059	6102	16
214		2020	7491	6103	17
215		2020	7492	6104	18
216		2020	6883	6105	19
217		2020	7013	6106	20
218		2020	6882	6107	21
219		2020	6946	6108	22
220		2020	6936	6109	23
221		2020	6887	6110	24
222		2020	7486	6111	25
223		2020	7489	6112	26
224		2020	7019	6113	27
225		2020	6858	6114	28
226		2020	6916	6115	29
227		2020	6998	6116	30
228		2020	7002	6117	31
229		2020	7017	6118	32
230		2020	7487	6119	33
231		2009	6994	6120	34
232		2014	6969	6121	35
233		2018	7003	6122	36
234		2009	6993	6123	37
235		2008	6992	6124	38
236		2013	7221	6125	39
237		2009	6991	6126	40
238		2017	6934	6127	41
239		2014	7050	6128	42
240		2017	6989	6129	43
241		2008	6995	6130	44
242		2018	6758	6131	45
243		2015	7046	6132	46
244		2018	6990	6133	47
245		2014	6869	6134	48
246		2017	7373	6135	49
247		2017	6864	6136	50
248		2018	6859	6137	51
249		2016	6929	6138	52
250		2017	6895	6139	53
251		2017	6862	6140	54
252		2017	7375	6141	55
253		2018	7141	6142	56
254		2017	7374	6143	57
255		2013	6906	6144	58
256		2017	6853	6145	59
257		2013	6765	6146	60
258		2014	6861	6147	61
259		2013	6829	6148	62
260		2016	7261	6149	63
261		2018	6914	6150	64
262		2017	6918	6151	65
263		2014	6835	6152	66
264		2014	7223	6153	67
265		2018	7175	6154	68
266		2014	6768	6155	69
267		2016	6911	6156	70
268		2014	6844	6157	71
269		2014	6841	6158	72
270		2014	7260	6159	73
271		2015	7300	6160	74
272		2017	6897	6161	75
273		2013	6892	6162	76
274		2013	6781	6163	77
275		2014	6773	6164	78
276		2017	6723	6165	79
277		2017	6728	6166	80
278		2016	7045	6167	81
279		2016	6729	6168	82
280		2016	6762	6169	83
281		2013	6764	6170	84
282		2017	6774	6171	85
283		2017	6759	6172	86
284		2014	7262	6173	87
285		2016	7333	6174	88
286		2017	6958	6175	89
287		2016	6954	6176	90
288		2016	7334	6177	91
289		2014	7020	6178	92
290		2018	7150	6179	93
291		2014	6930	6180	94
292		2016	7336	6181	95
293		2016	7337	6182	96
294		2018	7113	6183	97
295		2018	7127	6184	98
296		2016	7331	6185	99
297		2016	7332	6186	100
298		2018	7114	6187	101
299		2015	7302	6188	102
300		2017	7117	6189	103
301		2017	7121	6190	104
302		2013	6816	6191	105
303		2014	6819	6192	106
304		2014	6889	6193	107
305		2018	7118	6194	108
306		2014	7211	6195	109
307		2015	7309	6196	110
308		2012	7112	6197	111
309		2018	7110	6198	112
310		2017	7213	6199	113
311		2018	7134	6200	114
312		2017	7156	6201	115
313		2018	7140	6202	116
314		2018	7132	6203	117
315		2018	7136	6204	118
316		2018	7139	6205	119
317		2017	7138	6206	120
318		2013	6886	6207	121
319		2018	7097	6208	122
320		2018	7154	6209	123
321		2017	7143	6210	124
322		2018	7111	6211	125
323		2018	7091	6212	126
324		2018	7093	6213	127
325		2017	7147	6214	128
326		2018	7102	6215	129
327		2018	7094	6216	130
328		2018	7103	6217	132
329		2018	7096	6218	133
330		2017	7109	6219	134
331		2017	7098	6220	135
332		2017	7105	6221	136
333		2017	7115	6222	137
334		2017	7090	6223	138
335		2017	7101	6224	139
336		2017	7106	6225	140
337		2018	7379	6226	141
338		2018	6754	6227	142
339		2017	6996	6228	143
340		2016	7329	6229	144
341		2014	7249	6230	145
342		2018	7399	6231	146
343		2016	6974	6232	147
344		2018	7397	6233	148
345		2016	6981	6234	149
346		2018	7422	6235	150
347		2018	7424	6236	151
348		2018	7401	6237	152
349		2018	6901	6238	153
350		2015	7248	6239	154
351		2012	7632	6240	155
352		2018	7420	6241	156
353		2018	7419	6242	157
354		2018	7421	6243	158
355		2016	7318	6244	159
356		2015	7313	6245	160
357		2018	7400	6246	161
358		2016	7307	6247	162
359		2015	7311	6248	163
360		2016	7320	6249	164
361		2016	7319	6250	165
362		2018	7423	6251	166
363		2016	7335	6252	167
364		2018	7398	6253	168
365		2016	7321	6254	169
366		2018	7407	6255	170
367		2018	7408	6256	171
368		2011	6953	6257	172
369		2011	7277	6258	173
370	Parentale F ECCO 63	2011	6953	6259	174
371	Parentale M ECCO 63	2011	7243	6259	180
372		2018	7633	6260	175
373	Parentale F ECCO51CL	2012	7242	6261	176
374		2014	7241	6262	177
375		2012	7242	6263	178
376		\N	6952	6264	179
377		2016	7243	6265	181
378	Parentale M ECCO 61	2012	7243	6266	182
379	Parentale F ECCO 51 CL	2011	7242	6267	183
380	Parentale M ECCO51 CL	2011	7241	6268	184
381		2014	6952	6269	185
382		2011	6953	6270	186
383		2018	7404	6271	187
384		\N	7634	6272	188
385		2011	7634	6273	189
386		2014	7277	6274	190
387	Parentale F CLXL729	\N	7634	6275	191
388	Parentale F CLXL745	\N	6953	6276	192
389		2014	6798	6277	193
390		2014	7054	6278	194
391		2014	6899	6279	195
392		2016	6868	6280	196
393		2017	6813	6281	197
394		2016	6809	6282	198
395		2014	6808	6283	199
396		\N	6983	6284	200
397		2013	6792	6285	201
398		2016	7056	6286	202
399		2017	7129	6287	203
400		2016	6767	6288	204
401		2014	7259	6289	205
402		2018	6828	6290	206
403		2017	7131	6291	207
404		2009	6984	6292	208
405		2015	6999	6293	209
406		2014	6962	6294	210
407		2014	6978	6295	211
408		2014	7025	6296	212
409		2016	6944	6297	213
410		2018	7008	6298	214
411		2015	7049	6299	215
412		2018	7004	6300	216
413		2016	7052	6301	217
414	Verificare con Thai	2018	7002	6302	218
415		2014	7258	6303	219
416		2012	7012	6304	220
417		2014	7013	6305	221
418		2014	6913	6306	232
419		2013	6917	6307	233
420		2013	7071	6308	234
421		2016	6927	6309	235
422		2013	7328	6310	236
423		2013	6924	6311	237
424		2016	7180	6312	238
425		2015	6928	6313	239
426		2013	6935	6314	240
427		2015	6933	6315	241
428		2013	6758	6316	242
429		2016	6932	6317	243
430		2015	7078	6318	244
431		2017	7234	6319	245
432		2014	7275	6320	246
433		2016	6880	6321	247
434		2017	7168	6322	222
435		2017	7235	6323	223
436		2015	7635	6324	224
437		2016	7077	6325	225
438		2017	6908	6326	226
439		2018	6916	6327	227
440		2015	6923	6328	228
441		2016	7068	6329	229
442		2015	6926	6330	230
443		2016	6931	6331	231
444		2015	7072	6332	248
445		2014	6875	6333	249
446		2016	6898	6334	250
447		2014	6920	6335	251
448		2015	6863	6336	252
449		2013	6872	6337	253
450		2013	7226	6338	254
451		2016	6867	6339	256
452		2016	6884	6340	257
453		2015	6873	6341	258
454		2014	6888	6342	259
455		2015	6894	6343	260
456		2018	7232	6344	261
457		2013	6887	6345	262
458		2015	6877	6346	263
459		2018	6882	6347	264
460		2013	6885	6348	265
461		2013	6883	6349	266
462		2013	6896	6350	267
463		2015	6878	6351	268
464		2014	6909	6352	269
465		2015	6786	6353	278
466		2015	6785	6354	279
467		2018	7233	6355	280
468		2015	6776	6356	281
469		2018	6779	6357	282
470		2018	6780	6358	283
471		2015	7086	6359	284
472		2016	6782	6360	285
473		2018	6801	6361	286
474		2013	6783	6362	287
475		2013	6834	6363	288
476		2013	6789	6364	289
477		2018	6796	6365	290
478		2010	6793	6366	291
479		2015	6794	6367	292
480		2015	7085	6368	293
481		2016	7122	6369	294
482		2013	6802	6370	295
483		2016	7116	6371	296
484		2013	6790	6372	297
485		2013	6804	6373	298
486		2013	6778	6374	299
487		2017	6800	6375	300
488		2015	7087	6376	301
489		2015	7082	6377	302
490		2013	6803	6378	303
491		2015	7084	6379	304
492		2017	7228	6380	305
493		2014	6787	6381	306
494		2015	7079	6382	307
495		2017	7065	6383	308
496		2016	7161	6384	309
497		2016	7062	6385	310
498		2014	6845	6386	311
499		2017	7231	6387	312
500		2014	6846	6388	313
501		2017	7230	6389	314
502		2014	6907	6390	315
503		2013	6850	6391	316
504		2017	6848	6392	317
505		2016	6851	6393	318
506		2016	6843	6394	319
507		2015	6854	6395	320
508		2018	6839	6396	321
509		2017	6842	6397	322
510		2015	6847	6398	323
511		2014	6836	6399	324
512		2015	6831	6400	325
513		2017	7229	6401	326
514		2015	7080	6402	327
515		2015	7081	6403	328
516		2016	7133	6404	329
517		2017	6825	6405	330
518		2018	6820	6406	331
519		2015	7083	6407	332
520		2017	6826	6408	333
521		2017	6725	6409	334
522		2015	6739	6410	335
523		2015	7073	6411	336
524		2017	6737	6412	337
525		2015	6740	6413	338
526		2015	6830	6414	339
527		2014	6731	6415	340
528		2013	6727	6416	341
529		2016	6732	6417	347
530		2013	6735	6418	342
531		2012	7238	6419	343
532		2013	6821	6420	344
533		2014	6736	6421	345
534		2015	6730	6422	346
535		2014	6818	6423	349
536		2015	6824	6424	350
537		2012	7239	6425	351
538		2014	6817	6426	352
539		2018	6822	6427	353
541		2015	6750	6429	355
542		2015	6749	6430	356
543		2018	6746	6431	357
544		2011	7126	6432	358
545		2014	7276	6433	359
546		2018	6753	6434	360
547		2014	7274	6435	361
548		2018	6745	6436	362
549		2013	6741	6437	363
550		2014	6748	6438	364
551		2015	7276	6439	365
552		2018	6823	6440	366
553		2014	7265	6441	367
554		2013	6742	6442	368
555		2013	6747	6443	369
556		2013	6752	6444	370
557		2013	7245	6445	371
558		2014	7267	6446	372
559		2014	7244	6447	373
560		2014	7269	6448	374
561		2018	6814	6449	375
562		2018	7112	6450	376
563		2014	7268	6451	377
564		2017	6815	6452	378
565		2015	6806	6453	379
566		2017	7264	6454	380
567		2018	7227	6455	381
568		2013	6760	6456	382
569		2017	6770	6457	383
570		2013	6805	6458	384
571		2015	7130	6459	385
572		2016	7030	6460	386
573		2014	6769	6461	387
574		2018	6810	6462	388
575		2013	6766	6463	389
576		2013	6757	6464	390
577		2018	6761	6465	391
578		2013	6807	6466	392
579		2017	7135	6467	393
580		2018	7148	6468	394
581		2017	7195	6469	395
582		2018	7149	6470	396
583		2018	7196	6471	397
584		2018	7147	6472	398
585		2018	7152	6473	399
586		2018	7200	6474	400
587		2017	7189	6475	401
588		2018	7172	6476	402
589		2017	7186	6477	403
590		2017	7187	6478	404
591		2017	7184	6479	405
592		2018	7188	6480	406
593		2018	6920	6481	407
594		2017	7178	6482	408
595		2018	7176	6483	409
596		2018	7181	6484	410
597		2018	7194	6485	411
598		2018	7170	6486	412
599		2017	7193	6487	413
600		2017	7182	6488	414
601		2018	7171	6489	415
602	Registro 2015	2015	7298	6490	416
603	Controllare che non sia Re CL	2015	7293	6491	417
604		2015	7292	6492	418
605		2015	7314	6493	419
606	Presentata in iscrizione come Verelè	2015	6746	6494	420
607		2015	7297	6495	421
608		2015	7291	6496	422
609		2015	7281	6497	423
610		2015	7282	6498	424
611		2015	7296	6499	425
612		2015	7287	6500	426
613		2015	7284	6501	427
614		2015	7294	6502	428
615		2015	7285	6503	429
616	Registro 2016	2016	7293	6504	430
617	Registro 2016	2016	7387	6505	431
618	Registro 2016, ex Aurelio	2016	7338	6506	432
620	Allegato G 2016	2016	7246	6508	434
621	Allegato G 2016	2016	7211	6509	435
622	Registro 2016	2016	7349	6510	436
623	Registro 2016	2016	7342	6511	437
624	Registro 2016	2016	7361	6512	438
625	Registro 2016, Controllare con Marchese CL	2016	7344	6513	439
627	Registro 2016	2016	7273	6515	441
628	Registro 2016	2016	7382	6516	442
629	Registro 2016	2016	7636	6517	443
630	Registro 2016	2016	7460	6518	444
631	Registro 2016	2016	7285	6519	445
632	Registro 2016	2016	7350	6520	446
633	Registro 2016	2016	7347	6521	447
634	Registro 2016	2016	7287	6522	448
635	Registro 2016	2016	7271	6523	449
636	Allegato G 2016	2016	7212	6531	450
637	Allegato G 2016	2016	7309	6524	451
638	Registro 2016	2016	7288	6525	452
639	Registro 2016	2016	7304	6526	453
640	Registro 2016	2016	7637	6527	454
641	Registro 2016	2016	7295	6528	455
642	Registro 2016	2016	7314	6529	456
643	Registro 2016	2016	7281	6530	457
644	Registro 2016	2016	7284	6532	458
645	Registro 2016	2016	7291	6533	459
646	Registro 2016	2016	7283	6534	460
647	Registro 2016	2016	7303	6535	461
648	Registro 2016	2016	7292	6536	462
649	Registro 2016	2016	7298	6537	463
650	Registro 2016	2016	7346	6538	464
651	Registro 2016	2016	7280	6539	465
653	Registro 2016	2016	7282	6541	467
654	Registro 2016	2016	7297	6542	468
655	Registro 2016	2016	7294	6543	469
656	Registro 2016	2016	6742	6544	470
657	Registro 2016	2016	7296	6545	471
658	Registro 2016	2016	7341	6546	472
660	Registro 2018	2018	7368	6548	474
661	Registro 2018	2018	7415	6549	475
662	Registro 2018	2018	7411	6550	476
663	Registro 2018	2018	7351	6551	477
664		2021	7395	6552	480
665		2021	7395	6553	481
666	Registro 2018	2018	7359	6554	482
667	Registro 2018	2018	7414	6555	483
652	Registro 2016	2015	7339	6540	466
659	Registro 2018	2017	7355	6547	473
626	Registro 2016	2015	7289	6514	440
668	Registro 2018	2018	7360	6556	484
669	Registro 2018	2018	7353	6557	485
670	Registro 2018	2018	7377	6558	486
671	Registro 2018	2018	7352	6559	487
672	Registro 2018	2018	7354	6560	488
673	Registro 2018	2018	7387	6561	489
674	Registro 2018	2018	7367	6562	490
675	Registro 2018	2018	7356	6563	491
676	Registro 2018	2018	7365	6564	492
677	Registro 2018	2018	7362	6565	493
678	Registro 2018	2018	7389	6566	494
679	Registro 2018	2018	7358	6567	495
680	Registro 2018	2018	7357	6568	496
681	Registro 2018	2018	7404	6569	497
682	Registro 2018	2018	7405	6570	498
683	Registro 2018	2018	7409	6571	499
684	Registro 2018	2018	7406	6572	500
685	Registro 2018, RFH282	2018	7418	6573	501
686	Registro 2018	2018	7278	6574	503
687	Registro 2018	2018	7384	6575	504
688	Registro 2018	2018	7425	6576	505
689	Registro 2018	2018	7413	6577	506
690	Registro 2018	2018	7417	6578	507
691	Registro 2018	2018	7416	6579	508
692	Registro 2018	2018	7390	6580	509
693	Registro 2018	2018	7388	6581	510
694	Registro 2018	2018	7382	6582	511
695	Registro 2018	2018	7638	6583	512
696	Registro 2018	2018	7385	6584	513
697	Registro 2018	\N	7408	6585	514
698	Registro 2018	\N	7383	6586	515
699	Registro 2018	\N	7407	6587	516
700	Registro 2018	\N	7386	6588	517
701	Inew 2021	2021	7639	6589	518
702	Registro 2018	2018	7412	6590	502
703	2R/19	2018	7447	6591	519
704	9R/18	2020	7389	6592	520
705	44R/20	2020	7498	6593	521
706	30R/20	2020	7469	6594	522
707	20R/21	2020	7518	6595	523
708	33R/21	2020	7521	6596	524
709	2c/21	2020	7384	6597	525
710	11R/21	2020	7533	6598	526
711	13R/19	2020	7454	6599	527
712	49R/20	2020	7473	6600	528
713	28R/21	2020	7531	6601	529
714	57C/20	2020	7495	6602	530
715	35R/19	2020	7432	6603	531
716	37R/21	2020	7509	6604	532
717	8R/21	2020	7517	6605	533
718	2R/21	2020	7516	6606	534
719	29R/20	2020	7507	6607	535
720	46R/20	2020	7466	6608	536
721	53R/20	2020	7480	6609	537
722	15R/21	2020	7527	6610	538
723	16R/21	2020	7519	6611	539
724	7R/21	2020	7525	6612	540
725	1R/19 (INEW)	2018	7431	6613	541
726	1R/19	2020	7431	6614	542
727	22R/19	2018	7443	6615	543
728	17R/21	2018	7528	6616	544
729	15R/19	2018	7449	6617	545
730	12R/19	2018	7452	6618	546
731	21R/19 (INEW)	2018	7435	6619	547
732	17R/19	2018	7458	6620	548
733	11P/19	2018	7640	6621	549
734	32R/19	2018	7438	6622	550
735	35R/19 (Inew)	2018	7432	6623	551
736	33R/19	2018	7457	6624	552
737	7P/19	2018	7439	6625	553
738	22R/19	2018	7443	6626	554
739	24R/19	2018	7444	6627	555
740	57C/20	2018	7495	6628	556
741	31R/20	2018	7462	6629	557
742	20R/20	2018	7475	6630	558
743	34R/20	2018	7504	6631	559
744	10R/20	2018	7472	6632	560
745	46R/20	2018	7466	6633	561
746	9R/20	2018	7474	6634	562
747	19R/20	2018	7468	6635	563
748	52R/20	2018	7479	6636	564
749	8R/20	2018	7477	6637	565
750	38R/20	2018	7505	6638	566
751	3R/20	2018	7478	6639	567
753	42R/20	2018	7470	6641	569
754	14R/20	2018	7476	6642	570
755	55R/20	2018	7481	6643	571
756	25R/20	2018	7467	6644	572
757	56R/20	2018	7464	6645	573
758	29R/20	2018	7507	6646	574
759	40R/20	2018	7501	6647	575
760	45R/20	2018	7465	6648	576
761	49R/20	2018	7473	6649	577
762	26R/20	2018	7506	6650	578
763	53R/20	2018	7480	6651	579
764	51R/20	2018	7496	6652	580
765	44R/20	2018	7498	6653	581
766	54R/20	2018	7641	6654	582
767	30R/20	2018	7469	6655	583
768	50R/20	2018	7497	6656	584
769	48R/20	2018	7502	6657	585
770	18R/19	2018	7436	6658	586
771	6R/18	2018	7383	6659	587
772	11R/19	2018	7442	6660	588
773	16R/19	2018	7429	6661	589
774	10P/19	2018	7642	6662	590
775	37R/19	2018	7451	6663	591
776	20R/18	2018	7413	6664	592
777	2R/19 (Inew)	2018	7447	6665	593
778	6C/19	2018	7446	6666	594
779	28R/19	2018	7456	6667	595
780	36R/19	2018	7459	6668	596
781	9P/19	2018	7440	6669	597
782	23R/19	2018	7450	6670	598
783	5R/18	2018	7418	6671	599
784	7r/18	2018	7278	6672	600
785	23R/19	2018	7450	6673	601
786	7C/19	2018	7448	6674	602
787	8P/19	2018	7441	6675	603
788	10P/19	2018	7642	6676	604
789	5C/19	2018	7437	6677	605
790	24R/19	2018	7444	6678	606
791	10R/21	2020	7524	6679	607
792	1RE/21	2020	6784	6680	608
793	51R/20	2020	7496	6681	609
794	26R/20	2020	7506	6682	610
795	48R/20	2020	7502	6683	611
796	23R/21	2020	7529	6684	612
797	13R/21	2020	7514	6685	613
798	22R/21	2020	7510	6686	614
799	1C/21	2020	7643	6687	615
800	25R/20	2020	7467	6688	616
801	28R/19	2020	7456	6689	617
802	32R/21	2020	7520	6690	618
803	31R/20	2020	7462	6691	619
804	12R/21	2020	7523	6692	620
805	27R/21	2020	7532	6693	621
806	40R/20	2020	7501	6694	622
807	24R/21	2020	7530	6695	623
808	5R/21	2020	7513	6696	624
809	18R/21	2020	7522	6697	625
810	39R/20	2020	7499	6698	626
811	6R/21	2020	7515	6699	627
812	3R/21	2020	7512	6700	628
813	2RE/21	2020	6975	6701	629
814	19R/21	2020	7644	6702	630
815	47R/20	2020	7503	6703	631
816	41R/20	2020	7500	6704	632
817	14R/21	2020	7526	6705	633
818	38R/20	2020	7505	6706	634
819	34R/20	2020	7504	6707	635
820	33R/19	2020	7457	6708	636
821	52R/20	2020	7479	6709	637
822	45R/20	2020	7465	6710	638
823	11P/19	2018	7640	6711	639
824	27R/19	2020	7453	6713	641
825	4R/21	2020	7508	6714	642
826	21R/21	2020	7511	6715	643
827		2017	6921	6716	644
828		2016	6891	6717	645
829		2018	7204	6718	646
830		2018	7014	6719	647
831		2014	7645	6720	648
832		2013	6959	6721	649
833		2014	6857	6722	650
834		2014	6942	6723	651
835		2014	7270	6724	652
836		2013	6919	6725	653
837		2010	7646	6726	654
838		2013	7210	6983	655
839		2016	7042	6984	656
840		2011	7043	6985	657
841		2014	6876	6986	658
842		2014	6937	6987	659
843		2014	6797	6988	660
844		2013	6837	6989	661
845		2014	6865	6990	662
846		2013	6912	6991	663
847		2014	7359	6992	664
848		2016	7325	6993	665
849		2018	7169	6994	666
850		2013	6849	6995	667
851		2016	7330	6996	668
852		2017	7166	6997	669
853		2017	7167	6998	670
854		2018	7162	6999	671
855		2017	7164	7000	672
856		2017	6849	7001	673
857		2017	7058	7002	674
858		2016	7124	7003	675
859		2013	6791	7004	676
860		2017	6771	7005	677
861		2015	7035	7006	678
862		2015	7299	7007	679
863		2016	7039	7008	680
864		2015	6775	7009	681
865		2018	7206	7010	682
866		2015	7279	7011	683
867		2017	7051	7012	684
868		2015	7647	7013	685
869		2016	7088	7014	686
870		2013	7209	7015	687
871		2013	7648	7016	688
874		2013	7119	7019	691
875		2012	7208	7020	692
876		2013	7650	7021	693
877		2013	6722	7022	694
878		2011	7651	7023	695
879		2014	7001	7024	696
880		2016	7652	7025	697
881		2016	6972	7026	698
882		2012	7653	7027	699
883		2014	6925	7028	700
884		2014	7652	7029	701
885		\N	7059	7030	702
886		2013	7061	7031	703
887		2018	7104	7032	704
888		2016	7060	7033	705
889		2016	7038	7034	706
890		2014	7063	7035	707
891		2013	7044	7036	708
892		2018	7120	7037	709
893		2014	7037	7038	710
894	9R/15	2015	7272	7039	711
895		2017	7142	7040	712
896		2013	7041	7041	713
897		2014	7272	7042	714
898		2014	7288	7043	715
899		2015	6941	7044	716
900		2016	7040	7045	717
901		2015	6734	7046	718
902		2016	6856	7047	719
872	\N	2013	6879	7017	689
903		2014	7266	7048	720
904		2015	6939	7049	721
905		2015	6948	7050	722
906		2017	7190	7051	723
907		2016	7057	7052	724
908		2016	7029	7053	725
909		2013	7263	7054	726
910		2013	6950	7055	727
911		2013	6947	7056	728
912		2013	7236	7057	729
913		2014	6945	7058	730
914		2018	6949	7059	731
915		2014	6946	7060	732
916	19R/18	2017	7390	7061	733
917	6R/18	2017	7383	7062	734
918	30R/19	2018	7433	7063	735
919	4R/18	2017	7388	7064	736
920	27R/19	2018	7453	7065	737
921	2P/18	2017	7407	7066	738
922	31R/19	2018	7445	7067	739
923	2G/19	2018	7393	7068	740
924	13R/19	2018	7454	7069	741
925	10R/18	2018	7385	7070	742
926	2C/18	2018	7412	7071	743
927	1G/19	2018	7359	7072	744
928	8P/19	2018	7441	7073	745
929		2020	7044	7074	746
930		2020	6801	7075	747
931		2020	6761	7076	748
932		2020	6730	7077	749
933	21R/19	2019	7435	7078	750
934		2020	7227	7079	751
935	16R/15	2014	7286	7080	752
936		2020	7485	7081	753
937		2020	7488	7082	754
938		2020	6753	7083	755
939		2020	6758	7084	756
940		2020	7104	7085	757
941		2020	7483	7086	758
942		2020	6779	7087	759
943		2015	7299	7088	760
944	BST1	2019	7452	7089	761
945		2019	7463	7090	762
946	Standard	\N	6909	7091	763
947	5G	2018	6909	7092	764
948		\N	6810	7093	765
950		2016	7343	7095	767
951	7R/18	2019	7278	7096	768
952		2019	7458	7097	769
953	5C/19	2019	7437	7098	770
954	9R/18	2019	7389	7099	771
955	6C/19	2019	7446	7100	772
956	60C/20	2019	7638	7101	773
957	Standard	\N	6909	7102	774
958		2012	7403	7103	775
959		2015	7304	7104	776
960		2012	7123	7105	777
961		2015	7303	7106	778
962		2012	7095	7107	779
963		2014	7067	7108	780
964		2013	7356	7109	781
965		2014	7654	7110	782
966		2014	7655	7111	783
967		2013	7271	7112	784
968		2017	7642	7113	785
969		2015	7257	7114	786
970		2018	7183	7115	787
971		2016	7069	7116	788
972		2011	7656	7117	789
973		2014	6726	7118	790
974		2016	7034	7119	791
975		2017	7657	7120	792
976		2016	7202	7121	793
977		2018	7391	7122	794
978		2015	7028	7123	795
979		2017	7240	7124	796
980		2014	6881	7125	797
981		2020	7012	7126	798
982		2020	6969	7127	799
983		2020	6885	7128	800
984		2020	6894	7129	801
985		2020	6955	7130	802
986		2020	6835	7131	803
987		2020	7011	7132	804
988		2020	6886	7133	805
989		2020	7112	7134	806
990		2020	6906	7135	807
991		2020	7007	7136	808
992		2020	6784	7137	809
993		2020	7245	7138	810
994		2020	6909	7139	811
995	1G/20	2019	7413	7140	812
996		2020	7436	7141	813
997		2020	6980	7142	814
998	33R/19	2019	7457	7143	815
999		2020	7023	7144	816
1000	2R/19	2019	7447	7145	817
1001		2020	6975	7146	818
1002	27R/19	2019	7453	7147	819
1003	59C/20	2019	7362	7148	820
1004	24R/15	2014	7279	7149	821
1005	15R/19	2019	7449	7150	822
1006	35R/19	2019	7432	7151	823
1007	32R/19	2019	7438	7152	824
1008	36R/19	2019	7459	7153	825
1009		2015	7017	7154	826
1010	1C/18	2018	7417	7155	827
1011	3R/18	2018	7386	7156	828
1012	4C/18	2018	7384	7157	829
1013	1P/18	2017	7408	7158	830
1014	20R/18	2018	7413	7159	831
1015	3P/18	2017	7406	7160	832
1016	32RC/15	2018	7276	7161	833
1017	7P/19	2018	7439	7162	834
1018	5R/18	2018	7418	7163	835
1019	3C/18	2018	7416	7164	836
1020	8R/18	2018	7638	7165	837
1021	25R/18	2018	7382	7166	838
1022	9P/19	2018	7440	7167	839
1023	26R/19	2018	7434	7168	840
1024	14R/18	2018	7425	7169	841
1025	34R/19 I (new)	2018	7430	7170	842
1026	1RE/19	2018	7015	7171	843
1027	2RE/19	2018	6941	7172	844
1028	29R/19	2018	7455	7173	845
1029		2018	6900	7174	846
1030		2017	6874	7175	847
1031		2018	6915	7176	848
1032		2017	6871	7177	849
1033		2014	6795	7178	850
1034		2013	7658	7179	851
1035		2015	7177	7180	852
1036		2017	7214	7181	853
1037		2012	6743	7182	854
1038		2018	6890	7183	855
1039		2017	7024	7184	856
1040		2013	6811	7185	857
1041		2018	6902	7186	858
1042		2018	6951	7187	859
1043		2015	7246	7188	860
1044		2015	7165	7189	861
1045		2018	7403	7190	862
1046		2017	6827	7191	863
1047		2016	7048	7192	864
1048		2017	6910	7193	865
1049		2017	6938	7194	866
1050		2017	7212	7195	867
1051		2016	7322	7196	868
1052		2016	7323	7197	869
1053		2013	6870	7198	870
1054		2014	6855	7199	871
1055		2017	6833	7200	872
1056		2016	7174	7201	873
1057		2013	7217	7202	874
1058		2012	7151	7203	875
1059		2017	7157	7204	876
1060		2017	7092	7205	877
1061		2013	7222	7206	878
1062		2018	7151	7207	879
1063		2018	7159	7208	880
1064		2016	7185	7209	881
1065		2018	7394	7210	882
1066		2018	7392	7211	883
1067		2017	7369	7212	884
1068		2016	7324	7213	885
1069		2018	7396	7214	886
1070		2014	7218	7215	887
1071		2013	7225	7216	888
1072		2014	7659	7217	889
1073		2014	7220	7218	890
1074		2013	7158	7219	891
1075		2013	7216	7220	892
1076		2012	7159	7221	893
1077		2018	7179	7222	894
1078		2014	6903	7223	895
1079		2016	7327	7224	896
1080		2016	7316	7225	897
1081		2018	7395	7226	898
1082		2016	7326	7227	899
1083		2017	7317	7228	900
1084		2017	7305	7229	901
1085		2014	7250	7230	902
1086		2018	7393	7231	903
1087		2014	7252	7232	904
1088		2018	7023	7233	905
1089		2013	6751	7234	906
1090		2016	6719	7235	907
1091		2018	6755	7236	908
1092		2018	6738	7237	909
1093		2017	6799	7238	910
1094		2018	7215	7239	911
1095		2016	7089	7240	912
1096		2014	6721	7241	913
1097		2015	7247	7242	914
1098		2018	6832	7243	915
1099		2016	7047	7244	916
1100		2015	7301	7245	917
1101		2018	7137	7246	918
1102		2017	6788	7247	919
1103		2017	7376	7248	920
1104		2017	6724	7249	921
1105		2016	6743	7250	922
1106		2017	6812	7251	923
1107		2016	7660	7252	924
1108		2017	6756	7253	925
1109		2018	6988	7254	926
1110		2018	6866	7255	927
1111		2017	6840	7256	928
1112		2015	7308	7257	929
1113		2017	6860	7258	930
1114		2012	6754	7259	931
1115		2016	7055	7260	932
1116		2017	6763	7261	933
1130	\N	2021	7067	6712	934
1131	\N	2021	7025	7262	935
1132	\N	2021	6764	7263	936
1133	\N	2021	6834	7264	937
1134	\N	2021	7258	7265	938
1135	\N	2021	7095	7266	939
1136	\N	2021	6924	7267	940
1137	\N	2021	7654	7268	941
1138	\N	2021	6845	7269	942
1139	\N	2021	6791	7270	943
1140	\N	2021	7277	7271	944
1141	\N	2021	7272	7272	945
1142	\N	2021	7236	7273	946
1143	\N	2021	6919	7274	947
1144	\N	2021	6798	7275	948
1145	\N	2021	6870	7276	949
1146	\N	2021	6986	7277	950
1147	\N	2021	6766	7278	951
1148	\N	2021	7259	7279	952
1149	\N	2021	7658	7280	953
1150	\N	2021	6804	7281	954
1151	\N	2021	6859	7282	955
1152	\N	2021	6808	7283	956
1153	\N	2021	6748	7284	957
1154	\N	2021	7356	7285	958
1155	\N	2021	6846	7286	959
1156	\N	2021	6807	7287	960
1157	\N	2021	6935	7288	961
1158	\N	2021	6821	7289	962
1159	\N	2021	7041	7290	963
1160	\N	2021	7268	7291	964
1161	\N	2021	7648	7292	965
1162	\N	2021	6758	7293	966
1168	\N	2021	7071	7299	972
1167	\N	2021	7123	7298	971
1166	\N	2021	7010	7297	970
1165	\N	2021	6869	7296	969
1164	\N	2021	6792	7295	968
1163	\N	2021	6865	7294	967
1169	\N	2021	7265	7300	973
1171	\N	2021	7050	7302	975
1172	\N	2021	6818	7303	976
1173	\N	2021	7001	7304	977
1174	\N	2021	7223	7305	978
1175	\N	2021	6722	7306	979
1176	\N	2021	6913	7307	980
873	\N	2013	6826	7018	690
1170	\N	2021	6826	7301	974
1179	\N	2021	6751	7308	981
1181	\N	2021	6765	7309	982
1182	\N	2021	6855	7310	983
1183	\N	2021	6781	7311	984
1184	\N	2021	7119	7312	985
1185	\N	2021	6896	7313	986
1186	\N	2021	7271	7314	987
1187	\N	2021	6741	7315	988
1188	\N	2021	7253	7316	989
1189	\N	2021	7493	7317	990
1190	\N	2021	7534	7318	991
1191	\N	2021	7538	7319	992
1192	\N	2021	7009	7320	993
1193	\N	2021	6790	7321	994
1194	\N	2021	6817	7322	995
1195	\N	2021	6950	7323	996
1196	\N	2021	6735	7324	997
1197	\N	2021	7539	7325	998
1198	\N	2021	7492	7326	999
1199	\N	2021	7661	7327	1000
1200	\N	2021	7541	7328	1001
1201	\N	2021	7663	7329	1002
1202	\N	2021	7490	7330	1003
1203	\N	2021	6802	7331	1004
1204	\N	2021	7540	7332	1005
1205	\N	2021	7491	7333	1006
1206	\N	2021	7664	7334	1007
1207	\N	2021	7244	7335	1008
1208	\N	2021	6959	7336	1009
1209	\N	2021	6757	7337	1010
1210	\N	2021	6875	7338	1011
1211	\N	2021	6947	7339	1012
1212	\N	2021	6912	7340	1013
1213	\N	2021	6747	7341	1014
1214	\N	2021	6727	7342	1015
1215	\N	2021	7211	7343	1016
1216	\N	2021	7210	7344	1017
1217	\N	2021	6754	7345	1018
1220	\N	2021	6920	7346	1019
1221	\N	2021	6773	7347	1020
1222	\N	2021	7275	7348	1021
1223	\N	2021	7221	7349	1022
1224	\N	2021	6937	7350	1023
1225	\N	2021	7016	7351	1024
1226	\N	2021	6837	7352	1025
1227	\N	2021	6892	7353	1026
1228	\N	2021	6978	7354	1027
1229	\N	2021	6942	7355	1028
1230	\N	2021	7651	7356	1029
1231	\N	2021	7650	7357	1030
1232	\N	2021	6811	7358	1031
1233	\N	2021	6752	7359	1032
1234	\N	2021	6962	7360	1033
1235	\N	2021	6829	7361	1034
1236	\N	2021	6963	7362	1035
1237	\N	2021	6881	7363	1036
1238	\N	2021	7021	7364	1037
1239	\N	2021	6879	7365	1038
1240	\N	2021	7209	7366	1039
1241	\N	2021	7208	7367	1040
1242	\N	2021	6850	7368	1041
1243	\N	2021	7263	7369	1042
1244	\N	2021	6797	7370	1043
1245	\N	2021	6973	7371	1044
1246	\N	2021	6956	7372	1045
1247	\N	2021	6789	7373	1046
1248	\N	2021	6964	7374	1047
1249	\N	2021	6917	7375	1048
1250	\N	2016	7018	7376	1049
1251	\N	2017	6957	7377	1050
1252	\N	2013	7017	7378	1051
1253	\N	2015	7022	7379	1052
1254	\N	2016	7015	7380	1053
1255	\N	2013	7019	7381	1054
1256	\N	2013	7016	7382	1055
1257	\N	2014	7021	7383	1056
1258	\N	2015	7207	7384	1057
1259	\N	2013	6956	7385	1058
1260	\N	2014	6963	7386	1059
1261	\N	2016	6965	7387	1060
1262	\N	2016	7201	7388	1061
1263	\N	2018	6955	7389	1062
1264	\N	2014	6966	7390	1063
1265	\N	2014	6961	7391	1064
1266	\N	2015	6960	7392	1065
1267	\N	2014	6964	7393	1066
1268	\N	2014	7010	7394	1067
1269	\N	2015	7012	7395	1068
1270	\N	2016	7205	7396	1069
1271	\N	2013	7011	7397	1070
1272	11R/19	2019	7442	7398	1071
1273	1R/19	2019	7431	7399	1072
1274	7C/19	2019	7448	7400	1073
1275	28R/19	2019	7456	7401	1074
1276	16R/19	2019	7429	7402	1075
1277	24R/19	2019	7444	7403	1076
1278	22R/19	2019	7443	7404	1077
1279	23R/19	2019	7450	7405	1078
1280	\N	2018	7108	7406	1079
1281	\N	2017	7146	7407	1080
1282	\N	2014	7125	7408	1081
1283	\N	2014	7254	7409	1082
1284	\N	2017	7145	7410	1083
1285	\N	2019	7365	7411	1084
1286	\N	2018	7144	7412	1085
1287	\N	2017	7160	7413	1086
1288	\N	2014	7251	7414	1087
1289	\N	2017	7100	7415	1088
1290	\N	2017	7155	7416	1089
1291	\N	2015	7310	7417	1090
1292	\N	2017	7099	7418	1091
1293	\N	2014	7253	7419	1092
1294	\N	2014	7256	7420	1093
1295	\N	2015	7312	7421	1094
1296	\N	2014	7255	7422	1095
949	Standard	2015	7286	7094	766
1297	\N	2014	7005	7423	1096
1298	\N	2018	7402	7424	1097
1299	\N	2018	7191	7425	1098
1300	\N	2018	7199	7426	1099
1301	\N	2015	6997	7427	1100
1302	\N	2016	7064	7428	1101
1303	\N	2015	7036	7429	1102
1304	\N	2016	7032	7430	1103
1305	\N	2018	7163	7431	1104
1306	\N	2016	6943	7432	1105
1307	\N	2016	7066	7433	1106
1308	\N	2015	6904	7434	1107
1309	\N	2016	6905	7435	1108
1310	\N	2016	7070	7436	1109
1311	\N	2016	7033	7437	1110
1312	\N	2016	6971	7438	1111
1313	\N	2015	6922	7439	1112
1314	\N	2017	7192	7440	1113
1315	\N	2017	7197	7441	1114
1316	\N	2016	7026	7442	1115
752	43R/20	2019	7471	6640	568
1317	\N	2020	7471	7443	1116
1318	\N	2018	7000	7444	1117
1319	\N	2014	7009	7445	1118
1320	\N	2018	7237	7446	1119
1321	\N	2013	7007	7447	1120
1322	\N	2017	7198	7448	1121
1323	\N	2016	7031	7449	1122
1324	\N	2017	7027	7450	1123
1325	\N	2013	7002	7451	1124
1326	\N	2015	7075	7452	1125
1327	\N	2015	7006	7453	1126
1328	\N	2013	6998	7454	1127
1329	\N	2015	7074	7455	1128
1330	\N	2015	7076	7456	1129
1331	\N	2013	6975	7457	1130
1332	\N	2018	6968	7458	1131
1333	\N	2013	6986	7459	1132
1334	\N	2015	6980	7460	1133
1335	\N	2014	6977	7461	1134
1336	\N	2014	6985	7462	1135
1337	\N	2015	6970	7463	1136
1338	\N	2014	6987	7464	1137
1339	\N	2015	6979	7465	1138
1340	\N	2014	6982	7466	1139
1341	\N	2016	6976	7467	1140
1342	\N	2014	6973	7468	1141
1343	\N	2010	6987	7469	1142
1345	\N	2015	7665	7470	1143
1346	20R/16	2016	7340	7471	1144
619	Registro 2016	2015	7340	6507	433
1347	Registro 2017, 10R/16	2016	7339	7472	1145
1348	Campione Standard	2017	7426	7473	1146
1349	Registro 2017, 26R/17	2016	7366	7474	1147
1350	Registro 2017, 19R/15	2016	7293	7475	1148
1351	Registro 2017, 8R/17	2016	7290	7476	1149
1352	Registro 2017, 3RE/17	2016	6842	7477	1150
1353	Registro 2017, 7R/16	2016	7341	7478	1151
1354	Registro 2017, 30R/17	2016	7378	7479	1152
1355	Registro 2017, 5C/16	2016	7273	7480	1153
1356	Registro 2016, 2P/16	2015	7348	7481	1154
1357	Registro 2017, 25R/17	2016	7363	7482	1155
540	Riprodotto in-house	2017	6744	6428	354
1358	Registro 2017, reiscrizione, 2RE/17	2016	6744	7483	1156
1359	Registro 2017, 1RC/16	2016	7665	7484	1157
1360	Registro 2017, 3R/16	2016	7349	7485	1158
1361	Registro 2017, 4R/16	2016	7342	7486	1159
1362	Registro 2017, 27R/17	2016	7665	7487	1160
1367	Registro 2017, 6R/16	2016	7344	7488	1161
1368	Registro 2017, 14R/16	2016	7361	7489	1162
1369	Registro 2017, 30R/15	2016	7289	7490	1163
1370	Registro 2017, 9R/16	2016	7338	7491	1164
\.


--
-- Data for Name: collect_storage; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.collect_storage (id, name) FROM stdin;
452	S101
453	S102
454	S103
455	S104
456	S105
457	S106
458	S107
459	S108
460	S201
461	S202
462	S203
463	S204
464	S205
465	S206
466	S207
467	S208
468	S301
469	S302
470	S303
471	S304
472	S305
473	S306
474	S307
475	S308
476	S401
477	S402
478	S403
479	S404
480	S405
481	S406
482	S407
483	S408
484	S501
485	S502
486	S503
487	S504
488	S505
489	S506
490	S507
491	S508
492	S601
493	S602
494	S603
495	S604
496	S605
497	S606
498	S607
499	S608
500	S701
501	S702
502	S703
503	S704
504	S705
505	S706
506	S707
507	S708
508	D101
509	D102
510	D103
511	D104
512	D105
513	D106
514	D107
515	D108
516	D201
517	D202
518	D203
519	D204
520	D205
521	D206
522	D207
523	D208
524	D301
525	D302
526	D303
527	D304
528	D305
529	D306
530	D307
531	D308
532	D401
533	D402
534	D403
535	D404
536	D405
537	D406
538	D407
539	D408
540	D501
541	D502
542	D503
543	D504
544	D505
545	D506
546	D507
547	D508
548	D601
549	D602
550	D603
551	D604
552	D605
553	D606
554	D607
555	D608
556	D701
557	D702
558	D703
559	D704
560	D705
561	D706
562	D707
563	D708
\.


--
-- Data for Name: collect_storageposition; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.collect_storageposition (id, name, storage_id) FROM stdin;
6087	1	452
6088	2	452
6089	3	452
6090	4	452
6091	5	452
6092	6	452
6093	7	452
6094	8	452
6095	9	452
6096	10	452
6097	11	452
6098	12	452
6099	13	452
6100	14	452
6101	15	452
6102	16	452
6103	1	453
6104	2	453
6105	3	453
6106	4	453
6107	5	453
6108	6	453
6109	7	453
6110	8	453
6111	9	453
6112	10	453
6113	11	453
6114	12	453
6115	13	453
6116	14	453
6117	15	453
6118	16	453
6119	1	454
6120	2	454
6121	3	454
6122	4	454
6123	5	454
6124	6	454
6125	7	454
6126	8	454
6127	9	454
6128	10	454
6129	11	454
6130	12	454
6131	13	454
6132	14	454
6133	15	454
6134	16	454
6135	1	455
6136	2	455
6137	3	455
6138	4	455
6139	5	455
6140	6	455
6141	7	455
6142	8	455
6143	9	455
6144	10	455
6145	11	455
6146	12	455
6147	13	455
6148	14	455
6149	15	455
6150	16	455
6151	1	456
6152	2	456
6153	3	456
6154	4	456
6155	5	456
6156	6	456
6157	7	456
6158	8	456
6159	9	456
6160	10	456
6161	11	456
6162	12	456
6163	13	456
6164	14	456
6165	15	456
6166	16	456
6167	1	457
6168	2	457
6169	3	457
6170	4	457
6171	5	457
6172	6	457
6173	7	457
6174	8	457
6175	9	457
6176	10	457
6177	11	457
6178	12	457
6179	13	457
6180	14	457
6181	15	457
6182	16	457
6183	1	458
6184	2	458
6185	3	458
6186	4	458
6187	5	458
6188	6	458
6189	7	458
6190	8	458
6191	9	458
6192	10	458
6193	11	458
6194	12	458
6195	13	458
6196	14	458
6197	15	458
6198	16	458
6199	1	459
6200	2	459
6201	3	459
6202	4	459
6203	5	459
6204	6	459
6205	7	459
6206	8	459
6207	9	459
6208	10	459
6209	11	459
6210	12	459
6211	13	459
6212	14	459
6213	15	459
6214	16	459
6215	1	460
6216	2	460
6217	3	460
6218	4	460
6219	5	460
6220	6	460
6221	7	460
6222	8	460
6223	9	460
6224	10	460
6225	11	460
6226	12	460
6227	13	460
6228	14	460
6229	15	460
6230	16	460
6231	1	461
6232	2	461
6233	3	461
6234	4	461
6235	5	461
6236	6	461
6237	7	461
6238	8	461
6239	9	461
6240	10	461
6241	11	461
6242	12	461
6243	13	461
6244	14	461
6245	15	461
6246	16	461
6247	1	462
6248	2	462
6249	3	462
6250	4	462
6251	5	462
6252	6	462
6253	7	462
6254	8	462
6255	9	462
6256	10	462
6257	11	462
6258	12	462
6259	13	462
6260	14	462
6261	15	462
6262	16	462
6263	1	463
6264	2	463
6265	3	463
6266	4	463
6267	5	463
6268	6	463
6269	7	463
6270	8	463
6271	9	463
6272	10	463
6273	11	463
6274	12	463
6275	13	463
6276	14	463
6277	15	463
6278	16	463
6279	1	464
6280	2	464
6281	3	464
6282	4	464
6283	5	464
6284	6	464
6285	7	464
6286	8	464
6287	9	464
6288	10	464
6289	11	464
6290	12	464
6291	13	464
6292	14	464
6293	15	464
6294	16	464
6295	1	465
6296	2	465
6297	3	465
6298	4	465
6299	5	465
6300	6	465
6301	7	465
6302	8	465
6303	9	465
6304	10	465
6305	11	465
6306	12	465
6307	13	465
6308	14	465
6309	15	465
6310	16	465
6311	1	466
6312	2	466
6313	3	466
6314	4	466
6315	5	466
6316	6	466
6317	7	466
6318	8	466
6319	9	466
6320	10	466
6321	11	466
6322	12	466
6323	13	466
6324	14	466
6325	15	466
6326	16	466
6327	1	467
6328	2	467
6329	3	467
6330	4	467
6331	5	467
6332	6	467
6333	7	467
6334	8	467
6335	9	467
6336	10	467
6337	11	467
6338	12	467
6339	13	467
6340	14	467
6341	15	467
6342	16	467
6343	1	468
6344	2	468
6345	3	468
6346	4	468
6347	5	468
6348	6	468
6349	7	468
6350	8	468
6351	9	468
6352	10	468
6353	11	468
6354	12	468
6355	13	468
6356	14	468
6357	15	468
6358	16	468
6359	1	469
6360	2	469
6361	3	469
6362	4	469
6363	5	469
6364	6	469
6365	7	469
6366	8	469
6367	9	469
6368	10	469
6369	11	469
6370	12	469
6371	13	469
6372	14	469
6373	15	469
6374	16	469
6375	1	470
6376	2	470
6377	3	470
6378	4	470
6379	5	470
6380	6	470
6381	7	470
6382	8	470
6383	9	470
6384	10	470
6385	11	470
6386	12	470
6387	13	470
6388	14	470
6389	15	470
6390	16	470
6391	1	471
6392	2	471
6393	3	471
6394	4	471
6395	5	471
6396	6	471
6397	7	471
6398	8	471
6399	9	471
6400	10	471
6401	11	471
6402	12	471
6403	13	471
6404	14	471
6405	15	471
6406	16	471
6407	1	472
6408	2	472
6409	3	472
6410	4	472
6411	5	472
6412	6	472
6413	7	472
6414	8	472
6415	9	472
6416	10	472
6417	11	472
6418	12	472
6419	13	472
6420	14	472
6421	15	472
6422	16	472
6423	1	473
6424	2	473
6425	3	473
6426	4	473
6427	5	473
6428	6	473
6429	7	473
6430	8	473
6431	9	473
6432	10	473
6433	11	473
6434	12	473
6435	13	473
6436	14	473
6437	15	473
6438	16	473
6439	1	474
6440	2	474
6441	3	474
6442	4	474
6443	5	474
6444	6	474
6445	7	474
6446	8	474
6447	9	474
6448	10	474
6449	11	474
6450	12	474
6451	13	474
6452	14	474
6453	15	474
6454	16	474
6455	1	475
6456	2	475
6457	3	475
6458	4	475
6459	5	475
6460	6	475
6461	7	475
6462	8	475
6463	9	475
6464	10	475
6465	11	475
6466	12	475
6467	13	475
6468	14	475
6469	15	475
6470	16	475
6471	1	476
6472	2	476
6473	3	476
6474	4	476
6475	5	476
6476	6	476
6477	7	476
6478	8	476
6479	9	476
6480	10	476
6481	11	476
6482	12	476
6483	13	476
6484	14	476
6485	15	476
6486	16	476
6487	1	477
6488	2	477
6489	3	477
6490	4	477
6491	5	477
6492	6	477
6493	7	477
6494	8	477
6495	9	477
6496	10	477
6497	11	477
6498	12	477
6499	13	477
6500	14	477
6501	15	477
6502	16	477
6503	1	478
6504	2	478
6505	3	478
6506	4	478
6507	5	478
6508	6	478
6509	7	478
6510	8	478
6511	9	478
6512	10	478
6513	11	478
6514	12	478
6515	13	478
6516	14	478
6517	15	478
6518	16	478
6519	1	479
6520	2	479
6521	3	479
6522	4	479
6523	5	479
6524	6	479
6525	7	479
6526	8	479
6527	9	479
6528	10	479
6529	11	479
6530	12	479
6531	13	479
6532	14	479
6533	15	479
6534	16	479
6535	1	480
6536	2	480
6537	3	480
6538	4	480
6539	5	480
6540	6	480
6541	7	480
6542	8	480
6543	9	480
6544	10	480
6545	11	480
6546	12	480
6547	13	480
6548	14	480
6549	15	480
6550	16	480
6551	1	481
6552	2	481
6553	3	481
6554	4	481
6555	5	481
6556	6	481
6557	7	481
6558	8	481
6559	9	481
6560	10	481
6561	11	481
6562	12	481
6563	13	481
6564	14	481
6565	15	481
6566	16	481
6567	1	482
6568	2	482
6569	3	482
6570	4	482
6571	5	482
6572	6	482
6573	7	482
6574	8	482
6575	9	482
6576	10	482
6577	11	482
6578	12	482
6579	13	482
6580	14	482
6581	15	482
6582	16	482
6583	1	483
6584	2	483
6585	3	483
6586	4	483
6587	5	483
6588	6	483
6589	7	483
6590	8	483
6591	9	483
6592	10	483
6593	11	483
6594	12	483
6595	13	483
6596	14	483
6597	15	483
6598	16	483
6599	1	484
6600	2	484
6601	3	484
6602	4	484
6603	5	484
6604	6	484
6605	7	484
6606	8	484
6607	9	484
6608	10	484
6609	11	484
6610	12	484
6611	13	484
6612	14	484
6613	15	484
6614	16	484
6615	1	485
6616	2	485
6617	3	485
6618	4	485
6619	5	485
6620	6	485
6621	7	485
6622	8	485
6623	9	485
6624	10	485
6625	11	485
6626	12	485
6627	13	485
6628	14	485
6629	15	485
6630	16	485
6631	1	486
6632	2	486
6633	3	486
6634	4	486
6635	5	486
6636	6	486
6637	7	486
6638	8	486
6639	9	486
6640	10	486
6641	11	486
6642	12	486
6643	13	486
6644	14	486
6645	15	486
6646	16	486
6647	1	487
6648	2	487
6649	3	487
6650	4	487
6651	5	487
6652	6	487
6653	7	487
6654	8	487
6655	9	487
6656	10	487
6657	11	487
6658	12	487
6659	13	487
6660	14	487
6661	15	487
6662	16	487
6663	1	488
6664	2	488
6665	3	488
6666	4	488
6667	5	488
6668	6	488
6669	7	488
6670	8	488
6671	9	488
6672	10	488
6673	11	488
6674	12	488
6675	13	488
6676	14	488
6677	15	488
6678	16	488
6679	1	489
6680	2	489
6681	3	489
6682	4	489
6683	5	489
6684	6	489
6685	7	489
6686	8	489
6687	9	489
6688	10	489
6689	11	489
6690	12	489
6691	13	489
6692	14	489
6693	15	489
6694	16	489
6695	1	490
6696	2	490
6697	3	490
6698	4	490
6699	5	490
6700	6	490
6701	7	490
6702	8	490
6703	9	490
6704	10	490
6705	11	490
6706	12	490
6707	13	490
6708	14	490
6709	15	490
6710	16	490
6711	1	491
6712	2	491
6713	3	491
6714	4	491
6715	5	491
6716	6	491
6717	7	491
6718	8	491
6719	9	491
6720	10	491
6721	11	491
6722	12	491
6723	13	491
6724	14	491
6725	15	491
6726	16	491
6727	1	492
6728	2	492
6729	3	492
6730	4	492
6731	5	492
6732	6	492
6733	7	492
6734	8	492
6735	9	492
6736	10	492
6737	11	492
6738	12	492
6739	13	492
6740	14	492
6741	15	492
6742	16	492
6743	1	493
6744	2	493
6745	3	493
6746	4	493
6747	5	493
6748	6	493
6749	7	493
6750	8	493
6751	9	493
6752	10	493
6753	11	493
6754	12	493
6755	13	493
6756	14	493
6757	15	493
6758	16	493
6759	1	494
6760	2	494
6761	3	494
6762	4	494
6763	5	494
6764	6	494
6765	7	494
6766	8	494
6767	9	494
6768	10	494
6769	11	494
6770	12	494
6771	13	494
6772	14	494
6773	15	494
6774	16	494
6775	1	495
6776	2	495
6777	3	495
6778	4	495
6779	5	495
6780	6	495
6781	7	495
6782	8	495
6783	9	495
6784	10	495
6785	11	495
6786	12	495
6787	13	495
6788	14	495
6789	15	495
6790	16	495
6791	1	496
6792	2	496
6793	3	496
6794	4	496
6795	5	496
6796	6	496
6797	7	496
6798	8	496
6799	9	496
6800	10	496
6801	11	496
6802	12	496
6803	13	496
6804	14	496
6805	15	496
6806	16	496
6807	1	497
6808	2	497
6809	3	497
6810	4	497
6811	5	497
6812	6	497
6813	7	497
6814	8	497
6815	9	497
6816	10	497
6817	11	497
6818	12	497
6819	13	497
6820	14	497
6821	15	497
6822	16	497
6823	1	498
6824	2	498
6825	3	498
6826	4	498
6827	5	498
6828	6	498
6829	7	498
6830	8	498
6831	9	498
6832	10	498
6833	11	498
6834	12	498
6835	13	498
6836	14	498
6837	15	498
6838	16	498
6839	1	499
6840	2	499
6841	3	499
6842	4	499
6843	5	499
6844	6	499
6845	7	499
6846	8	499
6847	9	499
6848	10	499
6849	11	499
6850	12	499
6851	13	499
6852	14	499
6853	15	499
6854	16	499
6855	1	500
6856	2	500
6857	3	500
6858	4	500
6859	5	500
6860	6	500
6861	7	500
6862	8	500
6863	9	500
6864	10	500
6865	11	500
6866	12	500
6867	13	500
6868	14	500
6869	15	500
6870	16	500
6871	1	501
6872	2	501
6873	3	501
6874	4	501
6875	5	501
6876	6	501
6877	7	501
6878	8	501
6879	9	501
6880	10	501
6881	11	501
6882	12	501
6883	13	501
6884	14	501
6885	15	501
6886	16	501
6887	1	502
6888	2	502
6889	3	502
6890	4	502
6891	5	502
6892	6	502
6893	7	502
6894	8	502
6895	9	502
6896	10	502
6897	11	502
6898	12	502
6899	13	502
6900	14	502
6901	15	502
6902	16	502
6903	1	503
6904	2	503
6905	3	503
6906	4	503
6907	5	503
6908	6	503
6909	7	503
6910	8	503
6911	9	503
6912	10	503
6913	11	503
6914	12	503
6915	13	503
6916	14	503
6917	15	503
6918	16	503
6919	1	504
6920	2	504
6921	3	504
6922	4	504
6923	5	504
6924	6	504
6925	7	504
6926	8	504
6927	9	504
6928	10	504
6929	11	504
6930	12	504
6931	13	504
6932	14	504
6933	15	504
6934	16	504
6935	1	505
6936	2	505
6937	3	505
6938	4	505
6939	5	505
6940	6	505
6941	7	505
6942	8	505
6943	9	505
6944	10	505
6945	11	505
6946	12	505
6947	13	505
6948	14	505
6949	15	505
6950	16	505
6951	1	506
6952	2	506
6953	3	506
6954	4	506
6955	5	506
6956	6	506
6957	7	506
6958	8	506
6959	9	506
6960	10	506
6961	11	506
6962	12	506
6963	13	506
6964	14	506
6965	15	506
6966	16	506
6967	1	507
6968	2	507
6969	3	507
6970	4	507
6971	5	507
6972	6	507
6973	7	507
6974	8	507
6975	9	507
6976	10	507
6977	11	507
6978	12	507
6979	13	507
6980	14	507
6981	15	507
6982	16	507
6983	1	508
6984	2	508
6985	3	508
6986	4	508
6987	5	508
6988	6	508
6989	7	508
6990	8	508
6991	9	508
6992	10	508
6993	11	508
6994	12	508
6995	13	508
6996	14	508
6997	15	508
6998	16	508
6999	1	509
7000	2	509
7001	3	509
7002	4	509
7003	5	509
7004	6	509
7005	7	509
7006	8	509
7007	9	509
7008	10	509
7009	11	509
7010	12	509
7011	13	509
7012	14	509
7013	15	509
7014	16	509
7015	1	510
7016	2	510
7017	3	510
7018	4	510
7019	5	510
7020	6	510
7021	7	510
7022	8	510
7023	9	510
7024	10	510
7025	11	510
7026	12	510
7027	13	510
7028	14	510
7029	15	510
7030	16	510
7031	1	511
7032	2	511
7033	3	511
7034	4	511
7035	5	511
7036	6	511
7037	7	511
7038	8	511
7039	9	511
7040	10	511
7041	11	511
7042	12	511
7043	13	511
7044	14	511
7045	15	511
7046	16	511
7047	1	512
7048	2	512
7049	3	512
7050	4	512
7051	5	512
7052	6	512
7053	7	512
7054	8	512
7055	9	512
7056	10	512
7057	11	512
7058	12	512
7059	13	512
7060	14	512
7061	15	512
7062	16	512
7063	1	513
7064	2	513
7065	3	513
7066	4	513
7067	5	513
7068	6	513
7069	7	513
7070	8	513
7071	9	513
7072	10	513
7073	11	513
7074	12	513
7075	13	513
7076	14	513
7077	15	513
7078	16	513
7079	1	514
7080	2	514
7081	3	514
7082	4	514
7083	5	514
7084	6	514
7085	7	514
7086	8	514
7087	9	514
7088	10	514
7089	11	514
7090	12	514
7091	13	514
7092	14	514
7093	15	514
7094	16	514
7095	1	515
7096	2	515
7097	3	515
7098	4	515
7099	5	515
7100	6	515
7101	7	515
7102	8	515
7103	9	515
7104	10	515
7105	11	515
7106	12	515
7107	13	515
7108	14	515
7109	15	515
7110	16	515
7111	1	516
7112	2	516
7113	3	516
7114	4	516
7115	5	516
7116	6	516
7117	7	516
7118	8	516
7119	9	516
7120	10	516
7121	11	516
7122	12	516
7123	13	516
7124	14	516
7125	15	516
7126	16	516
7127	1	517
7128	2	517
7129	3	517
7130	4	517
7131	5	517
7132	6	517
7133	7	517
7134	8	517
7135	9	517
7136	10	517
7137	11	517
7138	12	517
7139	13	517
7140	14	517
7141	15	517
7142	16	517
7143	1	518
7144	2	518
7145	3	518
7146	4	518
7147	5	518
7148	6	518
7149	7	518
7150	8	518
7151	9	518
7152	10	518
7153	11	518
7154	12	518
7155	13	518
7156	14	518
7157	15	518
7158	16	518
7159	1	519
7160	2	519
7161	3	519
7162	4	519
7163	5	519
7164	6	519
7165	7	519
7166	8	519
7167	9	519
7168	10	519
7169	11	519
7170	12	519
7171	13	519
7172	14	519
7173	15	519
7174	16	519
7175	1	520
7176	2	520
7177	3	520
7178	4	520
7179	5	520
7180	6	520
7181	7	520
7182	8	520
7183	9	520
7184	10	520
7185	11	520
7186	12	520
7187	13	520
7188	14	520
7189	15	520
7190	16	520
7191	1	521
7192	2	521
7193	3	521
7194	4	521
7195	5	521
7196	6	521
7197	7	521
7198	8	521
7199	9	521
7200	10	521
7201	11	521
7202	12	521
7203	13	521
7204	14	521
7205	15	521
7206	16	521
7207	1	522
7208	2	522
7209	3	522
7210	4	522
7211	5	522
7212	6	522
7213	7	522
7214	8	522
7215	9	522
7216	10	522
7217	11	522
7218	12	522
7219	13	522
7220	14	522
7221	15	522
7222	16	522
7223	1	523
7224	2	523
7225	3	523
7226	4	523
7227	5	523
7228	6	523
7229	7	523
7230	8	523
7231	9	523
7232	10	523
7233	11	523
7234	12	523
7235	13	523
7236	14	523
7237	15	523
7238	16	523
7239	1	524
7240	2	524
7241	3	524
7242	4	524
7243	5	524
7244	6	524
7245	7	524
7246	8	524
7247	9	524
7248	10	524
7249	11	524
7250	12	524
7251	13	524
7252	14	524
7253	15	524
7254	16	524
7255	1	525
7256	2	525
7257	3	525
7258	4	525
7259	5	525
7260	6	525
7261	7	525
7262	8	525
7263	9	525
7264	10	525
7265	11	525
7266	12	525
7267	13	525
7268	14	525
7269	15	525
7270	16	525
7271	1	526
7272	2	526
7273	3	526
7274	4	526
7275	5	526
7276	6	526
7277	7	526
7278	8	526
7279	9	526
7280	10	526
7281	11	526
7282	12	526
7283	13	526
7284	14	526
7285	15	526
7286	16	526
7287	1	527
7288	2	527
7289	3	527
7290	4	527
7291	5	527
7292	6	527
7293	7	527
7294	8	527
7295	9	527
7296	10	527
7297	11	527
7298	12	527
7299	13	527
7300	14	527
7301	15	527
7302	16	527
7303	1	528
7304	2	528
7305	3	528
7306	4	528
7307	5	528
7308	6	528
7309	7	528
7310	8	528
7311	9	528
7312	10	528
7313	11	528
7314	12	528
7315	13	528
7316	14	528
7317	15	528
7318	16	528
7319	1	529
7320	2	529
7321	3	529
7322	4	529
7323	5	529
7324	6	529
7325	7	529
7326	8	529
7327	9	529
7328	10	529
7329	11	529
7330	12	529
7331	13	529
7332	14	529
7333	15	529
7334	16	529
7335	1	530
7336	2	530
7337	3	530
7338	4	530
7339	5	530
7340	6	530
7341	7	530
7342	8	530
7343	9	530
7344	10	530
7345	11	530
7346	12	530
7347	13	530
7348	14	530
7349	15	530
7350	16	530
7351	1	531
7352	2	531
7353	3	531
7354	4	531
7355	5	531
7356	6	531
7357	7	531
7358	8	531
7359	9	531
7360	10	531
7361	11	531
7362	12	531
7363	13	531
7364	14	531
7365	15	531
7366	16	531
7367	1	532
7368	2	532
7369	3	532
7370	4	532
7371	5	532
7372	6	532
7373	7	532
7374	8	532
7375	9	532
7376	10	532
7377	11	532
7378	12	532
7379	13	532
7380	14	532
7381	15	532
7382	16	532
7383	1	533
7384	2	533
7385	3	533
7386	4	533
7387	5	533
7388	6	533
7389	7	533
7390	8	533
7391	9	533
7392	10	533
7393	11	533
7394	12	533
7395	13	533
7396	14	533
7397	15	533
7398	16	533
7399	1	534
7400	2	534
7401	3	534
7402	4	534
7403	5	534
7404	6	534
7405	7	534
7406	8	534
7407	9	534
7408	10	534
7409	11	534
7410	12	534
7411	13	534
7412	14	534
7413	15	534
7414	16	534
7415	1	535
7416	2	535
7417	3	535
7418	4	535
7419	5	535
7420	6	535
7421	7	535
7422	8	535
7423	9	535
7424	10	535
7425	11	535
7426	12	535
7427	13	535
7428	14	535
7429	15	535
7430	16	535
7431	1	536
7432	2	536
7433	3	536
7434	4	536
7435	5	536
7436	6	536
7437	7	536
7438	8	536
7439	9	536
7440	10	536
7441	11	536
7442	12	536
7443	13	536
7444	14	536
7445	15	536
7446	16	536
7447	1	537
7448	2	537
7449	3	537
7450	4	537
7451	5	537
7452	6	537
7453	7	537
7454	8	537
7455	9	537
7456	10	537
7457	11	537
7458	12	537
7459	13	537
7460	14	537
7461	15	537
7462	16	537
7463	1	538
7464	2	538
7465	3	538
7466	4	538
7467	5	538
7468	6	538
7469	7	538
7470	8	538
7471	9	538
7472	10	538
7473	11	538
7474	12	538
7475	13	538
7476	14	538
7477	15	538
7478	16	538
7479	1	539
7480	2	539
7481	3	539
7482	4	539
7483	5	539
7484	6	539
7485	7	539
7486	8	539
7487	9	539
7488	10	539
7489	11	539
7490	12	539
7491	13	539
7492	14	539
7493	15	539
7494	16	539
7495	1	540
7496	2	540
7497	3	540
7498	4	540
7499	5	540
7500	6	540
7501	7	540
7502	8	540
7503	9	540
7504	10	540
7505	11	540
7506	12	540
7507	13	540
7508	14	540
7509	15	540
7510	16	540
7511	1	541
7512	2	541
7513	3	541
7514	4	541
7515	5	541
7516	6	541
7517	7	541
7518	8	541
7519	9	541
7520	10	541
7521	11	541
7522	12	541
7523	13	541
7524	14	541
7525	15	541
7526	16	541
7527	1	542
7528	2	542
7529	3	542
7530	4	542
7531	5	542
7532	6	542
7533	7	542
7534	8	542
7535	9	542
7536	10	542
7537	11	542
7538	12	542
7539	13	542
7540	14	542
7541	15	542
7542	16	542
7543	1	543
7544	2	543
7545	3	543
7546	4	543
7547	5	543
7548	6	543
7549	7	543
7550	8	543
7551	9	543
7552	10	543
7553	11	543
7554	12	543
7555	13	543
7556	14	543
7557	15	543
7558	16	543
7559	1	544
7560	2	544
7561	3	544
7562	4	544
7563	5	544
7564	6	544
7565	7	544
7566	8	544
7567	9	544
7568	10	544
7569	11	544
7570	12	544
7571	13	544
7572	14	544
7573	15	544
7574	16	544
7575	1	545
7576	2	545
7577	3	545
7578	4	545
7579	5	545
7580	6	545
7581	7	545
7582	8	545
7583	9	545
7584	10	545
7585	11	545
7586	12	545
7587	13	545
7588	14	545
7589	15	545
7590	16	545
7591	1	546
7592	2	546
7593	3	546
7594	4	546
7595	5	546
7596	6	546
7597	7	546
7598	8	546
7599	9	546
7600	10	546
7601	11	546
7602	12	546
7603	13	546
7604	14	546
7605	15	546
7606	16	546
7607	1	547
7608	2	547
7609	3	547
7610	4	547
7611	5	547
7612	6	547
7613	7	547
7614	8	547
7615	9	547
7616	10	547
7617	11	547
7618	12	547
7619	13	547
7620	14	547
7621	15	547
7622	16	547
7623	1	548
7624	2	548
7625	3	548
7626	4	548
7627	5	548
7628	6	548
7629	7	548
7630	8	548
7631	9	548
7632	10	548
7633	11	548
7634	12	548
7635	13	548
7636	14	548
7637	15	548
7638	16	548
7639	1	549
7640	2	549
7641	3	549
7642	4	549
7643	5	549
7644	6	549
7645	7	549
7646	8	549
7647	9	549
7648	10	549
7649	11	549
7650	12	549
7651	13	549
7652	14	549
7653	15	549
7654	16	549
7655	1	550
7656	2	550
7657	3	550
7658	4	550
7659	5	550
7660	6	550
7661	7	550
7662	8	550
7663	9	550
7664	10	550
7665	11	550
7666	12	550
7667	13	550
7668	14	550
7669	15	550
7670	16	550
7671	1	551
7672	2	551
7673	3	551
7674	4	551
7675	5	551
7676	6	551
7677	7	551
7678	8	551
7679	9	551
7680	10	551
7681	11	551
7682	12	551
7683	13	551
7684	14	551
7685	15	551
7686	16	551
7687	1	552
7688	2	552
7689	3	552
7690	4	552
7691	5	552
7692	6	552
7693	7	552
7694	8	552
7695	9	552
7696	10	552
7697	11	552
7698	12	552
7699	13	552
7700	14	552
7701	15	552
7702	16	552
7703	1	553
7704	2	553
7705	3	553
7706	4	553
7707	5	553
7708	6	553
7709	7	553
7710	8	553
7711	9	553
7712	10	553
7713	11	553
7714	12	553
7715	13	553
7716	14	553
7717	15	553
7718	16	553
7719	1	554
7720	2	554
7721	3	554
7722	4	554
7723	5	554
7724	6	554
7725	7	554
7726	8	554
7727	9	554
7728	10	554
7729	11	554
7730	12	554
7731	13	554
7732	14	554
7733	15	554
7734	16	554
7735	1	555
7736	2	555
7737	3	555
7738	4	555
7739	5	555
7740	6	555
7741	7	555
7742	8	555
7743	9	555
7744	10	555
7745	11	555
7746	12	555
7747	13	555
7748	14	555
7749	15	555
7750	16	555
7751	1	556
7752	2	556
7753	3	556
7754	4	556
7755	5	556
7756	6	556
7757	7	556
7758	8	556
7759	9	556
7760	10	556
7761	11	556
7762	12	556
7763	13	556
7764	14	556
7765	15	556
7766	16	556
7767	1	557
7768	2	557
7769	3	557
7770	4	557
7771	5	557
7772	6	557
7773	7	557
7774	8	557
7775	9	557
7776	10	557
7777	11	557
7778	12	557
7779	13	557
7780	14	557
7781	15	557
7782	16	557
7783	1	558
7784	2	558
7785	3	558
7786	4	558
7787	5	558
7788	6	558
7789	7	558
7790	8	558
7791	9	558
7792	10	558
7793	11	558
7794	12	558
7795	13	558
7796	14	558
7797	15	558
7798	16	558
7799	1	559
7800	2	559
7801	3	559
7802	4	559
7803	5	559
7804	6	559
7805	7	559
7806	8	559
7807	9	559
7808	10	559
7809	11	559
7810	12	559
7811	13	559
7812	14	559
7813	15	559
7814	16	559
7815	1	560
7816	2	560
7817	3	560
7818	4	560
7819	5	560
7820	6	560
7821	7	560
7822	8	560
7823	9	560
7824	10	560
7825	11	560
7826	12	560
7827	13	560
7828	14	560
7829	15	560
7830	16	560
7831	1	561
7832	2	561
7833	3	561
7834	4	561
7835	5	561
7836	6	561
7837	7	561
7838	8	561
7839	9	561
7840	10	561
7841	11	561
7842	12	561
7843	13	561
7844	14	561
7845	15	561
7846	16	561
7847	1	562
7848	2	562
7849	3	562
7850	4	562
7851	5	562
7852	6	562
7853	7	562
7854	8	562
7855	9	562
7856	10	562
7857	11	562
7858	12	562
7859	13	562
7860	14	562
7861	15	562
7862	16	562
7863	1	563
7864	2	563
7865	3	563
7866	4	563
7867	5	563
7868	6	563
7869	7	563
7870	8	563
7871	9	563
7872	10	563
7873	11	563
7874	12	563
7875	13	563
7876	14	563
7877	15	563
7878	16	563
\.


--
-- Data for Name: describe_description; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.describe_description (id, name, protocol_id, variety_id) FROM stdin;
3234	Official	7	6719
3235	Official	7	6720
3236	Official	7	6721
3237	Official	7	6722
3238	Official	7	6723
3239	Official	7	6724
3240	Official	7	6725
3241	Official	7	6726
3242	Official	7	6727
3243	Official	7	6728
3244	Official	7	6729
3245	Official	7	6730
3246	Official	7	6731
3247	Official	7	6732
3248	Official	7	6733
3249	Official	7	6734
3250	Official	7	6735
3251	Official	7	6736
3252	Official	7	6737
3253	Official	7	6738
3254	Official	7	6739
3255	Official	7	6740
3256	Official	7	6741
3257	Official	7	6742
3258	Official	7	6743
3259	Official	7	6744
3260	Official	7	6745
3261	Official	7	6746
3262	Official	7	6747
3263	Official	7	6748
3264	Official	7	6749
3265	Official	7	6750
3266	Official	7	6751
3267	Official	7	6752
3268	Official	7	6753
3269	Official	7	6754
3270	Official	7	6755
3271	Official	7	6756
3272	Official	7	6757
3273	Official	7	6758
3274	Official	7	6759
3275	Official	7	6760
3276	Official	7	6761
3277	Official	7	6762
3278	Official	7	6763
3279	Official	7	6764
3280	Official	7	6765
3281	Official	7	6766
3282	Official	7	6767
3283	Official	7	6768
3284	Official	7	6769
3285	Official	7	6770
3286	Official	7	6771
3287	Official	7	6772
3288	Official	7	6773
3289	Official	7	6774
3290	Official	7	6775
3291	Official	7	6776
3292	Official	7	6777
3293	Official	7	6778
3294	Official	7	6779
3295	Official	7	6780
3296	Official	7	6781
3297	Official	7	6782
3298	Official	7	6783
3299	Official	7	6784
3300	Official	7	6785
3301	Official	7	6786
3302	Official	7	6787
3303	Official	7	6788
3304	Official	7	6789
3305	Official	7	6790
3306	Official	7	6791
3307	Official	7	6792
3308	Official	7	6793
3309	Official	7	6794
3310	Official	7	6795
3311	Official	7	6796
3312	Official	7	6797
3313	Official	7	6798
3314	Official	7	6799
3315	Official	7	6800
3316	Official	7	6801
3317	Official	7	6802
3318	Official	7	6803
3319	Official	7	6804
3320	Official	7	6805
3321	Official	7	6806
3322	Official	7	6807
3323	Official	7	6808
3324	Official	7	6809
3325	Official	7	6810
3326	Official	7	6811
3327	Official	7	6812
3328	Official	7	6813
3329	Official	7	6814
3330	Official	7	6815
3331	Official	7	6816
3332	Official	7	6817
3333	Official	7	6818
3334	Official	7	6819
3335	Official	7	6820
3336	Official	7	6821
3337	Official	7	6822
3338	Official	7	6823
3339	Official	7	6824
3340	Official	7	6825
3341	Official	7	6826
3342	Official	7	6827
3343	Official	7	6828
3344	Official	7	6829
3345	Official	7	6830
3346	Official	7	6831
3347	Official	7	6832
3348	Official	7	6833
3349	Official	7	6834
3350	Official	7	6835
3351	Official	7	6836
3352	Official	7	6837
3353	Official	7	6838
3354	Official	7	6839
3355	Official	7	6840
3356	Official	7	6841
3357	Official	7	6842
3358	Official	7	6843
3359	Official	7	6844
3360	Official	7	6845
3361	Official	7	6846
3362	Official	7	6847
3363	Official	7	6848
3364	Official	7	6849
3365	Official	7	6850
3366	Official	7	6851
3367	Official	7	6852
3368	Official	7	6853
3369	Official	7	6854
3370	Official	7	6855
3371	Official	7	6856
3372	Official	7	6857
3373	Official	7	6858
3374	Official	7	6859
3375	Official	7	6860
3376	Official	7	6861
3377	Official	7	6862
3378	Official	7	6863
3379	Official	7	6864
3380	Official	7	6865
3381	Official	7	6866
3382	Official	7	6867
3383	Official	7	6868
3384	Official	7	6869
3385	Official	7	6870
3386	Official	7	6871
3387	Official	7	6872
3388	Official	7	6873
3389	Official	7	6874
3390	Official	7	6875
3391	Official	7	6876
3392	Official	7	6877
3393	Official	7	6878
3394	Official	7	6879
3395	Official	7	6880
3396	Official	7	6881
3397	Official	7	6882
3398	Official	7	6883
3399	Official	7	6884
3400	Official	7	6885
3401	Official	7	6886
3402	Official	7	6887
3403	Official	7	6888
3404	Official	7	6889
3405	Official	7	6890
3406	Official	7	6891
3407	Official	7	6892
3408	Official	7	6893
3409	Official	7	6894
3410	Official	7	6895
3411	Official	7	6896
3412	Official	7	6897
3413	Official	7	6898
3414	Official	7	6899
3415	Official	7	6900
3416	Official	7	6901
3417	Official	7	6902
3418	Official	7	6903
3419	Official	7	6904
3420	Official	7	6905
3421	Official	7	6906
3422	Official	7	6907
3423	Official	7	6908
3424	Official	7	6909
3425	Official	7	6910
3426	Official	7	6911
3427	Official	7	6912
3428	Official	7	6913
3429	Official	7	6914
3430	Official	7	6915
3431	Official	7	6916
3432	Official	7	6917
3433	Official	7	6918
3434	Official	7	6919
3435	Official	7	6920
3436	Official	7	6921
3437	Official	7	6922
3438	Official	7	6923
3439	Official	7	6924
3440	Official	7	6925
3441	Official	7	6926
3442	Official	7	6927
3443	Official	7	6928
3444	Official	7	6929
3445	Official	7	6930
3446	Official	7	6931
3447	Official	7	6932
3448	Official	7	6933
3449	Official	7	6934
3450	Official	7	6935
3451	Official	7	6936
3452	Official	7	6937
3453	Official	7	6938
3454	Official	7	6939
3455	Official	7	6940
3456	Official	7	6941
3457	Official	7	6942
3458	Official	7	6943
3459	Official	7	6944
3460	Official	7	6945
3461	Official	7	6946
3462	Official	7	6947
3463	Official	7	6948
3464	Official	7	6949
3465	Official	7	6950
3466	Official	7	6951
3467	Official	7	6952
3468	Official	7	6953
3469	Official	7	6954
3470	Official	7	6955
3471	Official	7	6956
3472	Official	7	6957
3473	Official	7	6958
3474	Official	7	6959
3475	Official	7	6960
3476	Official	7	6961
3477	Official	7	6962
3478	Official	7	6963
3479	Official	7	6964
3480	Official	7	6965
3481	Official	7	6966
3482	Official	7	6967
3483	Official	7	6968
3484	Official	7	6969
3485	Official	7	6970
3486	Official	7	6971
3487	Official	7	6972
3488	Official	7	6973
3489	Official	7	6974
3490	Official	7	6975
3491	Official	7	6976
3492	Official	7	6977
3493	Official	7	6978
3494	Official	7	6979
3495	Official	7	6980
3496	Official	7	6981
3497	Official	7	6982
3498	Official	7	6983
3499	Official	7	6984
3500	Official	7	6985
3501	Official	7	6986
3502	Official	7	6987
3503	Official	7	6988
3504	Official	7	6989
3505	Official	7	6990
3506	Official	7	6991
3507	Official	7	6992
3508	Official	7	6993
3509	Official	7	6994
3510	Official	7	6995
3511	Official	7	6996
3512	Official	7	6997
3513	Official	7	6998
3514	Official	7	6999
3515	Official	7	7000
3516	Official	7	7001
3517	Official	7	7002
3518	Official	7	7003
3519	Official	7	7004
3520	Official	7	7005
3521	Official	7	7006
3522	Official	7	7007
3523	Official	7	7008
3524	Official	7	7009
3525	Official	7	7010
3526	Official	7	7011
3527	Official	7	7012
3528	Official	7	7013
3529	Official	7	7014
3530	Official	7	7015
3531	Official	7	7016
3532	Official	7	7017
3533	Official	7	7018
3534	Official	7	7019
3535	Official	7	7020
3536	Official	7	7021
3537	Official	7	7022
3538	Official	7	7023
3539	Official	7	7024
3540	Official	7	7025
3541	Official	7	7026
3542	Official	7	7027
3543	Official	7	7028
3544	Official	7	7029
3545	Official	7	7030
3546	Official	7	7031
3547	Official	7	7032
3548	Official	7	7033
3549	Official	7	7034
3550	Official	7	7035
3551	Official	7	7036
3552	Official	7	7037
3553	Official	7	7038
3554	Official	7	7039
3555	Official	7	7040
3556	Official	7	7041
3557	Official	7	7042
3558	Official	7	7043
3559	Official	7	7044
3560	Official	7	7045
3561	Official	7	7046
3562	Official	7	7047
3563	Official	7	7048
3564	Official	7	7049
3565	Official	7	7050
3566	Official	7	7051
3567	Official	7	7052
3568	Official	7	7053
3569	Official	7	7054
3570	Official	7	7055
3571	Official	7	7056
3572	Official	7	7057
3573	Official	7	7058
3574	Official	7	7059
3575	Official	7	7060
3576	Official	7	7061
3577	Official	7	7062
3578	Official	7	7063
3579	Official	7	7064
3580	Official	7	7065
3581	Official	7	7066
3582	Official	7	7067
3583	Official	7	7068
3584	Official	7	7069
3585	Official	7	7070
3586	Official	7	7071
3587	Official	7	7072
3588	Official	7	7073
3589	Official	7	7074
3590	Official	7	7075
3591	Official	7	7076
3592	Official	7	7077
3593	Official	7	7078
3594	Official	7	7079
3595	Official	7	7080
3596	Official	7	7081
3597	Official	7	7082
3598	Official	7	7083
3599	Official	7	7084
3600	Official	7	7085
3601	Official	7	7086
3602	Official	7	7087
3603	Official	7	7088
3604	Official	7	7089
3605	Official	7	7090
3606	Official	7	7091
3607	Official	7	7092
3608	Official	7	7093
3609	Official	7	7094
3610	Official	7	7095
3611	Official	7	7096
3612	Official	7	7097
3613	Official	7	7098
3614	Official	7	7099
3615	Official	7	7100
3616	Official	7	7101
3617	Official	7	7102
3618	Official	7	7103
3619	Official	7	7104
3620	Official	7	7105
3621	Official	7	7106
3622	Official	7	7107
3623	Official	7	7108
3624	Official	7	7109
3625	Official	7	7110
3626	Official	7	7111
3627	Official	7	7112
3628	Official	7	7113
3629	Official	7	7114
3630	Official	7	7115
3631	Official	7	7116
3632	Official	7	7117
3633	Official	7	7118
3634	Official	7	7119
3635	Official	7	7120
3636	Official	7	7121
3637	Official	7	7122
3638	Official	7	7123
3639	Official	7	7124
3640	Official	7	7125
3641	Official	7	7126
3642	Official	7	7127
3643	Official	7	7128
3644	Official	7	7129
3645	Official	7	7130
3646	Official	7	7131
3647	Official	7	7132
3648	Official	7	7133
3649	Official	7	7134
3650	Official	7	7135
3651	Official	7	7136
3652	Official	7	7137
3653	Official	7	7138
3654	Official	7	7139
3655	Official	7	7140
3656	Official	7	7141
3657	Official	7	7142
3658	Official	7	7143
3659	Official	7	7144
3660	Official	7	7145
3661	Official	7	7146
3662	Official	7	7147
3663	Official	7	7148
3664	Official	7	7149
3665	Official	7	7150
3666	Official	7	7151
3667	Official	7	7152
3668	Official	7	7153
3669	Official	7	7154
3670	Official	7	7155
3671	Official	7	7156
3672	Official	7	7157
3673	Official	7	7158
3674	Official	7	7159
3675	Official	7	7160
3676	Official	7	7161
3677	Official	7	7162
3678	Official	7	7163
3679	Official	7	7164
3680	Official	7	7165
3681	Official	7	7166
3682	Official	7	7167
3683	Official	7	7168
3684	Official	7	7169
3685	Official	7	7170
3686	Official	7	7171
3687	Official	7	7172
3688	Official	7	7173
3689	Official	7	7174
3690	Official	7	7175
3691	Official	7	7176
3692	Official	7	7177
3693	Official	7	7178
3694	Official	7	7179
3695	Official	7	7180
3696	Official	7	7181
3697	Official	7	7182
3698	Official	7	7183
3699	Official	7	7184
3700	Official	7	7185
3701	Official	7	7186
3702	Official	7	7187
3703	Official	7	7188
3704	Official	7	7189
3705	Official	7	7190
3706	Official	7	7191
3707	Official	7	7192
3708	Official	7	7193
3709	Official	7	7194
3710	Official	7	7195
3711	Official	7	7196
3712	Official	7	7197
3713	Official	7	7198
3714	Official	7	7199
3715	Official	7	7200
3716	Official	7	7201
3717	Official	7	7202
3718	Official	7	7203
3719	Official	7	7204
3720	Official	7	7205
3721	Official	7	7206
3722	Official	7	7207
3723	Official	7	7208
3724	Official	7	7209
3725	Official	7	7210
3726	Official	7	7211
3727	Official	7	7212
3728	Official	7	7213
3729	Official	7	7214
3730	Official	7	7215
3731	Official	7	7216
3732	Official	7	7217
3733	Official	7	7218
3734	Official	7	7219
3735	Official	7	7220
3736	Official	7	7221
3737	Official	7	7222
3738	Official	7	7223
3739	Official	7	7224
3740	Official	7	7225
3741	Official	7	7226
3742	Official	7	7227
3743	Official	7	7228
3744	Official	7	7229
3745	Official	7	7230
3746	Official	7	7231
3747	Official	7	7232
3748	Official	7	7233
3749	Official	7	7234
3750	Official	7	7235
3751	Official	7	7236
3752	Official	7	7237
3753	Official	7	7238
3754	Official	7	7239
3755	Official	7	7240
3756	Official	7	7241
3757	Official	7	7242
3758	Official	7	7243
3759	Official	7	7244
3760	Official	7	7245
3761	Official	7	7246
3762	Official	7	7247
3763	Official	7	7248
3764	Official	7	7249
3765	Official	7	7250
3766	Official	7	7251
3767	Official	7	7252
3768	Official	7	7253
3769	Official	7	7254
3770	Official	7	7255
3771	Official	7	7256
3772	Official	7	7257
3773	Official	7	7258
3774	Official	7	7259
3775	Official	7	7260
3776	Official	7	7261
3777	Official	7	7262
3778	Official	7	7263
3779	Official	7	7264
3780	Official	7	7265
3781	Official	7	7266
3782	Official	7	7267
3783	Official	7	7268
3784	Official	7	7269
3785	Official	7	7270
3786	Official	7	7271
3787	Official	7	7272
3788	Official	7	7273
3789	Official	7	7274
3790	Official	7	7275
3791	Official	7	7276
3792	Official	7	7277
3793	Official	7	7278
3794	Official	7	7279
3795	Official	7	7280
3796	Official	7	7281
3797	Official	7	7282
3798	Official	7	7283
3799	Official	7	7284
3800	Official	7	7285
3801	Official	7	7286
3802	Official	7	7287
3803	Official	7	7288
3804	Official	7	7289
3805	Official	7	7290
3806	Official	7	7291
3807	Official	7	7292
3808	Official	7	7293
3809	Official	7	7294
3810	Official	7	7295
3811	Official	7	7296
3812	Official	7	7297
3813	Official	7	7298
3814	Official	7	7299
3815	Official	7	7300
3816	Official	7	7301
3817	Official	7	7302
3818	Official	7	7303
3819	Official	7	7304
3820	Official	7	7305
3821	Official	7	7306
3822	Official	7	7307
3823	Official	7	7308
3824	Official	7	7309
3825	Official	7	7310
3826	Official	7	7311
3827	Official	7	7312
3828	Official	7	7313
3829	Official	7	7314
3830	Official	7	7315
3831	Official	7	7316
3832	Official	7	7317
3833	Official	7	7318
3834	Official	7	7319
3835	Official	7	7320
3836	Official	7	7321
3837	Official	7	7322
3838	Official	7	7323
3839	Official	7	7324
3840	Official	7	7325
3841	Official	7	7326
3842	Official	7	7327
3843	Official	7	7328
3844	Official	7	7329
3845	Official	7	7330
3846	Official	7	7331
3847	Official	7	7332
3848	Official	7	7333
3849	Official	7	7334
3850	Official	7	7335
3851	Official	7	7336
3852	Official	7	7337
3853	Official	7	7338
3854	Official	7	7339
3855	Official	7	7340
3856	Official	7	7341
3857	Official	7	7342
3858	Official	7	7343
3859	Official	7	7344
3860	Official	7	7345
3861	Official	7	7346
3862	Official	7	7347
3863	Official	7	7348
3864	Official	7	7349
3865	Official	7	7350
3866	Official	7	7351
3867	Official	7	7352
3868	Official	7	7353
3869	Official	7	7354
3870	Official	7	7355
3871	Official	7	7356
3872	Official	7	7357
3873	Official	7	7358
3874	Official	7	7359
3875	Official	7	7360
3876	Official	7	7361
3877	Official	7	7362
3878	Official	7	7363
3879	Official	7	7364
3880	Official	7	7365
3881	Official	7	7366
3882	Official	7	7367
3883	Official	7	7368
3884	Official	7	7369
3885	Official	7	7370
3886	Official	7	7371
3887	Official	7	7372
3888	Official	7	7373
3889	Official	7	7374
3890	Official	7	7375
3891	Official	7	7376
3892	Official	7	7377
3893	Official	7	7378
3894	Official	7	7379
3895	Official	7	7380
3896	Official	7	7381
3897	Official	7	7382
3898	Official	7	7383
3899	Official	7	7384
3900	Official	7	7385
3901	Official	7	7386
3902	Official	7	7387
3903	Official	7	7388
3904	Official	7	7389
3905	Official	7	7390
3906	Official	7	7391
3907	Official	7	7392
3908	Official	7	7393
3909	Official	7	7394
3910	Official	7	7395
3911	Official	7	7396
3912	Official	7	7397
3913	Official	7	7398
3914	Official	7	7399
3915	Official	7	7400
3916	Official	7	7401
3917	Official	7	7402
3918	Official	7	7403
3919	Official	7	7404
3920	Official	7	7405
3921	Official	7	7406
3922	Official	7	7407
3923	Official	7	7408
3924	Official	7	7409
3925	Official	7	7410
3926	Official	7	7411
3927	Official	7	7412
3928	Official	7	7413
3929	Official	7	7414
3930	Official	7	7415
3931	Official	7	7416
3932	Official	7	7417
3933	Official	7	7418
3934	Official	7	7419
3935	Official	7	7420
3936	Official	7	7421
3937	Official	7	7422
3938	Official	7	7423
3939	Official	7	7424
3940	Official	7	7425
3941	Official	7	7426
3942	Official	7	7427
3943	Official	7	7428
3944	Official	7	7429
3945	Official	7	7430
3946	Official	7	7431
3947	Official	7	7432
3948	Official	7	7433
3949	Official	7	7434
3950	Official	7	7435
3951	Official	7	7436
3952	Official	7	7437
3953	Official	7	7438
3954	Official	7	7439
3955	Official	7	7440
3956	Official	7	7441
3957	Official	7	7442
3958	Official	7	7443
3959	Official	7	7444
3960	Official	7	7445
3961	Official	7	7446
3962	Official	7	7447
3963	Official	7	7448
3964	Official	7	7449
3965	Official	7	7450
3966	Official	7	7451
3967	Official	7	7452
3968	Official	7	7453
3969	Official	7	7454
3970	Official	7	7455
3971	Official	7	7456
3972	Official	7	7457
3973	Official	7	7458
3974	Official	7	7459
3975	Official	7	7460
3976	Official	7	7461
3977	Official	7	7462
3978	Official	7	7463
3979	Official	7	7464
3980	Official	7	7465
3981	Official	7	7466
3982	Official	7	7467
3983	Official	7	7468
3984	Official	7	7469
3985	Official	7	7470
3986	Official	7	7471
3987	Official	7	7472
3988	Official	7	7473
3989	Official	7	7474
3990	Official	7	7475
3991	Official	7	7476
3992	Official	7	7477
3993	Official	7	7478
3994	Official	7	7479
3995	Official	7	7480
3996	Official	7	7481
3997	Official	7	7482
3998	Official	7	7483
3999	Official	7	7484
4000	Official	7	7485
4001	Official	7	7486
4002	Official	7	7487
4003	Official	7	7488
4004	Official	7	7489
4005	Official	7	7490
4006	Official	7	7491
4007	Official	7	7492
4008	Official	7	7493
4009	Official	7	7494
4010	Official	7	7495
4011	Official	7	7496
4012	Official	7	7497
4013	Official	7	7498
4014	Official	7	7499
4015	Official	7	7500
4016	Official	7	7501
4017	Official	7	7502
4018	Official	7	7503
4019	Official	7	7504
4020	Official	7	7505
4021	Official	7	7506
4022	Official	7	7507
4023	Official	7	7508
4024	Official	7	7509
4025	Official	7	7510
4026	Official	7	7511
4027	Official	7	7512
4028	Official	7	7513
4029	Official	7	7514
4030	Official	7	7515
4031	Official	7	7516
4032	Official	7	7517
4033	Official	7	7518
4034	Official	7	7519
4035	Official	7	7520
4036	Official	7	7521
4037	Official	7	7522
4038	Official	7	7523
4039	Official	7	7524
4040	Official	7	7525
4041	Official	7	7526
4042	Official	7	7527
4043	Official	7	7528
4044	Official	7	7529
4045	Official	7	7530
4046	Official	7	7531
4047	Official	7	7532
4048	Official	7	7533
4049	Official	7	7534
4050	Official	7	7535
4051	Official	7	7536
4052	Official	7	7537
4053	Official	7	7538
4054	Official	7	7539
4055	Official	7	7540
4056	Official	7	7541
4057	Official	7	7542
4058	Official	7	7543
4059	Official	7	7544
4060	Official	7	7654
\.


--
-- Data for Name: describe_expression; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.describe_expression (id, description_id, state_of_expression_id) FROM stdin;
108447	3234	733
108448	3234	734
108449	3234	740
108450	3234	744
108451	3234	746
108452	3234	749
108453	3234	753
108454	3234	758
108455	3234	761
108456	3234	764
108457	3234	768
108458	3234	774
108459	3234	777
108460	3234	782
108461	3234	787
108462	3234	789
108463	3234	793
108464	3234	794
108465	3234	806
108466	3234	814
108467	3234	819
108468	3234	822
108469	3234	828
108470	3234	832
108471	3234	835
108472	3234	841
108473	3234	845
108474	3234	846
108475	3234	851
108476	3234	852
108477	3234	859
108478	3234	860
108479	3234	871
108480	3234	873
108481	3234	874
108482	3235	732
108483	3235	734
108484	3235	740
108485	3235	744
108486	3235	746
108487	3235	749
108488	3235	754
108489	3235	760
108490	3235	761
108491	3235	764
108492	3235	768
108493	3235	772
108494	3235	777
108495	3235	783
108496	3235	787
108497	3235	789
108498	3235	793
108499	3235	794
108500	3235	809
108501	3235	811
108502	3235	819
108503	3235	823
108504	3235	827
108505	3235	832
108506	3235	834
108507	3235	842
108508	3235	845
108509	3235	847
108510	3235	851
108511	3235	853
108512	3235	857
108513	3235	860
108514	3235	871
108515	3235	872
108516	3235	874
108517	3236	732
108518	3236	734
108519	3236	740
108520	3236	744
108521	3236	747
108522	3236	749
108523	3236	754
108524	3236	757
108525	3236	761
108526	3236	764
108527	3236	768
108528	3236	775
108529	3236	777
108530	3236	783
108531	3236	787
108532	3236	789
108533	3236	792
108534	3236	794
108535	3236	806
108536	3236	815
108537	3236	819
108538	3236	822
108539	3236	828
108540	3236	830
108541	3236	835
108542	3236	841
108543	3236	845
108544	3236	846
108545	3236	851
108546	3236	852
108547	3236	859
108548	3236	860
108549	3236	871
108550	3236	874
108551	3237	732
108552	3237	734
108553	3237	740
108554	3237	744
108555	3237	746
108556	3237	749
108557	3237	760
108558	3237	761
108559	3237	765
108560	3237	769
108561	3237	774
108562	3237	777
108563	3237	785
108564	3237	787
108565	3237	789
108566	3237	792
108567	3237	802
108568	3237	808
108569	3237	814
108570	3237	828
108571	3237	832
108572	3237	836
108573	3237	842
108574	3237	845
108575	3237	848
108576	3237	851
108577	3237	854
108578	3237	857
108579	3237	860
108580	3237	871
108581	3237	874
108582	3238	732
108583	3238	734
108584	3238	740
108585	3238	744
108586	3238	746
108587	3238	748
108588	3238	753
108589	3238	760
108590	3238	761
108591	3238	764
108592	3238	768
108593	3238	772
108594	3238	777
108595	3238	783
108596	3238	787
108597	3238	789
108598	3238	793
108599	3238	795
108600	3238	796
108601	3238	801
108602	3238	809
108603	3238	811
108604	3238	819
108605	3238	823
108606	3238	826
108607	3238	833
108608	3238	834
108609	3238	842
108610	3238	845
108611	3238	848
108612	3238	851
108613	3238	854
108614	3238	856
108615	3238	860
108616	3238	871
108617	3238	872
108618	3238	874
108619	3239	733
108620	3239	734
108621	3239	740
108622	3239	744
108623	3239	746
108624	3239	749
108625	3239	753
108626	3239	760
108627	3239	761
108628	3239	764
108629	3239	768
108630	3239	772
108631	3239	777
108632	3239	782
108633	3239	787
108634	3239	789
108635	3239	793
108636	3239	794
108637	3239	806
108638	3239	811
108639	3239	818
108640	3239	822
108641	3239	826
108642	3239	832
108643	3239	834
108644	3239	840
108645	3239	845
108646	3239	846
108647	3239	851
108648	3239	852
108649	3239	859
108650	3239	860
108651	3239	871
108652	3239	873
108653	3239	874
108654	3240	733
108655	3240	734
108656	3240	740
108657	3240	743
108658	3240	746
108659	3240	749
108660	3240	754
108661	3240	757
108662	3240	761
108663	3240	764
108664	3240	768
108665	3240	773
108666	3240	777
108667	3240	782
108668	3240	787
108669	3240	789
108670	3240	792
108671	3240	794
108672	3240	808
108673	3240	811
108674	3240	819
108675	3240	822
108676	3240	827
108677	3240	830
108678	3240	835
108679	3240	841
108680	3240	845
108681	3240	847
108682	3240	851
108683	3240	852
108684	3240	858
108685	3240	860
108686	3240	871
108687	3240	873
108688	3240	874
108689	3241	732
108690	3241	734
108691	3241	736
108692	3241	740
108693	3241	744
108694	3241	745
108695	3241	749
108696	3241	753
108697	3241	758
108698	3241	761
108699	3241	764
108700	3241	768
108701	3241	772
108702	3241	777
108703	3241	784
108704	3241	787
108705	3241	789
108706	3241	792
108707	3241	795
108708	3241	797
108709	3241	802
108710	3241	808
108711	3241	811
108712	3241	819
108713	3241	823
108714	3241	828
108715	3241	830
108716	3241	835
108717	3241	841
108718	3241	843
108719	3241	847
108720	3241	849
108721	3241	853
108722	3241	856
108723	3241	860
108724	3241	871
108725	3241	872
108726	3241	874
108727	3242	732
108728	3242	734
108729	3242	740
108730	3242	743
108731	3242	746
108732	3242	749
108733	3242	752
108734	3242	757
108735	3242	761
108736	3242	764
108737	3242	768
108738	3242	772
108739	3242	777
108740	3242	783
108741	3242	787
108742	3242	789
108743	3242	792
108744	3242	794
108745	3242	806
108746	3242	811
108747	3242	818
108748	3242	822
108749	3242	828
108750	3242	831
108751	3242	835
108752	3242	840
108753	3242	845
108754	3242	846
108755	3242	851
108756	3242	852
108757	3242	859
108758	3242	860
108759	3242	871
108760	3242	872
108761	3242	874
108762	3243	731
108763	3243	734
108764	3243	740
108765	3243	743
108766	3243	747
108767	3243	748
108768	3243	752
108769	3243	760
108770	3243	761
108771	3243	764
108772	3243	768
108773	3243	772
108774	3243	777
108775	3243	783
108776	3243	787
108777	3243	789
108778	3243	791
108779	3243	794
108780	3243	808
108781	3243	811
108782	3243	817
108783	3243	821
108784	3243	827
108785	3243	833
108786	3243	835
108787	3243	841
108788	3243	843
108789	3243	847
108790	3243	849
108791	3243	854
108792	3243	856
108793	3243	860
108794	3243	871
108795	3243	873
108796	3243	874
108797	3244	732
108798	3244	734
108799	3244	740
108800	3244	744
108801	3244	747
108802	3244	748
108803	3244	753
108804	3244	760
108805	3244	761
108806	3244	764
108807	3244	768
108808	3244	774
108809	3244	777
108810	3244	783
108811	3244	787
108812	3244	789
108813	3244	793
108814	3244	794
108815	3244	806
108816	3244	813
108817	3244	819
108818	3244	823
108819	3244	825
108820	3244	832
108821	3244	835
108822	3244	840
108823	3244	845
108824	3244	846
108825	3244	851
108826	3244	852
108827	3244	859
108828	3244	860
108829	3244	871
108830	3244	872
108831	3244	874
108832	3245	731
108833	3245	734
108834	3245	740
108835	3245	744
108836	3245	746
108837	3245	749
108838	3245	753
108839	3245	758
108840	3245	761
108841	3245	764
108842	3245	768
108843	3245	772
108844	3245	777
108845	3245	784
108846	3245	787
108847	3245	789
108848	3245	792
108849	3245	795
108850	3245	800
108851	3245	803
108852	3245	807
108853	3245	815
108854	3245	819
108855	3245	823
108856	3245	827
108857	3245	832
108858	3245	837
108859	3245	842
108860	3245	845
108861	3245	848
108862	3245	851
108863	3245	854
108864	3245	857
108865	3245	860
108866	3245	871
108867	3245	872
108868	3245	874
108869	3246	732
108870	3246	734
108871	3246	740
108872	3246	743
108873	3246	746
108874	3246	749
108875	3246	754
108876	3246	758
108877	3246	761
108878	3246	764
108879	3246	768
108880	3246	772
108881	3246	777
108882	3246	783
108883	3246	787
108884	3246	789
108885	3246	792
108886	3246	794
108887	3246	806
108888	3246	811
108889	3246	818
108890	3246	821
108891	3246	826
108892	3246	831
108893	3246	835
108894	3246	841
108895	3246	845
108896	3246	847
108897	3246	851
108898	3246	853
108899	3246	858
108900	3246	860
108901	3246	871
108902	3246	873
108903	3246	874
108904	3247	731
108905	3247	734
108906	3247	740
108907	3247	743
108908	3247	746
108909	3247	749
108910	3247	753
108911	3247	758
108912	3247	761
108913	3247	764
108914	3247	768
108915	3247	772
108916	3247	777
108917	3247	784
108918	3247	787
108919	3247	789
108920	3247	792
108921	3247	794
108922	3247	808
108923	3247	811
108924	3247	818
108925	3247	822
108926	3247	828
108927	3247	830
108928	3247	835
108929	3247	841
108930	3247	844
108931	3247	847
108932	3247	851
108933	3247	853
108934	3247	857
108935	3247	860
108936	3247	871
108937	3247	872
108938	3247	874
108939	3248	732
108940	3248	734
108941	3248	740
108942	3248	744
108943	3248	746
108944	3248	749
108945	3248	753
108946	3248	758
108947	3248	761
108948	3248	764
108949	3248	768
108950	3248	772
108951	3248	777
108952	3248	783
108953	3248	787
108954	3248	789
108955	3248	793
108956	3248	795
108957	3248	798
108958	3248	804
108959	3248	808
108960	3248	811
108961	3248	819
108962	3248	821
108963	3248	827
108964	3248	831
108965	3248	835
108966	3248	840
108967	3248	843
108968	3248	847
108969	3248	849
108970	3248	854
108971	3248	856
108972	3248	860
108973	3248	871
108974	3248	872
108975	3248	874
108976	3249	732
108977	3249	734
108978	3249	740
108979	3249	744
108980	3249	746
108981	3249	750
108982	3249	754
108983	3249	758
108984	3249	761
108985	3249	764
108986	3249	768
108987	3249	772
108988	3249	777
108989	3249	783
108990	3249	787
108991	3249	789
108992	3249	792
108993	3249	794
108994	3249	808
108995	3249	811
108996	3249	819
108997	3249	822
108998	3249	827
108999	3249	830
109000	3249	835
109001	3249	841
109002	3249	845
109003	3249	846
109004	3249	851
109005	3249	852
109006	3249	859
109007	3249	860
109008	3249	871
109009	3249	873
109010	3249	874
109011	3250	733
109012	3250	734
109013	3250	740
109014	3250	743
109015	3250	745
109016	3250	749
109017	3250	754
109018	3250	758
109019	3250	761
109020	3250	764
109021	3250	768
109022	3250	775
109023	3250	777
109024	3250	783
109025	3250	787
109026	3250	789
109027	3250	792
109028	3250	794
109029	3250	806
109030	3250	814
109031	3250	819
109032	3250	822
109033	3250	828
109034	3250	831
109035	3250	835
109036	3250	841
109037	3250	845
109038	3250	847
109039	3250	851
109040	3250	853
109041	3250	858
109042	3250	860
109043	3250	871
109044	3250	872
109045	3250	874
109046	3251	733
109047	3251	734
109048	3251	740
109049	3251	744
109050	3251	747
109051	3251	749
109052	3251	753
109053	3251	757
109054	3251	761
109055	3251	764
109056	3251	768
109057	3251	776
109058	3251	781
109059	3251	784
109060	3251	787
109061	3251	789
109062	3251	793
109063	3251	794
109064	3251	806
109065	3251	815
109066	3251	819
109067	3251	822
109068	3251	828
109069	3251	830
109070	3251	835
109071	3251	841
109072	3251	845
109073	3251	846
109074	3251	851
109075	3251	852
109076	3251	859
109077	3251	860
109078	3251	871
109079	3251	873
109080	3251	876
109081	3252	732
109082	3252	734
109083	3252	741
109084	3252	744
109085	3252	746
109086	3252	749
109087	3252	753
109088	3252	760
109089	3252	761
109090	3252	766
109091	3252	770
109092	3252	775
109093	3252	777
109094	3252	786
109095	3252	788
109096	3252	790
109097	3252	792
109098	3252	794
109099	3252	810
109100	3252	813
109101	3252	819
109102	3252	823
109103	3252	828
109104	3252	831
109105	3252	836
109106	3252	842
109107	3252	845
109108	3252	848
109109	3252	851
109110	3252	854
109111	3252	857
109112	3252	860
109113	3252	871
109114	3252	872
109115	3252	874
109116	3253	733
109117	3253	734
109118	3253	740
109119	3253	744
109120	3253	747
109121	3253	749
109122	3253	754
109123	3253	760
109124	3253	761
109125	3253	764
109126	3253	768
109127	3253	772
109128	3253	777
109129	3253	783
109130	3253	787
109131	3253	789
109132	3253	792
109133	3253	794
109134	3253	806
109135	3253	811
109136	3253	819
109137	3253	822
109138	3253	828
109139	3253	832
109140	3253	835
109141	3253	841
109142	3253	844
109143	3253	847
109144	3253	851
109145	3253	853
109146	3253	857
109147	3253	860
109148	3253	871
109149	3253	874
109150	3254	732
109151	3254	734
109152	3254	740
109153	3254	743
109154	3254	746
109155	3254	750
109156	3254	755
109157	3254	759
109158	3254	761
109159	3254	764
109160	3254	768
109161	3254	772
109162	3254	777
109163	3254	784
109164	3254	787
109165	3254	789
109166	3254	792
109167	3254	794
109168	3254	808
109169	3254	811
109170	3254	818
109171	3254	821
109172	3254	828
109173	3254	831
109174	3254	835
109175	3254	841
109176	3254	845
109177	3254	847
109178	3254	851
109179	3254	853
109180	3254	857
109181	3254	860
109182	3254	871
109183	3254	872
109184	3254	874
109185	3255	732
109186	3255	734
109187	3255	740
109188	3255	743
109189	3255	746
109190	3255	749
109191	3255	754
109192	3255	758
109193	3255	761
109194	3255	764
109195	3255	768
109196	3255	772
109197	3255	777
109198	3255	783
109199	3255	787
109200	3255	789
109201	3255	792
109202	3255	794
109203	3255	808
109204	3255	811
109205	3255	818
109206	3255	822
109207	3255	827
109208	3255	830
109209	3255	835
109210	3255	841
109211	3255	845
109212	3255	847
109213	3255	851
109214	3255	853
109215	3255	858
109216	3255	860
109217	3255	871
109218	3255	872
109219	3255	874
109220	3256	732
109221	3256	734
109222	3256	740
109223	3256	744
109224	3256	747
109225	3256	749
109226	3256	753
109227	3256	760
109228	3256	761
109229	3256	766
109230	3256	770
109231	3256	775
109232	3256	777
109233	3256	784
109234	3256	787
109235	3256	789
109236	3256	793
109237	3256	794
109238	3256	810
109239	3256	815
109240	3256	819
109241	3256	823
109242	3256	828
109243	3256	831
109244	3256	837
109245	3256	842
109246	3256	844
109247	3256	848
109248	3256	850
109249	3256	854
109250	3256	856
109251	3256	860
109252	3256	871
109253	3256	873
109254	3256	874
109255	3257	732
109256	3257	734
109257	3257	740
109258	3257	744
109259	3257	747
109260	3257	749
109261	3257	753
109262	3257	758
109263	3257	761
109264	3257	764
109265	3257	768
109266	3257	772
109267	3257	777
109268	3257	784
109269	3257	787
109270	3257	789
109271	3257	792
109272	3257	794
109273	3257	808
109274	3257	811
109275	3257	818
109276	3257	821
109277	3257	828
109278	3257	831
109279	3257	835
109280	3257	841
109281	3257	845
109282	3257	847
109283	3257	851
109284	3257	853
109285	3257	858
109286	3257	860
109287	3257	871
109288	3257	872
109289	3257	874
109290	3258	731
109291	3258	734
109292	3258	740
109293	3258	742
109294	3258	746
109295	3258	748
109296	3258	753
109297	3258	759
109298	3258	761
109299	3258	764
109300	3258	768
109301	3258	772
109302	3258	777
109303	3258	782
109304	3258	787
109305	3258	789
109306	3258	792
109307	3258	794
109308	3258	808
109309	3258	811
109310	3258	819
109311	3258	822
109312	3258	828
109313	3258	832
109314	3258	835
109315	3258	841
109316	3258	844
109317	3258	847
109318	3258	850
109319	3258	853
109320	3258	856
109321	3258	860
109322	3258	871
109323	3258	872
109324	3258	874
109325	3259	732
109326	3259	734
109327	3259	740
109328	3259	742
109329	3259	746
109330	3259	749
109331	3259	753
109332	3259	758
109333	3259	761
109334	3259	764
109335	3259	768
109336	3259	772
109337	3259	777
109338	3259	784
109339	3259	787
109340	3259	789
109341	3259	791
109342	3259	794
109343	3259	808
109344	3259	811
109345	3259	818
109346	3259	821
109347	3259	828
109348	3259	832
109349	3259	835
109350	3259	841
109351	3259	843
109352	3259	848
109353	3259	849
109354	3259	854
109355	3259	856
109356	3259	860
109357	3259	871
109358	3259	873
109359	3259	874
109360	3260	732
109361	3260	734
109362	3260	740
109363	3260	743
109364	3260	746
109365	3260	749
109366	3260	754
109367	3260	757
109368	3260	761
109369	3260	764
109370	3260	768
109371	3260	772
109372	3260	777
109373	3260	783
109374	3260	787
109375	3260	789
109376	3260	792
109377	3260	794
109378	3260	807
109379	3260	814
109380	3260	819
109381	3260	823
109382	3260	826
109383	3260	830
109384	3260	834
109385	3260	840
109386	3260	845
109387	3260	846
109388	3260	851
109389	3260	852
109390	3260	859
109391	3260	860
109392	3260	871
109393	3260	873
109394	3260	874
109395	3261	732
109396	3261	734
109397	3261	740
109398	3261	744
109399	3261	746
109400	3261	749
109401	3261	753
109402	3261	758
109403	3261	761
109404	3261	764
109405	3261	768
109406	3261	772
109407	3261	777
109408	3261	784
109409	3261	787
109410	3261	789
109411	3261	793
109412	3261	794
109413	3261	808
109414	3261	815
109415	3261	819
109416	3261	823
109417	3261	826
109418	3261	831
109419	3261	835
109420	3261	840
109421	3261	845
109422	3261	846
109423	3261	851
109424	3261	852
109425	3261	859
109426	3261	868
109427	3261	871
109428	3261	872
109429	3261	876
109430	3262	732
109431	3262	734
109432	3262	740
109433	3262	743
109434	3262	745
109435	3262	748
109436	3262	753
109437	3262	758
109438	3262	761
109439	3262	764
109440	3262	768
109441	3262	772
109442	3262	777
109443	3262	782
109444	3262	787
109445	3262	789
109446	3262	792
109447	3262	794
109448	3262	807
109449	3262	811
109450	3262	819
109451	3262	823
109452	3262	826
109453	3262	831
109454	3262	835
109455	3262	841
109456	3262	845
109457	3262	846
109458	3262	851
109459	3262	852
109460	3262	859
109461	3262	860
109462	3262	871
109463	3262	873
109464	3262	874
109465	3263	731
109466	3263	734
109467	3263	740
109468	3263	744
109469	3263	745
109470	3263	749
109471	3263	753
109472	3263	759
109473	3263	761
109474	3263	764
109475	3263	768
109476	3263	776
109477	3263	777
109478	3263	783
109479	3263	787
109480	3263	789
109481	3263	792
109482	3263	794
109483	3263	806
109484	3263	815
109485	3263	819
109486	3263	822
109487	3263	825
109488	3263	832
109489	3263	835
109490	3263	841
109491	3263	845
109492	3263	846
109493	3263	851
109494	3263	852
109495	3263	859
109496	3263	860
109497	3263	871
109498	3263	873
109499	3263	876
109500	3264	732
109501	3264	734
109502	3264	740
109503	3264	744
109504	3264	746
109505	3264	749
109506	3264	754
109507	3264	759
109508	3264	761
109509	3264	764
109510	3264	768
109511	3264	772
109512	3264	777
109513	3264	784
109514	3264	787
109515	3264	789
109516	3264	793
109517	3264	794
109518	3264	808
109519	3264	811
109520	3264	818
109521	3264	822
109522	3264	827
109523	3264	831
109524	3264	835
109525	3264	841
109526	3264	844
109527	3264	847
109528	3264	850
109529	3264	853
109530	3264	857
109531	3264	860
109532	3264	871
109533	3264	872
109534	3264	874
109535	3265	732
109536	3265	734
109537	3265	740
109538	3265	743
109539	3265	747
109540	3265	749
109541	3265	754
109542	3265	759
109543	3265	761
109544	3265	764
109545	3265	768
109546	3265	772
109547	3265	777
109548	3265	784
109549	3265	787
109550	3265	789
109551	3265	792
109552	3265	794
109553	3265	806
109554	3265	811
109555	3265	818
109556	3265	822
109557	3265	826
109558	3265	831
109559	3265	835
109560	3265	841
109561	3265	844
109562	3265	847
109563	3265	850
109564	3265	853
109565	3265	857
109566	3265	860
109567	3265	871
109568	3265	873
109569	3265	874
109570	3266	732
109571	3266	734
109572	3266	740
109573	3266	744
109574	3266	746
109575	3266	749
109576	3266	754
109577	3266	760
109578	3266	761
109579	3266	764
109580	3266	768
109581	3266	772
109582	3266	777
109583	3266	783
109584	3266	787
109585	3266	789
109586	3266	793
109587	3266	794
109588	3266	809
109589	3266	811
109590	3266	819
109591	3266	823
109592	3266	827
109593	3266	832
109594	3266	834
109595	3266	842
109596	3266	845
109597	3266	847
109598	3266	851
109599	3266	853
109600	3266	857
109601	3266	860
109602	3266	871
109603	3266	873
109604	3266	874
109605	3267	732
109606	3267	734
109607	3267	740
109608	3267	743
109609	3267	746
109610	3267	749
109611	3267	753
109612	3267	759
109613	3267	761
109614	3267	764
109615	3267	768
109616	3267	774
109617	3267	777
109618	3267	783
109619	3267	787
109620	3267	789
109621	3267	792
109622	3267	794
109623	3267	806
109624	3267	815
109625	3267	819
109626	3267	823
109627	3267	827
109628	3267	831
109629	3267	834
109630	3267	841
109631	3267	845
109632	3267	846
109633	3267	851
109634	3267	852
109635	3267	859
109636	3267	860
109637	3267	871
109638	3267	872
109639	3267	874
109640	3268	732
109641	3268	734
109642	3268	740
109643	3268	744
109644	3268	747
109645	3268	749
109646	3268	753
109647	3268	758
109648	3268	761
109649	3268	764
109650	3268	768
109651	3268	772
109652	3268	777
109653	3268	784
109654	3268	787
109655	3268	789
109656	3268	793
109657	3268	794
109658	3268	808
109659	3268	811
109660	3268	819
109661	3268	823
109662	3268	828
109663	3268	831
109664	3268	835
109665	3268	840
109666	3268	845
109667	3268	847
109668	3268	851
109669	3268	853
109670	3268	858
109671	3268	860
109672	3268	871
109673	3268	872
109674	3268	874
109675	3269	732
109676	3269	734
109677	3269	740
109678	3269	744
109679	3269	746
109680	3269	749
109681	3269	753
109682	3269	760
109683	3269	761
109684	3269	764
109685	3269	768
109686	3269	772
109687	3269	777
109688	3269	783
109689	3269	787
109690	3269	789
109691	3269	793
109692	3269	794
109693	3269	808
109694	3269	811
109695	3269	819
109696	3269	823
109697	3269	827
109698	3269	832
109699	3269	835
109700	3269	841
109701	3269	845
109702	3269	846
109703	3269	851
109704	3269	852
109705	3269	859
109706	3269	860
109707	3269	871
109708	3269	874
109709	3270	732
109710	3270	734
109711	3270	740
109712	3270	744
109713	3270	746
109714	3270	749
109715	3270	754
109716	3270	760
109717	3270	761
109718	3270	764
109719	3270	768
109720	3270	772
109721	3270	777
109722	3270	784
109723	3270	787
109724	3270	789
109725	3270	793
109726	3270	794
109727	3270	808
109728	3270	811
109729	3270	819
109730	3270	823
109731	3270	828
109732	3270	832
109733	3270	835
109734	3270	842
109735	3270	845
109736	3270	847
109737	3270	851
109738	3270	854
109739	3270	857
109740	3270	860
109741	3270	871
109742	3270	874
109743	3271	733
109744	3271	734
109745	3271	740
109746	3271	744
109747	3271	745
109748	3271	748
109749	3271	754
109750	3271	760
109751	3271	761
109752	3271	764
109753	3271	768
109754	3271	775
109755	3271	781
109756	3271	782
109757	3271	787
109758	3271	789
109759	3271	792
109760	3271	794
109761	3271	806
109762	3271	815
109763	3271	819
109764	3271	822
109765	3271	826
109766	3271	832
109767	3271	834
109768	3271	841
109769	3271	845
109770	3271	846
109771	3271	851
109772	3271	852
109773	3271	859
109774	3271	860
109775	3271	871
109776	3271	874
109777	3272	732
109778	3272	734
109779	3272	740
109780	3272	743
109781	3272	747
109782	3272	750
109783	3272	754
109784	3272	758
109785	3272	761
109786	3272	764
109787	3272	768
109788	3272	772
109789	3272	777
109790	3272	785
109791	3272	787
109792	3272	789
109793	3272	792
109794	3272	794
109795	3272	808
109796	3272	811
109797	3272	818
109798	3272	823
109799	3272	827
109800	3272	835
109801	3272	842
109802	3272	845
109803	3272	847
109804	3272	851
109805	3272	854
109806	3272	857
109807	3272	860
109808	3272	871
109809	3272	872
109810	3272	874
109811	3273	733
109812	3273	734
109813	3273	740
109814	3273	744
109815	3273	746
109816	3273	749
109817	3273	754
109818	3273	760
109819	3273	761
109820	3273	764
109821	3273	768
109822	3273	772
109823	3273	777
109824	3273	784
109825	3273	787
109826	3273	789
109827	3273	792
109828	3273	794
109829	3273	809
109830	3273	811
109831	3273	819
109832	3273	821
109833	3273	828
109834	3273	833
109835	3273	835
109836	3273	842
109837	3273	844
109838	3273	847
109839	3273	850
109840	3273	854
109841	3273	856
109842	3273	860
109843	3273	871
109844	3273	872
109845	3273	874
109846	3274	733
109847	3274	734
109848	3274	740
109849	3274	743
109850	3274	747
109851	3274	748
109852	3274	752
109853	3274	760
109854	3274	761
109855	3274	764
109856	3274	768
109857	3274	772
109858	3274	777
109859	3274	782
109860	3274	787
109861	3274	789
109862	3274	792
109863	3274	795
109864	3274	800
109865	3274	803
109866	3274	807
109867	3274	811
109868	3274	818
109869	3274	822
109870	3274	826
109871	3274	833
109872	3274	834
109873	3274	841
109874	3274	845
109875	3274	847
109876	3274	850
109877	3274	853
109878	3274	857
109879	3274	860
109880	3274	871
109881	3274	872
109882	3274	874
109883	3275	731
109884	3275	734
109885	3275	740
109886	3275	744
109887	3275	747
109888	3275	750
109889	3275	754
109890	3275	758
109891	3275	761
109892	3275	764
109893	3275	768
109894	3275	772
109895	3275	777
109896	3275	785
109897	3275	787
109898	3275	789
109899	3275	792
109900	3275	794
109901	3275	809
109902	3275	811
109903	3275	819
109904	3275	822
109905	3275	828
109906	3275	831
109907	3275	835
109908	3275	842
109909	3275	845
109910	3275	847
109911	3275	851
109912	3275	854
109913	3275	857
109914	3275	860
109915	3275	871
109916	3275	872
109917	3275	874
109918	3276	732
109919	3276	734
109920	3276	740
109921	3276	742
109922	3276	745
109923	3276	749
109924	3276	753
109925	3276	758
109926	3276	761
109927	3276	764
109928	3276	768
109929	3276	772
109930	3276	777
109931	3276	784
109932	3276	787
109933	3276	789
109934	3276	791
109935	3276	794
109936	3276	808
109937	3276	811
109938	3276	818
109939	3276	822
109940	3276	828
109941	3276	832
109942	3276	835
109943	3276	841
109944	3276	843
109945	3276	847
109946	3276	849
109947	3276	854
109948	3276	856
109949	3276	860
109950	3276	871
109951	3276	872
109952	3276	874
109953	3277	731
109954	3277	734
109955	3277	740
109956	3277	744
109957	3277	746
109958	3277	749
109959	3277	753
109960	3277	760
109961	3277	761
109962	3277	764
109963	3277	768
109964	3277	772
109965	3277	777
109966	3277	784
109967	3277	787
109968	3277	789
109969	3277	792
109970	3277	794
109971	3277	809
109972	3277	811
109973	3277	819
109974	3277	823
109975	3277	828
109976	3277	833
109977	3277	835
109978	3277	841
109979	3277	843
109980	3277	847
109981	3277	849
109982	3277	854
109983	3277	856
109984	3277	860
109985	3277	871
109986	3277	874
109987	3278	732
109988	3278	734
109989	3278	740
109990	3278	744
109991	3278	746
109992	3278	750
109993	3278	754
109994	3278	760
109995	3278	761
109996	3278	764
109997	3278	768
109998	3278	773
109999	3278	777
110000	3278	783
110001	3278	787
110002	3278	789
110003	3278	793
110004	3278	794
110005	3278	806
110006	3278	815
110007	3278	819
110008	3278	823
110009	3278	827
110010	3278	833
110011	3278	835
110012	3278	841
110013	3278	845
110014	3278	846
110015	3278	851
110016	3278	852
110017	3278	859
110018	3278	860
110019	3278	871
110020	3278	874
110021	3279	732
110022	3279	734
110023	3279	740
110024	3279	743
110025	3279	747
110026	3279	748
110027	3279	753
110028	3279	760
110029	3279	761
110030	3279	764
110031	3279	768
110032	3279	772
110033	3279	777
110034	3279	782
110035	3279	787
110036	3279	789
110037	3279	792
110038	3279	794
110039	3279	808
110040	3279	811
110041	3279	818
110042	3279	822
110043	3279	826
110044	3279	833
110045	3279	835
110046	3279	841
110047	3279	844
110048	3279	848
110049	3279	850
110050	3279	854
110051	3279	856
110052	3279	860
110053	3279	871
110054	3279	872
110055	3279	874
110056	3280	732
110057	3280	734
110058	3280	740
110059	3280	743
110060	3280	747
110061	3280	749
110062	3280	753
110063	3280	760
110064	3280	761
110065	3280	764
110066	3280	768
110067	3280	772
110068	3280	777
110069	3280	782
110070	3280	787
110071	3280	789
110072	3280	792
110073	3280	794
110074	3280	809
110075	3280	811
110076	3280	819
110077	3280	823
110078	3280	826
110079	3280	833
110080	3280	835
110081	3280	842
110082	3280	844
110083	3280	848
110084	3280	850
110085	3280	854
110086	3280	856
110087	3280	860
110088	3280	871
110089	3280	872
110090	3280	874
110091	3281	732
110092	3281	734
110093	3281	740
110094	3281	744
110095	3281	747
110096	3281	748
110097	3281	752
110098	3281	758
110099	3281	761
110100	3281	764
110101	3281	768
110102	3281	772
110103	3281	777
110104	3281	783
110105	3281	787
110106	3281	789
110107	3281	793
110108	3281	794
110109	3281	806
110110	3281	811
110111	3281	819
110112	3281	823
110113	3281	827
110114	3281	831
110115	3281	834
110116	3281	842
110117	3281	845
110118	3281	847
110119	3281	851
110120	3281	854
110121	3281	857
110122	3281	860
110123	3281	871
110124	3281	872
110125	3281	874
110126	3282	731
110127	3282	734
110128	3282	740
110129	3282	744
110130	3282	746
110131	3282	749
110132	3282	753
110133	3282	760
110134	3282	761
110135	3282	764
110136	3282	768
110137	3282	772
110138	3282	777
110139	3282	785
110140	3282	787
110141	3282	789
110142	3282	792
110143	3282	795
110144	3282	800
110145	3282	803
110146	3282	809
110147	3282	811
110148	3282	819
110149	3282	822
110150	3282	828
110151	3282	832
110152	3282	835
110153	3282	840
110154	3282	844
110155	3282	847
110156	3282	849
110157	3282	852
110158	3282	857
110159	3282	860
110160	3282	871
110161	3282	873
110162	3282	874
110163	3283	732
110164	3283	734
110165	3283	740
110166	3283	743
110167	3283	747
110168	3283	749
110169	3283	753
110170	3283	759
110171	3283	761
110172	3283	764
110173	3283	768
110174	3283	772
110175	3283	777
110176	3283	784
110177	3283	787
110178	3283	789
110179	3283	791
110180	3283	795
110181	3283	800
110182	3283	804
110183	3283	810
110184	3283	811
110185	3283	819
110186	3283	822
110187	3283	826
110188	3283	832
110189	3283	835
110190	3283	842
110191	3283	844
110192	3283	848
110193	3283	850
110194	3283	854
110195	3283	856
110196	3283	860
110197	3283	871
110198	3283	872
110199	3283	874
110200	3284	732
110201	3284	734
110202	3284	740
110203	3284	742
110204	3284	747
110205	3284	750
110206	3284	753
110207	3284	757
110208	3284	761
110209	3284	764
110210	3284	768
110211	3284	772
110212	3284	777
110213	3284	783
110214	3284	787
110215	3284	789
110216	3284	791
110217	3284	794
110218	3284	808
110219	3284	811
110220	3284	818
110221	3284	821
110222	3284	828
110223	3284	830
110224	3284	835
110225	3284	841
110226	3284	845
110227	3284	847
110228	3284	851
110229	3284	853
110230	3284	857
110231	3284	860
110232	3284	871
110233	3284	872
110234	3284	874
110235	3285	732
110236	3285	734
110237	3285	740
110238	3285	742
110239	3285	746
110240	3285	749
110241	3285	753
110242	3285	758
110243	3285	761
110244	3285	764
110245	3285	768
110246	3285	772
110247	3285	777
110248	3285	783
110249	3285	787
110250	3285	789
110251	3285	792
110252	3285	795
110253	3285	799
110254	3285	803
110255	3285	808
110256	3285	811
110257	3285	819
110258	3285	822
110259	3285	828
110260	3285	832
110261	3285	835
110262	3285	840
110263	3285	843
110264	3285	847
110265	3285	849
110266	3285	853
110267	3285	856
110268	3285	860
110269	3285	871
110270	3285	872
110271	3285	874
110272	3286	732
110273	3286	734
110274	3286	740
110275	3286	744
110276	3286	746
110277	3286	749
110278	3286	754
110279	3286	758
110280	3286	761
110281	3286	764
110282	3286	768
110283	3286	772
110284	3286	777
110285	3286	784
110286	3286	787
110287	3286	789
110288	3286	792
110289	3286	794
110290	3286	809
110291	3286	811
110292	3286	819
110293	3286	823
110294	3286	827
110295	3286	831
110296	3286	834
110297	3286	842
110298	3286	845
110299	3286	847
110300	3286	851
110301	3286	853
110302	3286	857
110303	3286	860
110304	3286	871
110305	3286	872
110306	3286	874
110307	3287	732
110308	3287	734
110309	3287	740
110310	3287	744
110311	3287	747
110312	3287	749
110313	3287	754
110314	3287	758
110315	3287	761
110316	3287	764
110317	3287	768
110318	3287	772
110319	3287	777
110320	3287	783
110321	3287	787
110322	3287	789
110323	3287	793
110324	3287	794
110325	3287	808
110326	3287	811
110327	3287	819
110328	3287	822
110329	3287	828
110330	3287	831
110331	3287	835
110332	3287	840
110333	3287	845
110334	3287	846
110335	3287	851
110336	3287	852
110337	3287	858
110338	3287	860
110339	3287	871
110340	3287	872
110341	3287	874
110342	3288	733
110343	3288	734
110344	3288	740
110345	3288	744
110346	3288	747
110347	3288	749
110348	3288	753
110349	3288	759
110350	3288	761
110351	3288	764
110352	3288	768
110353	3288	775
110354	3288	777
110355	3288	783
110356	3288	787
110357	3288	789
110358	3288	792
110359	3288	794
110360	3288	806
110361	3288	811
110362	3288	819
110363	3288	822
110364	3288	826
110365	3288	832
110366	3288	835
110367	3288	840
110368	3288	845
110369	3288	846
110370	3288	851
110371	3288	852
110372	3288	859
110373	3288	860
110374	3288	871
110375	3288	872
110376	3288	874
110377	3289	731
110378	3289	734
110379	3289	740
110380	3289	743
110381	3289	746
110382	3289	749
110383	3289	754
110384	3289	760
110385	3289	761
110386	3289	764
110387	3289	768
110388	3289	772
110389	3289	777
110390	3289	784
110391	3289	787
110392	3289	789
110393	3289	792
110394	3289	794
110395	3289	810
110396	3289	811
110397	3289	819
110398	3289	821
110399	3289	828
110400	3289	833
110401	3289	835
110402	3289	841
110403	3289	844
110404	3289	847
110405	3289	850
110406	3289	853
110407	3289	856
110408	3289	860
110409	3289	871
110410	3289	872
110411	3289	874
110412	3290	732
110413	3290	734
110414	3290	740
110415	3290	743
110416	3290	747
110417	3290	749
110418	3290	753
110419	3290	758
110420	3290	761
110421	3290	764
110422	3290	768
110423	3290	772
110424	3290	777
110425	3290	784
110426	3290	787
110427	3290	789
110428	3290	792
110429	3290	794
110430	3290	808
110431	3290	811
110432	3290	818
110433	3290	821
110434	3290	828
110435	3290	831
110436	3290	835
110437	3290	841
110438	3290	845
110439	3290	847
110440	3290	851
110441	3290	853
110442	3290	858
110443	3290	860
110444	3290	871
110445	3290	872
110446	3290	874
110447	3291	732
110448	3291	734
110449	3291	740
110450	3291	744
110451	3291	746
110452	3291	750
110453	3291	754
110454	3291	758
110455	3291	761
110456	3291	764
110457	3291	768
110458	3291	772
110459	3291	777
110460	3291	783
110461	3291	787
110462	3291	789
110463	3291	792
110464	3291	794
110465	3291	809
110466	3291	811
110467	3291	819
110468	3291	822
110469	3291	828
110470	3291	830
110471	3291	835
110472	3291	842
110473	3291	845
110474	3291	847
110475	3291	851
110476	3291	853
110477	3291	858
110478	3291	860
110479	3291	871
110480	3291	872
110481	3291	874
110482	3292	732
110483	3292	734
110484	3292	740
110485	3292	743
110486	3292	746
110487	3292	750
110488	3292	754
110489	3292	760
110490	3292	761
110491	3292	764
110492	3292	768
110493	3292	775
110494	3292	781
110495	3292	783
110496	3292	787
110497	3292	789
110498	3292	792
110499	3292	795
110500	3292	796
110501	3292	802
110502	3292	806
110503	3292	815
110504	3292	819
110505	3292	822
110506	3292	826
110507	3292	832
110508	3292	835
110509	3292	841
110510	3292	845
110511	3292	846
110512	3292	851
110513	3292	852
110514	3292	859
110515	3292	860
110516	3292	871
110517	3292	872
110518	3292	874
110519	3293	732
110520	3293	734
110521	3293	740
110522	3293	744
110523	3293	747
110524	3293	748
110525	3293	754
110526	3293	760
110527	3293	761
110528	3293	764
110529	3293	768
110530	3293	774
110531	3293	777
110532	3293	786
110533	3293	787
110534	3293	790
110535	3293	793
110536	3293	795
110537	3293	800
110538	3293	805
110539	3293	808
110540	3293	815
110541	3293	819
110542	3293	823
110543	3293	828
110544	3293	832
110545	3293	836
110546	3293	841
110547	3293	845
110548	3293	848
110549	3293	851
110550	3293	854
110551	3293	857
110552	3293	860
110553	3293	871
110554	3293	873
110555	3293	874
110556	3294	731
110557	3294	734
110558	3294	740
110559	3294	744
110560	3294	746
110561	3294	749
110562	3294	753
110563	3294	761
110564	3294	764
110565	3294	768
110566	3294	774
110567	3294	777
110568	3294	784
110569	3294	787
110570	3294	789
110571	3294	793
110572	3294	794
110573	3294	808
110574	3294	815
110575	3294	819
110576	3294	823
110577	3294	828
110578	3294	837
110579	3294	842
110580	3294	845
110581	3294	848
110582	3294	851
110583	3294	854
110584	3294	857
110585	3294	860
110586	3294	871
110587	3294	873
110588	3294	874
110589	3295	731
110590	3295	734
110591	3295	740
110592	3295	743
110593	3295	746
110594	3295	749
110595	3295	754
110596	3295	757
110597	3295	761
110598	3295	764
110599	3295	768
110600	3295	774
110601	3295	777
110602	3295	784
110603	3295	787
110604	3295	789
110605	3295	793
110606	3295	794
110607	3295	808
110608	3295	815
110609	3295	819
110610	3295	823
110611	3295	827
110612	3295	830
110613	3295	837
110614	3295	842
110615	3295	845
110616	3295	848
110617	3295	851
110618	3295	854
110619	3295	857
110620	3295	860
110621	3295	871
110622	3295	873
110623	3295	874
110624	3296	732
110625	3296	734
110626	3296	740
110627	3296	743
110628	3296	747
110629	3296	749
110630	3296	753
110631	3296	760
110632	3296	761
110633	3296	764
110634	3296	768
110635	3296	772
110636	3296	777
110637	3296	783
110638	3296	787
110639	3296	789
110640	3296	792
110641	3296	794
110642	3296	809
110643	3296	811
110644	3296	819
110645	3296	822
110646	3296	828
110647	3296	833
110648	3296	835
110649	3296	841
110650	3296	844
110651	3296	848
110652	3296	850
110653	3296	854
110654	3296	856
110655	3296	860
110656	3296	871
110657	3296	872
110658	3296	874
110659	3297	732
110660	3297	734
110661	3297	740
110662	3297	743
110663	3297	745
110664	3297	749
110665	3297	754
110666	3297	758
110667	3297	761
110668	3297	764
110669	3297	768
110670	3297	772
110671	3297	777
110672	3297	784
110673	3297	787
110674	3297	789
110675	3297	792
110676	3297	795
110677	3297	799
110678	3297	804
110679	3297	808
110680	3297	813
110681	3297	819
110682	3297	822
110683	3297	827
110684	3297	830
110685	3297	835
110686	3297	840
110687	3297	843
110688	3297	847
110689	3297	849
110690	3297	853
110691	3297	856
110692	3297	860
110693	3297	869
110694	3297	872
110695	3297	874
110696	3298	732
110697	3298	734
110698	3298	740
110699	3298	743
110700	3298	747
110701	3298	749
110702	3298	754
110703	3298	758
110704	3298	761
110705	3298	764
110706	3298	768
110707	3298	772
110708	3298	777
110709	3298	783
110710	3298	787
110711	3298	789
110712	3298	792
110713	3298	795
110714	3298	797
110715	3298	801
110716	3298	808
110717	3298	811
110718	3298	818
110719	3298	822
110720	3298	828
110721	3298	831
110722	3298	835
110723	3298	840
110724	3298	843
110725	3298	848
110726	3298	849
110727	3298	854
110728	3298	856
110729	3298	860
110730	3298	871
110731	3298	872
110732	3298	874
110733	3299	732
110734	3299	734
110735	3299	740
110736	3299	742
110737	3299	746
110738	3299	748
110739	3299	753
110740	3299	758
110741	3299	761
110742	3299	764
110743	3299	768
110744	3299	772
110745	3299	777
110746	3299	783
110747	3299	787
110748	3299	789
110749	3299	792
110750	3299	795
110751	3299	798
110752	3299	803
110753	3299	808
110754	3299	811
110755	3299	818
110756	3299	822
110757	3299	828
110758	3299	831
110759	3299	835
110760	3299	841
110761	3299	843
110762	3299	847
110763	3299	849
110764	3299	853
110765	3299	856
110766	3299	860
110767	3299	871
110768	3299	872
110769	3299	874
110770	3300	732
110771	3300	734
110772	3300	740
110773	3300	743
110774	3300	747
110775	3300	749
110776	3300	753
110777	3300	758
110778	3300	761
110779	3300	764
110780	3300	770
110781	3300	775
110782	3300	777
110783	3300	784
110784	3300	787
110785	3300	789
110786	3300	792
110787	3300	794
110788	3300	808
110789	3300	814
110790	3300	818
110791	3300	822
110792	3300	825
110793	3300	831
110794	3300	837
110795	3300	842
110796	3300	845
110797	3300	847
110798	3300	851
110799	3300	853
110800	3300	857
110801	3300	860
110802	3300	871
110803	3300	872
110804	3300	874
110805	3301	733
110806	3301	735
110807	3301	739
110808	3301	741
110809	3301	743
110810	3301	746
110811	3301	750
110812	3301	754
110813	3301	760
110814	3301	761
110815	3301	767
110816	3301	771
110817	3301	776
110818	3301	781
110819	3301	783
110820	3301	788
110821	3301	790
110822	3301	792
110823	3301	794
110824	3301	806
110825	3301	816
110826	3301	819
110827	3301	823
110828	3301	828
110829	3301	831
110830	3301	835
110831	3301	841
110832	3301	844
110833	3301	847
110834	3301	850
110835	3301	853
110836	3301	857
110837	3301	860
110838	3301	871
110839	3301	873
110840	3301	874
110841	3302	732
110842	3302	734
110843	3302	740
110844	3302	742
110845	3302	746
110846	3302	748
110847	3302	753
110848	3302	758
110849	3302	761
110850	3302	764
110851	3302	768
110852	3302	772
110853	3302	777
110854	3302	783
110855	3302	787
110856	3302	789
110857	3302	791
110858	3302	794
110859	3302	809
110860	3302	811
110861	3302	818
110862	3302	821
110863	3302	826
110864	3302	830
110865	3302	835
110866	3302	841
110867	3302	843
110868	3302	847
110869	3302	849
110870	3302	854
110871	3302	856
110872	3302	860
110873	3302	869
110874	3302	872
110875	3302	874
110876	3303	732
110877	3303	734
110878	3303	740
110879	3303	743
110880	3303	745
110881	3303	750
110882	3303	754
110883	3303	757
110884	3303	761
110885	3303	764
110886	3303	768
110887	3303	772
110888	3303	777
110889	3303	783
110890	3303	787
110891	3303	789
110892	3303	792
110893	3303	794
110894	3303	808
110895	3303	811
110896	3303	818
110897	3303	822
110898	3303	828
110899	3303	830
110900	3303	835
110901	3303	841
110902	3303	843
110903	3303	847
110904	3303	849
110905	3303	854
110906	3303	856
110907	3303	860
110908	3303	871
110909	3303	872
110910	3303	874
110911	3304	732
110912	3304	734
110913	3304	740
110914	3304	743
110915	3304	745
110916	3304	749
110917	3304	754
110918	3304	757
110919	3304	761
110920	3304	764
110921	3304	768
110922	3304	775
110923	3304	781
110924	3304	783
110925	3304	787
110926	3304	789
110927	3304	792
110928	3304	794
110929	3304	806
110930	3304	815
110931	3304	819
110932	3304	822
110933	3304	827
110934	3304	830
110935	3304	834
110936	3304	840
110937	3304	845
110938	3304	846
110939	3304	851
110940	3304	852
110941	3304	859
110942	3304	860
110943	3304	871
110944	3304	873
110945	3304	874
110946	3305	732
110947	3305	734
110948	3305	740
110949	3305	743
110950	3305	745
110951	3305	750
110952	3305	755
110953	3305	758
110954	3305	761
110955	3305	764
110956	3305	768
110957	3305	776
110958	3305	780
110959	3305	783
110960	3305	787
110961	3305	789
110962	3305	792
110963	3305	794
110964	3305	806
110965	3305	816
110966	3305	819
110967	3305	822
110968	3305	826
110969	3305	831
110970	3305	834
110971	3305	840
110972	3305	845
110973	3305	846
110974	3305	851
110975	3305	852
110976	3305	859
110977	3305	860
110978	3305	871
110979	3305	873
110980	3305	874
110981	3306	732
110982	3306	734
110983	3306	740
110984	3306	743
110985	3306	746
110986	3306	749
110987	3306	754
110988	3306	758
110989	3306	761
110990	3306	764
110991	3306	768
110992	3306	772
110993	3306	777
110994	3306	784
110995	3306	787
110996	3306	789
110997	3306	792
110998	3306	794
110999	3306	806
111000	3306	811
111001	3306	827
111002	3306	830
111003	3306	835
111004	3306	841
111005	3306	843
111006	3306	847
111007	3306	849
111008	3306	854
111009	3306	856
111010	3306	860
111011	3306	871
111012	3306	872
111013	3306	874
111014	3307	733
111015	3307	734
111016	3307	740
111017	3307	743
111018	3307	746
111019	3307	748
111020	3307	753
111021	3307	760
111022	3307	761
111023	3307	764
111024	3307	768
111025	3307	775
111026	3307	777
111027	3307	784
111028	3307	787
111029	3307	789
111030	3307	792
111031	3307	794
111032	3307	806
111033	3307	816
111034	3307	819
111035	3307	823
111036	3307	827
111037	3307	832
111038	3307	835
111039	3307	840
111040	3307	845
111041	3307	846
111042	3307	851
111043	3307	852
111044	3307	859
111045	3307	860
111046	3307	871
111047	3307	872
111048	3307	874
111049	3308	732
111050	3308	735
111051	3308	737
111052	3308	740
111053	3308	744
111054	3308	745
111055	3308	749
111056	3308	753
111057	3308	760
111058	3308	761
111059	3308	764
111060	3308	768
111061	3308	775
111062	3308	781
111063	3308	784
111064	3308	787
111065	3308	789
111066	3308	793
111067	3308	794
111068	3308	807
111069	3308	815
111070	3308	819
111071	3308	823
111072	3308	825
111073	3308	832
111074	3308	835
111075	3308	841
111076	3308	845
111077	3308	846
111078	3308	851
111079	3308	853
111080	3308	859
111081	3308	860
111082	3308	871
111083	3308	872
111084	3308	874
111085	3309	732
111086	3309	734
111087	3309	740
111088	3309	742
111089	3309	746
111090	3309	749
111091	3309	753
111092	3309	758
111093	3309	761
111094	3309	764
111095	3309	768
111096	3309	772
111097	3309	777
111098	3309	784
111099	3309	787
111100	3309	789
111101	3309	792
111102	3309	794
111103	3309	806
111104	3309	811
111105	3309	818
111106	3309	823
111107	3309	827
111108	3309	832
111109	3309	835
111110	3309	841
111111	3309	845
111112	3309	847
111113	3309	851
111114	3309	853
111115	3309	857
111116	3309	860
111117	3309	871
111118	3309	872
111119	3309	874
111120	3310	732
111121	3310	734
111122	3310	740
111123	3310	744
111124	3310	746
111125	3310	749
111126	3310	754
111127	3310	757
111128	3310	761
111129	3310	764
111130	3310	768
111131	3310	772
111132	3310	777
111133	3310	783
111134	3310	787
111135	3310	789
111136	3310	792
111137	3310	794
111138	3310	806
111139	3310	811
111140	3310	818
111141	3310	822
111142	3310	828
111143	3310	831
111144	3310	835
111145	3310	841
111146	3310	844
111147	3310	847
111148	3310	850
111149	3310	853
111150	3310	857
111151	3310	860
111152	3310	871
111153	3310	874
111154	3311	732
111155	3311	734
111156	3311	740
111157	3311	743
111158	3311	746
111159	3311	748
111160	3311	753
111161	3311	760
111162	3311	761
111163	3311	764
111164	3311	768
111165	3311	774
111166	3311	777
111167	3311	782
111168	3311	787
111169	3311	789
111170	3311	792
111171	3311	794
111172	3311	806
111173	3311	815
111174	3311	819
111175	3311	822
111176	3311	827
111177	3311	832
111178	3311	835
111179	3311	841
111180	3311	845
111181	3311	846
111182	3311	851
111183	3311	852
111184	3311	859
111185	3311	860
111186	3311	871
111187	3311	873
111188	3311	874
111189	3312	731
111190	3312	734
111191	3312	740
111192	3312	744
111193	3312	746
111194	3312	749
111195	3312	754
111196	3312	757
111197	3312	761
111198	3312	764
111199	3312	768
111200	3312	774
111201	3312	777
111202	3312	784
111203	3312	787
111204	3312	789
111205	3312	792
111206	3312	794
111207	3312	809
111208	3312	813
111209	3312	819
111210	3312	822
111211	3312	828
111212	3312	830
111213	3312	836
111214	3312	841
111215	3312	844
111216	3312	848
111217	3312	850
111218	3312	854
111219	3312	856
111220	3312	860
111221	3312	871
111222	3312	874
111223	3313	732
111224	3313	734
111225	3313	740
111226	3313	744
111227	3313	746
111228	3313	749
111229	3313	753
111230	3313	760
111231	3313	761
111232	3313	764
111233	3313	768
111234	3313	772
111235	3313	777
111236	3313	783
111237	3313	787
111238	3313	789
111239	3313	792
111240	3313	794
111241	3313	807
111242	3313	811
111243	3313	819
111244	3313	823
111245	3313	825
111246	3313	833
111247	3313	835
111248	3313	841
111249	3313	845
111250	3313	846
111251	3313	851
111252	3313	852
111253	3313	859
111254	3313	860
111255	3313	871
111256	3313	873
111257	3313	874
111258	3314	732
111259	3314	734
111260	3314	740
111261	3314	743
111262	3314	745
111263	3314	748
111264	3314	753
111265	3314	760
111266	3314	761
111267	3314	764
111268	3314	768
111269	3314	773
111270	3314	781
111271	3314	782
111272	3314	787
111273	3314	789
111274	3314	792
111275	3314	794
111276	3314	806
111277	3314	814
111278	3314	819
111279	3314	822
111280	3314	827
111281	3314	831
111282	3314	834
111283	3314	841
111284	3314	845
111285	3314	846
111286	3314	851
111287	3314	852
111288	3314	859
111289	3314	860
111290	3314	871
111291	3314	874
111292	3315	732
111293	3315	734
111294	3315	740
111295	3315	743
111296	3315	747
111297	3315	748
111298	3315	753
111299	3315	758
111300	3315	761
111301	3315	764
111302	3315	768
111303	3315	772
111304	3315	777
111305	3315	783
111306	3315	787
111307	3315	789
111308	3315	792
111309	3315	794
111310	3315	807
111311	3315	811
111312	3315	819
111313	3315	822
111314	3315	827
111315	3315	831
111316	3315	835
111317	3315	840
111318	3315	845
111319	3315	847
111320	3315	851
111321	3315	853
111322	3315	857
111323	3315	860
111324	3315	871
111325	3315	872
111326	3315	874
111327	3316	732
111328	3316	734
111329	3316	740
111330	3316	743
111331	3316	746
111332	3316	748
111333	3316	753
111334	3316	757
111335	3316	761
111336	3316	764
111337	3316	768
111338	3316	774
111339	3316	777
111340	3316	783
111341	3316	787
111342	3316	789
111343	3316	792
111344	3316	794
111345	3316	808
111346	3316	814
111347	3316	818
111348	3316	822
111349	3316	827
111350	3316	830
111351	3316	837
111352	3316	841
111353	3316	844
111354	3316	847
111355	3316	850
111356	3316	854
111357	3316	856
111358	3316	860
111359	3316	871
111360	3316	873
111361	3316	874
111362	3317	733
111363	3317	734
111364	3317	740
111365	3317	743
111366	3317	745
111367	3317	749
111368	3317	754
111369	3317	756
111370	3317	761
111371	3317	764
111372	3317	768
111373	3317	774
111374	3317	781
111375	3317	783
111376	3317	787
111377	3317	789
111378	3317	792
111379	3317	794
111380	3317	806
111381	3317	815
111382	3317	819
111383	3317	822
111384	3317	827
111385	3317	829
111386	3317	835
111387	3317	841
111388	3317	845
111389	3317	846
111390	3317	851
111391	3317	852
111392	3317	859
111393	3317	860
111394	3317	871
111395	3317	873
111396	3317	874
111397	3318	732
111398	3318	734
111399	3318	740
111400	3318	743
111401	3318	746
111402	3318	748
111403	3318	753
111404	3318	758
111405	3318	761
111406	3318	764
111407	3318	768
111408	3318	772
111409	3318	777
111410	3318	783
111411	3318	787
111412	3318	789
111413	3318	792
111414	3318	794
111415	3318	806
111416	3318	811
111417	3318	819
111418	3318	822
111419	3318	828
111420	3318	834
111421	3318	841
111422	3318	844
111423	3318	847
111424	3318	850
111425	3318	853
111426	3318	857
111427	3318	860
111428	3318	871
111429	3318	872
111430	3318	874
111431	3319	732
111432	3319	734
111433	3319	740
111434	3319	743
111435	3319	746
111436	3319	748
111437	3319	753
111438	3319	757
111439	3319	761
111440	3319	764
111441	3319	768
111442	3319	773
111443	3319	777
111444	3319	784
111445	3319	787
111446	3319	789
111447	3319	792
111448	3319	795
111449	3319	797
111450	3319	802
111451	3319	807
111452	3319	813
111453	3319	818
111454	3319	822
111455	3319	828
111456	3319	830
111457	3319	835
111458	3319	841
111459	3319	843
111460	3319	847
111461	3319	849
111462	3319	853
111463	3319	856
111464	3319	860
111465	3319	869
111466	3319	872
111467	3319	874
111468	3320	732
111469	3320	734
111470	3320	740
111471	3320	742
111472	3320	746
111473	3320	748
111474	3320	753
111475	3320	757
111476	3320	761
111477	3320	764
111478	3320	768
111479	3320	773
111480	3320	777
111481	3320	783
111482	3320	787
111483	3320	789
111484	3320	792
111485	3320	794
111486	3320	807
111487	3320	811
111488	3320	819
111489	3320	822
111490	3320	828
111491	3320	830
111492	3320	835
111493	3320	841
111494	3320	845
111495	3320	847
111496	3320	851
111497	3320	853
111498	3320	857
111499	3320	860
111500	3320	871
111501	3320	872
111502	3320	874
111503	3321	732
111504	3321	734
111505	3321	740
111506	3321	742
111507	3321	746
111508	3321	749
111509	3321	754
111510	3321	759
111511	3321	761
111512	3321	764
111513	3321	768
111514	3321	772
111515	3321	777
111516	3321	783
111517	3321	787
111518	3321	789
111519	3321	792
111520	3321	794
111521	3321	809
111522	3321	811
111523	3321	818
111524	3321	821
111525	3321	827
111526	3321	832
111527	3321	835
111528	3321	841
111529	3321	845
111530	3321	846
111531	3321	851
111532	3321	852
111533	3321	859
111534	3321	860
111535	3321	871
111536	3321	873
111537	3321	874
111538	3322	732
111539	3322	734
111540	3322	740
111541	3322	742
111542	3322	746
111543	3322	750
111544	3322	754
111545	3322	758
111546	3322	761
111547	3322	764
111548	3322	768
111549	3322	772
111550	3322	777
111551	3322	783
111552	3322	787
111553	3322	789
111554	3322	792
111555	3322	794
111556	3322	807
111557	3322	811
111558	3322	818
111559	3322	822
111560	3322	828
111561	3322	831
111562	3322	835
111563	3322	841
111564	3322	844
111565	3322	847
111566	3322	850
111567	3322	853
111568	3322	857
111569	3322	860
111570	3322	871
111571	3322	872
111572	3322	874
111573	3323	731
111574	3323	734
111575	3323	740
111576	3323	743
111577	3323	746
111578	3323	748
111579	3323	752
111580	3323	760
111581	3323	761
111582	3323	764
111583	3323	768
111584	3323	772
111585	3323	777
111586	3323	782
111587	3323	787
111588	3323	789
111589	3323	792
111590	3323	794
111591	3323	807
111592	3323	811
111593	3323	819
111594	3323	823
111595	3323	825
111596	3323	833
111597	3323	835
111598	3323	841
111599	3323	845
111600	3323	846
111601	3323	851
111602	3323	852
111603	3323	859
111604	3323	860
111605	3323	871
111606	3323	873
111607	3323	876
111608	3324	733
111609	3324	734
111610	3324	740
111611	3324	742
111612	3324	746
111613	3324	748
111614	3324	753
111615	3324	757
111616	3324	761
111617	3324	764
111618	3324	768
111619	3324	772
111620	3324	777
111621	3324	782
111622	3324	787
111623	3324	789
111624	3324	792
111625	3324	794
111626	3324	806
111627	3324	811
111628	3324	818
111629	3324	822
111630	3324	826
111631	3324	831
111632	3324	835
111633	3324	842
111634	3324	845
111635	3324	847
111636	3324	851
111637	3324	854
111638	3324	857
111639	3324	860
111640	3324	871
111641	3324	874
111642	3325	732
111643	3325	734
111644	3325	740
111645	3325	743
111646	3325	746
111647	3325	748
111648	3325	753
111649	3325	758
111650	3325	761
111651	3325	764
111652	3325	768
111653	3325	772
111654	3325	777
111655	3325	784
111656	3325	787
111657	3325	789
111658	3325	792
111659	3325	795
111660	3325	797
111661	3325	801
111662	3325	806
111663	3325	811
111664	3325	819
111665	3325	822
111666	3325	828
111667	3325	831
111668	3325	835
111669	3325	841
111670	3325	844
111671	3325	847
111672	3325	850
111673	3325	853
111674	3325	857
111675	3325	860
111676	3325	871
111677	3325	872
111678	3325	874
111679	3326	732
111680	3326	734
111681	3326	740
111682	3326	743
111683	3326	747
111684	3326	748
111685	3326	753
111686	3326	760
111687	3326	761
111688	3326	764
111689	3326	768
111690	3326	772
111691	3326	777
111692	3326	783
111693	3326	787
111694	3326	789
111695	3326	792
111696	3326	794
111697	3326	808
111698	3326	811
111699	3326	819
111700	3326	822
111701	3326	828
111702	3326	833
111703	3326	835
111704	3326	841
111705	3326	845
111706	3326	847
111707	3326	851
111708	3326	853
111709	3326	857
111710	3326	860
111711	3326	871
111712	3326	874
111713	3327	732
111714	3327	734
111715	3327	740
111716	3327	744
111717	3327	746
111718	3327	749
111719	3327	753
111720	3327	760
111721	3327	761
111722	3327	764
111723	3327	768
111724	3327	772
111725	3327	777
111726	3327	784
111727	3327	787
111728	3327	789
111729	3327	792
111730	3327	794
111731	3327	808
111732	3327	811
111733	3327	818
111734	3327	822
111735	3327	827
111736	3327	832
111737	3327	835
111738	3327	841
111739	3327	844
111740	3327	847
111741	3327	850
111742	3327	853
111743	3327	857
111744	3327	860
111745	3327	871
111746	3327	874
111747	3328	732
111748	3328	734
111749	3328	740
111750	3328	744
111751	3328	745
111752	3328	749
111753	3328	753
111754	3328	760
111755	3328	761
111756	3328	764
111757	3328	768
111758	3328	775
111759	3328	781
111760	3328	782
111761	3328	787
111762	3328	789
111763	3328	793
111764	3328	794
111765	3328	806
111766	3328	815
111767	3328	819
111768	3328	822
111769	3328	826
111770	3328	832
111771	3328	835
111772	3328	841
111773	3328	845
111774	3328	846
111775	3328	851
111776	3328	852
111777	3328	859
111778	3328	860
111779	3328	871
111780	3328	872
111781	3328	874
111782	3329	732
111783	3329	734
111784	3329	740
111785	3329	743
111786	3329	747
111787	3329	749
111788	3329	754
111789	3329	757
111790	3329	761
111791	3329	764
111792	3329	768
111793	3329	772
111794	3329	777
111795	3329	784
111796	3329	787
111797	3329	789
111798	3329	792
111799	3329	794
111800	3329	808
111801	3329	811
111802	3329	819
111803	3329	823
111804	3329	828
111805	3329	832
111806	3329	835
111807	3329	841
111808	3329	845
111809	3329	847
111810	3329	851
111811	3329	853
111812	3329	857
111813	3329	860
111814	3329	871
111815	3329	872
111816	3329	874
111817	3330	732
111818	3330	734
111819	3330	740
111820	3330	742
111821	3330	746
111822	3330	749
111823	3330	753
111824	3330	758
111825	3330	761
111826	3330	764
111827	3330	768
111828	3330	772
111829	3330	777
111830	3330	783
111831	3330	787
111832	3330	789
111833	3330	792
111834	3330	794
111835	3330	808
111836	3330	811
111837	3330	818
111838	3330	822
111839	3330	828
111840	3330	835
111841	3330	841
111842	3330	843
111843	3330	847
111844	3330	849
111845	3330	853
111846	3330	856
111847	3330	860
111848	3330	871
111849	3330	872
111850	3330	874
111851	3331	732
111852	3331	734
111853	3331	740
111854	3331	744
111855	3331	747
111856	3331	749
111857	3331	754
111858	3331	760
111859	3331	761
111860	3331	764
111861	3331	768
111862	3331	772
111863	3331	777
111864	3331	787
111865	3331	789
111866	3331	794
111867	3331	806
111868	3331	811
111869	3331	819
111870	3331	822
111871	3331	828
111872	3331	835
111873	3331	857
111874	3331	860
111875	3331	871
111876	3331	872
111877	3331	874
111878	3332	732
111879	3332	734
111880	3332	740
111881	3332	744
111882	3332	745
111883	3332	750
111884	3332	754
111885	3332	758
111886	3332	761
111887	3332	764
111888	3332	768
111889	3332	772
111890	3332	777
111891	3332	784
111892	3332	787
111893	3332	789
111894	3332	792
111895	3332	794
111896	3332	806
111897	3332	811
111898	3332	819
111899	3332	823
111900	3332	828
111901	3332	830
111902	3332	835
111903	3332	841
111904	3332	845
111905	3332	847
111906	3332	851
111907	3332	853
111908	3332	858
111909	3332	860
111910	3332	871
111911	3332	872
111912	3332	874
111913	3333	732
111914	3333	734
111915	3333	740
111916	3333	744
111917	3333	746
111918	3333	750
111919	3333	754
111920	3333	757
111921	3333	761
111922	3333	764
111923	3333	768
111924	3333	772
111925	3333	777
111926	3333	785
111927	3333	787
111928	3333	789
111929	3333	792
111930	3333	794
111931	3333	806
111932	3333	811
111933	3333	819
111934	3333	822
111935	3333	828
111936	3333	831
111937	3333	835
111938	3333	842
111939	3333	845
111940	3333	847
111941	3333	851
111942	3333	854
111943	3333	857
111944	3333	860
111945	3333	871
111946	3333	873
111947	3333	874
111948	3334	732
111949	3334	734
111950	3334	740
111951	3334	744
111952	3334	747
111953	3334	750
111954	3334	755
111955	3334	756
111956	3334	761
111957	3334	764
111958	3334	768
111959	3334	775
111960	3334	781
111961	3334	785
111962	3334	787
111963	3334	789
111964	3334	793
111965	3334	794
111966	3334	807
111967	3334	815
111968	3334	819
111969	3334	823
111970	3334	828
111971	3334	831
111972	3334	835
111973	3334	841
111974	3334	843
111975	3334	847
111976	3334	850
111977	3334	854
111978	3334	856
111979	3334	860
111980	3334	871
111981	3334	872
111982	3334	874
111983	3335	732
111984	3335	734
111985	3335	740
111986	3335	742
111987	3335	747
111988	3335	749
111989	3335	753
111990	3335	758
111991	3335	761
111992	3335	764
111993	3335	768
111994	3335	774
111995	3335	777
111996	3335	783
111997	3335	787
111998	3335	789
111999	3335	792
112000	3335	794
112001	3335	809
112002	3335	815
112003	3335	818
112004	3335	821
112005	3335	827
112006	3335	832
112007	3335	837
112008	3335	841
112009	3335	843
112010	3335	847
112011	3335	849
112012	3335	854
112013	3335	856
112014	3335	860
112015	3335	871
112016	3335	873
112017	3335	874
112018	3336	733
112019	3336	734
112020	3336	740
112021	3336	742
112022	3336	745
112023	3336	750
112024	3336	754
112025	3336	758
112026	3336	761
112027	3336	764
112028	3336	768
112029	3336	774
112030	3336	777
112031	3336	783
112032	3336	787
112033	3336	789
112034	3336	793
112035	3336	794
112036	3336	807
112037	3336	814
112038	3336	819
112039	3336	822
112040	3336	827
112041	3336	831
112042	3336	834
112043	3336	840
112044	3336	845
112045	3336	846
112046	3336	851
112047	3336	852
112048	3336	859
112049	3336	860
112050	3336	871
112051	3336	872
112052	3336	874
112053	3337	732
112054	3337	734
112055	3337	740
112056	3337	743
112057	3337	746
112058	3337	749
112059	3337	753
112060	3337	759
112061	3337	761
112062	3337	764
112063	3337	768
112064	3337	775
112065	3337	777
112066	3337	783
112067	3337	787
112068	3337	789
112069	3337	792
112070	3337	794
112071	3337	806
112072	3337	816
112073	3337	819
112074	3337	823
112075	3337	827
112076	3337	831
112077	3337	835
112078	3337	840
112079	3337	845
112080	3337	846
112081	3337	851
112082	3337	852
112083	3337	859
112084	3337	860
112085	3337	871
112086	3337	873
112087	3337	874
112088	3338	732
112089	3338	734
112090	3338	740
112091	3338	742
112092	3338	747
112093	3338	749
112094	3338	754
112095	3338	759
112096	3338	761
112097	3338	764
112098	3338	768
112099	3338	774
112100	3338	777
112101	3338	784
112102	3338	787
112103	3338	789
112104	3338	792
112105	3338	794
112106	3338	808
112107	3338	814
112108	3338	818
112109	3338	822
112110	3338	827
112111	3338	831
112112	3338	836
112113	3338	841
112114	3338	845
112115	3338	847
112116	3338	851
112117	3338	853
112118	3338	858
112119	3338	860
112120	3338	871
112121	3338	872
112122	3338	874
112123	3339	732
112124	3339	734
112125	3339	740
112126	3339	742
112127	3339	746
112128	3339	749
112129	3339	753
112130	3339	758
112131	3339	761
112132	3339	764
112133	3339	768
112134	3339	772
112135	3339	777
112136	3339	784
112137	3339	787
112138	3339	789
112139	3339	792
112140	3339	795
112141	3339	799
112142	3339	803
112143	3339	808
112144	3339	811
112145	3339	818
112146	3339	822
112147	3339	828
112148	3339	831
112149	3339	835
112150	3339	841
112151	3339	843
112152	3339	847
112153	3339	849
112154	3339	853
112155	3339	856
112156	3339	860
112157	3339	871
112158	3339	872
112159	3339	874
112160	3340	732
112161	3340	734
112162	3340	740
112163	3340	743
112164	3340	746
112165	3340	749
112166	3340	753
112167	3340	759
112168	3340	761
112169	3340	764
112170	3340	768
112171	3340	772
112172	3340	777
112173	3340	785
112174	3340	787
112175	3340	789
112176	3340	792
112177	3340	794
112178	3340	808
112179	3340	811
112180	3340	818
112181	3340	822
112182	3340	826
112183	3340	832
112184	3340	835
112185	3340	841
112186	3340	845
112187	3340	847
112188	3340	851
112189	3340	853
112190	3340	857
112191	3340	860
112192	3340	871
112193	3340	872
112194	3340	874
112195	3341	732
112196	3341	734
112197	3341	740
112198	3341	743
112199	3341	747
112200	3341	749
112201	3341	753
112202	3341	757
112203	3341	761
112204	3341	764
112205	3341	768
112206	3341	772
112207	3341	777
112208	3341	783
112209	3341	787
112210	3341	789
112211	3341	792
112212	3341	794
112213	3341	808
112214	3341	811
112215	3341	818
112216	3341	822
112217	3341	828
112218	3341	831
112219	3341	835
112220	3341	841
112221	3341	845
112222	3341	846
112223	3341	851
112224	3341	852
112225	3341	858
112226	3341	860
112227	3341	871
112228	3341	872
112229	3341	874
112230	3342	732
112231	3342	734
112232	3342	740
112233	3342	744
112234	3342	746
112235	3342	749
112236	3342	753
112237	3342	760
112238	3342	761
112239	3342	764
112240	3342	768
112241	3342	772
112242	3342	777
112243	3342	783
112244	3342	787
112245	3342	789
112246	3342	792
112247	3342	794
112248	3342	808
112249	3342	811
112250	3342	818
112251	3342	822
112252	3342	827
112253	3342	832
112254	3342	835
112255	3342	841
112256	3342	845
112257	3342	847
112258	3342	851
112259	3342	853
112260	3342	857
112261	3342	860
112262	3342	871
112263	3342	874
112264	3343	732
112265	3343	734
112266	3343	740
112267	3343	743
112268	3343	746
112269	3343	749
112270	3343	753
112271	3343	760
112272	3343	761
112273	3343	764
112274	3343	768
112275	3343	772
112276	3343	777
112277	3343	783
112278	3343	787
112279	3343	789
112280	3343	792
112281	3343	794
112282	3343	809
112283	3343	811
112284	3343	819
112285	3343	823
112286	3343	828
112287	3343	832
112288	3343	835
112289	3343	842
112290	3343	844
112291	3343	848
112292	3343	850
112293	3343	854
112294	3343	856
112295	3343	860
112296	3343	871
112297	3343	872
112298	3343	874
112299	3344	732
112300	3344	734
112301	3344	740
112302	3344	744
112303	3344	746
112304	3344	750
112305	3344	754
112306	3344	760
112307	3344	761
112308	3344	764
112309	3344	768
112310	3344	772
112311	3344	777
112312	3344	783
112313	3344	787
112314	3344	789
112315	3344	792
112316	3344	794
112317	3344	808
112318	3344	811
112319	3344	819
112320	3344	822
112321	3344	827
112322	3344	833
112323	3344	835
112324	3344	842
112325	3344	845
112326	3344	847
112327	3344	851
112328	3344	853
112329	3344	859
112330	3344	860
112331	3344	871
112332	3344	874
112333	3345	732
112334	3345	734
112335	3345	740
112336	3345	743
112337	3345	745
112338	3345	749
112339	3345	753
112340	3345	757
112341	3345	761
112342	3345	764
112343	3345	768
112344	3345	772
112345	3345	777
112346	3345	783
112347	3345	787
112348	3345	789
112349	3345	792
112350	3345	794
112351	3345	807
112352	3345	811
112353	3345	819
112354	3345	822
112355	3345	825
112356	3345	830
112357	3345	835
112358	3345	841
112359	3345	845
112360	3345	846
112361	3345	851
112362	3345	852
112363	3345	859
112364	3345	860
112365	3345	871
112366	3345	873
112367	3345	874
112368	3346	732
112369	3346	734
112370	3346	740
112371	3346	744
112372	3346	746
112373	3346	750
112374	3346	754
112375	3346	759
112376	3346	761
112377	3346	764
112378	3346	768
112379	3346	775
112380	3346	777
112381	3346	784
112382	3346	787
112383	3346	789
112384	3346	793
112385	3346	794
112386	3346	806
112387	3346	816
112388	3346	819
112389	3346	823
112390	3346	828
112391	3346	831
112392	3346	835
112393	3346	840
112394	3346	844
112395	3346	846
112396	3346	851
112397	3346	852
112398	3346	859
112399	3346	860
112400	3346	871
112401	3346	873
112402	3346	874
112403	3347	733
112404	3347	735
112405	3347	737
112406	3347	740
112407	3347	743
112408	3347	746
112409	3347	748
112410	3347	752
112411	3347	760
112412	3347	761
112413	3347	764
112414	3347	768
112415	3347	772
112416	3347	777
112417	3347	782
112418	3347	787
112419	3347	789
112420	3347	793
112421	3347	794
112422	3347	806
112423	3347	811
112424	3347	819
112425	3347	822
112426	3347	825
112427	3347	832
112428	3347	834
112429	3347	840
112430	3347	845
112431	3347	846
112432	3347	851
112433	3347	852
112434	3347	859
112435	3347	860
112436	3347	871
112437	3347	874
112438	3348	732
112439	3348	734
112440	3348	740
112441	3348	743
112442	3348	746
112443	3348	749
112444	3348	753
112445	3348	760
112446	3348	761
112447	3348	764
112448	3348	768
112449	3348	774
112450	3348	781
112451	3348	782
112452	3348	787
112453	3348	789
112454	3348	792
112455	3348	794
112456	3348	806
112457	3348	815
112458	3348	819
112459	3348	822
112460	3348	827
112461	3348	833
112462	3348	834
112463	3348	841
112464	3348	845
112465	3348	846
112466	3348	851
112467	3348	852
112468	3348	859
112469	3348	860
112470	3348	871
112471	3348	874
112472	3349	732
112473	3349	734
112474	3349	740
112475	3349	742
112476	3349	746
112477	3349	749
112478	3349	753
112479	3349	757
112480	3349	761
112481	3349	764
112482	3349	768
112483	3349	772
112484	3349	777
112485	3349	783
112486	3349	787
112487	3349	789
112488	3349	792
112489	3349	794
112490	3349	808
112491	3349	811
112492	3349	818
112493	3349	822
112494	3349	827
112495	3349	831
112496	3349	835
112497	3349	840
112498	3349	845
112499	3349	847
112500	3349	850
112501	3349	853
112502	3349	857
112503	3349	860
112504	3349	871
112505	3349	872
112506	3349	874
112507	3350	733
112508	3350	734
112509	3350	740
112510	3350	743
112511	3350	747
112512	3350	748
112513	3350	753
112514	3350	757
112515	3350	761
112516	3350	764
112517	3350	768
112518	3350	772
112519	3350	777
112520	3350	782
112521	3350	787
112522	3350	789
112523	3350	791
112524	3350	794
112525	3350	806
112526	3350	811
112527	3350	818
112528	3350	822
112529	3350	827
112530	3350	831
112531	3350	835
112532	3350	841
112533	3350	844
112534	3350	847
112535	3350	850
112536	3350	854
112537	3350	856
112538	3350	860
112539	3350	871
112540	3350	872
112541	3350	874
112542	3351	732
112543	3351	734
112544	3351	740
112545	3351	743
112546	3351	745
112547	3351	749
112548	3351	753
112549	3351	758
112550	3351	761
112551	3351	764
112552	3351	768
112553	3351	776
112554	3351	781
112555	3351	783
112556	3351	787
112557	3351	789
112558	3351	792
112559	3351	794
112560	3351	806
112561	3351	816
112562	3351	819
112563	3351	822
112564	3351	827
112565	3351	831
112566	3351	835
112567	3351	840
112568	3351	845
112569	3351	846
112570	3351	851
112571	3351	852
112572	3351	859
112573	3351	860
112574	3351	871
112575	3351	873
112576	3351	876
112577	3352	732
112578	3352	734
112579	3352	740
112580	3352	744
112581	3352	746
112582	3352	749
112583	3352	754
112584	3352	757
112585	3352	761
112586	3352	764
112587	3352	768
112588	3352	772
112589	3352	777
112590	3352	784
112591	3352	787
112592	3352	789
112593	3352	792
112594	3352	794
112595	3352	808
112596	3352	811
112597	3352	819
112598	3352	822
112599	3352	828
112600	3352	831
112601	3352	835
112602	3352	841
112603	3352	844
112604	3352	847
112605	3352	850
112606	3352	853
112607	3352	857
112608	3352	860
112609	3352	871
112610	3352	874
112611	3353	733
112612	3353	734
112613	3353	740
112614	3353	744
112615	3353	746
112616	3353	749
112617	3353	753
112618	3353	760
112619	3353	761
112620	3353	764
112621	3353	768
112622	3353	772
112623	3353	777
112624	3353	783
112625	3353	787
112626	3353	789
112627	3353	793
112628	3353	795
112629	3353	796
112630	3353	801
112631	3353	809
112632	3353	811
112633	3353	819
112634	3353	823
112635	3353	827
112636	3353	833
112637	3353	835
112638	3353	842
112639	3353	845
112640	3353	848
112641	3353	851
112642	3353	854
112643	3353	857
112644	3353	860
112645	3353	871
112646	3353	872
112647	3353	874
112648	3354	732
112649	3354	734
112650	3354	740
112651	3354	743
112652	3354	747
112653	3354	749
112654	3354	753
112655	3354	758
112656	3354	761
112657	3354	764
112658	3354	768
112659	3354	772
112660	3354	777
112661	3354	783
112662	3354	787
112663	3354	789
112664	3354	792
112665	3354	794
112666	3354	809
112667	3354	811
112668	3354	818
112669	3354	822
112670	3354	828
112671	3354	830
112672	3354	834
112673	3354	842
112674	3354	845
112675	3354	847
112676	3354	851
112677	3354	854
112678	3354	857
112679	3354	860
112680	3354	871
112681	3354	872
112682	3354	874
112683	3355	733
112684	3355	734
112685	3355	740
112686	3355	744
112687	3355	746
112688	3355	749
112689	3355	753
112690	3355	760
112691	3355	761
112692	3355	764
112693	3355	768
112694	3355	772
112695	3355	777
112696	3355	782
112697	3355	787
112698	3355	789
112699	3355	792
112700	3355	794
112701	3355	808
112702	3355	811
112703	3355	818
112704	3355	822
112705	3355	828
112706	3355	831
112707	3355	834
112708	3355	840
112709	3355	845
112710	3355	846
112711	3355	851
112712	3355	852
112713	3355	859
112714	3355	860
112715	3355	871
112716	3355	874
112717	3356	732
112718	3356	734
112719	3356	740
112720	3356	744
112721	3356	747
112722	3356	749
112723	3356	754
112724	3356	758
112725	3356	761
112726	3356	764
112727	3356	768
112728	3356	776
112729	3356	781
112730	3356	784
112731	3356	787
112732	3356	789
112733	3356	791
112734	3356	794
112735	3356	809
112736	3356	816
112737	3356	818
112738	3356	822
112739	3356	827
112740	3356	832
112741	3356	835
112742	3356	840
112743	3356	845
112744	3356	846
112745	3356	851
112746	3356	852
112747	3356	859
112748	3356	865
112749	3356	871
112750	3356	872
112751	3356	874
112752	3357	733
112753	3357	734
112754	3357	740
112755	3357	743
112756	3357	746
112757	3357	748
112758	3357	752
112759	3357	760
112760	3357	761
112761	3357	764
112762	3357	768
112763	3357	775
112764	3357	781
112765	3357	783
112766	3357	787
112767	3357	789
112768	3357	792
112769	3357	795
112770	3357	798
112771	3357	803
112772	3357	806
112773	3357	815
112774	3357	819
112775	3357	823
112776	3357	828
112777	3357	832
112778	3357	835
112779	3357	841
112780	3357	845
112781	3357	846
112782	3357	851
112783	3357	852
112784	3357	859
112785	3357	860
112786	3357	871
112787	3357	873
112788	3357	876
112789	3358	731
112790	3358	734
112791	3358	740
112792	3358	744
112793	3358	746
112794	3358	749
112795	3358	754
112796	3358	760
112797	3358	761
112798	3358	764
112799	3358	768
112800	3358	772
112801	3358	777
112802	3358	784
112803	3358	787
112804	3358	789
112805	3358	792
112806	3358	794
112807	3358	806
112808	3358	811
112809	3358	818
112810	3358	822
112811	3358	828
112812	3358	832
112813	3358	835
112814	3358	842
112815	3358	845
112816	3358	848
112817	3358	851
112818	3358	854
112819	3358	856
112820	3358	860
112821	3358	871
112822	3358	873
112823	3358	874
112824	3359	732
112825	3359	734
112826	3359	740
112827	3359	743
112828	3359	747
112829	3359	749
112830	3359	753
112831	3359	760
112832	3359	761
112833	3359	764
112834	3359	768
112835	3359	772
112836	3359	777
112837	3359	782
112838	3359	787
112839	3359	789
112840	3359	792
112841	3359	794
112842	3359	809
112843	3359	811
112844	3359	818
112845	3359	822
112846	3359	826
112847	3359	833
112848	3359	835
112849	3359	841
112850	3359	844
112851	3359	847
112852	3359	850
112853	3359	854
112854	3359	856
112855	3359	860
112856	3359	871
112857	3359	872
112858	3359	874
112859	3360	732
112860	3360	734
112861	3360	740
112862	3360	744
112863	3360	745
112864	3360	750
112865	3360	755
112866	3360	758
112867	3360	761
112868	3360	764
112869	3360	768
112870	3360	775
112871	3360	781
112872	3360	782
112873	3360	787
112874	3360	789
112875	3360	792
112876	3360	794
112877	3360	808
112878	3360	815
112879	3360	819
112880	3360	822
112881	3360	826
112882	3360	830
112883	3360	835
112884	3360	841
112885	3360	845
112886	3360	846
112887	3360	851
112888	3360	852
112889	3360	859
112890	3360	860
112891	3360	871
112892	3360	873
112893	3360	874
112894	3361	732
112895	3361	734
112896	3361	740
112897	3361	744
112898	3361	746
112899	3361	749
112900	3361	754
112901	3361	758
112902	3361	761
112903	3361	764
112904	3361	768
112905	3361	772
112906	3361	777
112907	3361	784
112908	3361	787
112909	3361	789
112910	3361	792
112911	3361	794
112912	3361	806
112913	3361	811
112914	3361	818
112915	3361	822
112916	3361	827
112917	3361	832
112918	3361	835
112919	3361	842
112920	3361	845
112921	3361	848
112922	3361	851
112923	3361	854
112924	3361	857
112925	3361	860
112926	3361	871
112927	3361	872
112928	3361	874
112929	3362	732
112930	3362	734
112931	3362	740
112932	3362	744
112933	3362	746
112934	3362	748
112935	3362	752
112936	3362	760
112937	3362	761
112938	3362	764
112939	3362	768
112940	3362	772
112941	3362	777
112942	3362	783
112943	3362	787
112944	3362	789
112945	3362	792
112946	3362	794
112947	3362	806
112948	3362	811
112949	3362	819
112950	3362	823
112951	3362	826
112952	3362	832
112953	3362	835
112954	3362	840
112955	3362	845
112956	3362	846
112957	3362	851
112958	3362	852
112959	3362	859
112960	3362	860
112961	3362	871
112962	3362	873
112963	3362	874
112964	3363	732
112965	3363	734
112966	3363	740
112967	3363	742
112968	3363	746
112969	3363	749
112970	3363	754
112971	3363	757
112972	3363	761
112973	3363	764
112974	3363	768
112975	3363	772
112976	3363	777
112977	3363	783
112978	3363	787
112979	3363	789
112980	3363	792
112981	3363	794
112982	3363	806
112983	3363	811
112984	3363	819
112985	3363	823
112986	3363	828
112987	3363	830
112988	3363	835
112989	3363	841
112990	3363	845
112991	3363	846
112992	3363	851
112993	3363	852
112994	3363	859
112995	3363	860
112996	3363	871
112997	3363	872
112998	3363	876
112999	3364	732
113000	3364	734
113001	3364	740
113002	3364	744
113003	3364	746
113004	3364	749
113005	3364	754
113006	3364	758
113007	3364	761
113008	3364	764
113009	3364	770
113010	3364	776
113011	3364	781
113012	3364	786
113013	3364	787
113014	3364	789
113015	3364	793
113016	3364	795
113017	3364	796
113018	3364	803
113019	3364	810
113020	3364	816
113021	3364	819
113022	3364	823
113023	3364	828
113024	3364	832
113025	3364	837
113026	3364	842
113027	3364	845
113028	3364	848
113029	3364	851
113030	3364	854
113031	3364	857
113032	3364	860
113033	3364	871
113034	3364	874
113035	3365	732
113036	3365	734
113037	3365	740
113038	3365	742
113039	3365	745
113040	3365	748
113041	3365	753
113042	3365	758
113043	3365	761
113044	3365	764
113045	3365	768
113046	3365	775
113047	3365	781
113048	3365	783
113049	3365	787
113050	3365	789
113051	3365	792
113052	3365	794
113053	3365	806
113054	3365	815
113055	3365	818
113056	3365	822
113057	3365	825
113058	3365	835
113059	3365	841
113060	3365	845
113061	3365	846
113062	3365	851
113063	3365	852
113064	3365	859
113065	3365	860
113066	3365	871
113067	3365	873
113068	3365	876
113069	3366	732
113070	3366	734
113071	3366	740
113072	3366	744
113073	3366	745
113074	3366	748
113075	3366	753
113076	3366	760
113077	3366	761
113078	3366	764
113079	3366	768
113080	3366	775
113081	3366	777
113082	3366	783
113083	3366	787
113084	3366	789
113085	3366	792
113086	3366	795
113087	3366	797
113088	3366	802
113089	3366	806
113090	3366	814
113091	3366	819
113092	3366	822
113093	3366	826
113094	3366	832
113095	3366	835
113096	3366	841
113097	3366	845
113098	3366	846
113099	3366	851
113100	3366	852
113101	3366	859
113102	3366	860
113103	3366	871
113104	3366	873
113105	3366	874
113106	3367	732
113107	3367	734
113108	3367	740
113109	3367	743
113110	3367	745
113111	3367	749
113112	3367	753
113113	3367	758
113114	3367	761
113115	3367	764
113116	3367	768
113117	3367	773
113118	3367	777
113119	3367	783
113120	3367	787
113121	3367	789
113122	3367	792
113123	3367	794
113124	3367	806
113125	3367	814
113126	3367	819
113127	3367	822
113128	3367	827
113129	3367	830
113130	3367	834
113131	3367	840
113132	3367	845
113133	3367	846
113134	3367	851
113135	3367	852
113136	3367	859
113137	3367	860
113138	3367	871
113139	3367	873
113140	3367	874
113141	3368	733
113142	3368	734
113143	3368	740
113144	3368	742
113145	3368	746
113146	3368	749
113147	3368	753
113148	3368	760
113149	3368	761
113150	3368	764
113151	3368	768
113152	3368	772
113153	3368	777
113154	3368	782
113155	3368	787
113156	3368	789
113157	3368	791
113158	3368	794
113159	3368	806
113160	3368	811
113161	3368	818
113162	3368	821
113163	3368	826
113164	3368	833
113165	3368	835
113166	3368	842
113167	3368	844
113168	3368	847
113169	3368	850
113170	3368	854
113171	3368	856
113172	3368	860
113173	3368	871
113174	3368	872
113175	3368	874
113176	3369	732
113177	3369	734
113178	3369	740
113179	3369	743
113180	3369	746
113181	3369	748
113182	3369	754
113183	3369	757
113184	3369	761
113185	3369	764
113186	3369	768
113187	3369	772
113188	3369	777
113189	3369	783
113190	3369	787
113191	3369	789
113192	3369	792
113193	3369	795
113194	3369	797
113195	3369	801
113196	3369	809
113197	3369	811
113198	3369	819
113199	3369	822
113200	3369	827
113201	3369	831
113202	3369	835
113203	3369	842
113204	3369	845
113205	3369	848
113206	3369	851
113207	3369	854
113208	3369	857
113209	3369	860
113210	3369	871
113211	3369	872
113212	3369	874
113213	3370	732
113214	3370	734
113215	3370	740
113216	3370	743
113217	3370	746
113218	3370	748
113219	3370	753
113220	3370	757
113221	3370	761
113222	3370	764
113223	3370	768
113224	3370	772
113225	3370	777
113226	3370	782
113227	3370	787
113228	3370	789
113229	3370	792
113230	3370	794
113231	3370	808
113232	3370	811
113233	3370	819
113234	3370	823
113235	3370	828
113236	3370	830
113237	3370	835
113238	3370	841
113239	3370	845
113240	3370	847
113241	3370	851
113242	3370	853
113243	3370	857
113244	3370	860
113245	3370	871
113246	3370	874
113247	3371	732
113248	3371	734
113249	3371	740
113250	3371	743
113251	3371	746
113252	3371	749
113253	3371	754
113254	3371	758
113255	3371	761
113256	3371	764
113257	3371	768
113258	3371	776
113259	3371	781
113260	3371	784
113261	3371	787
113262	3371	790
113263	3371	792
113264	3371	794
113265	3371	806
113266	3371	816
113267	3371	818
113268	3371	822
113269	3371	828
113270	3371	830
113271	3371	835
113272	3371	840
113273	3371	845
113274	3371	846
113275	3371	851
113276	3371	852
113277	3371	859
113278	3371	860
113279	3371	871
113280	3371	873
113281	3371	874
113282	3372	732
113283	3372	734
113284	3372	740
113285	3372	743
113286	3372	746
113287	3372	748
113288	3372	753
113289	3372	759
113290	3372	761
113291	3372	764
113292	3372	768
113293	3372	772
113294	3372	777
113295	3372	783
113296	3372	787
113297	3372	789
113298	3372	792
113299	3372	794
113300	3372	806
113301	3372	811
113302	3372	819
113303	3372	823
113304	3372	827
113305	3372	833
113306	3372	835
113307	3372	840
113308	3372	844
113309	3372	847
113310	3372	850
113311	3372	853
113312	3372	857
113313	3372	860
113314	3372	871
113315	3372	874
113316	3373	732
113317	3373	734
113318	3373	740
113319	3373	744
113320	3373	745
113321	3373	749
113322	3373	754
113323	3373	760
113324	3373	761
113325	3373	764
113326	3373	768
113327	3373	772
113328	3373	777
113329	3373	783
113330	3373	787
113331	3373	789
113332	3373	793
113333	3373	795
113334	3373	797
113335	3373	803
113336	3373	806
113337	3373	811
113338	3373	819
113339	3373	822
113340	3373	828
113341	3373	833
113342	3373	835
113343	3373	841
113344	3373	844
113345	3373	847
113346	3373	850
113347	3373	853
113348	3373	856
113349	3373	860
113350	3373	871
113351	3373	872
113352	3373	874
113353	3374	732
113354	3374	734
113355	3374	740
113356	3374	743
113357	3374	746
113358	3374	749
113359	3374	753
113360	3374	757
113361	3374	761
113362	3374	764
113363	3374	768
113364	3374	772
113365	3374	777
113366	3374	783
113367	3374	787
113368	3374	789
113369	3374	792
113370	3374	794
113371	3374	810
113372	3374	811
113373	3374	819
113374	3374	823
113375	3374	828
113376	3374	832
113377	3374	835
113378	3374	842
113379	3374	844
113380	3374	848
113381	3374	850
113382	3374	854
113383	3374	856
113384	3374	860
113385	3374	871
113386	3374	872
113387	3374	874
113388	3375	731
113389	3375	734
113390	3375	740
113391	3375	744
113392	3375	745
113393	3375	749
113394	3375	754
113395	3375	760
113396	3375	761
113397	3375	764
113398	3375	768
113399	3375	775
113400	3375	781
113401	3375	782
113402	3375	787
113403	3375	789
113404	3375	793
113405	3375	794
113406	3375	807
113407	3375	815
113408	3375	819
113409	3375	822
113410	3375	827
113411	3375	831
113412	3375	834
113413	3375	840
113414	3375	845
113415	3375	846
113416	3375	851
113417	3375	852
113418	3375	859
113419	3375	860
113420	3375	871
113421	3375	874
113422	3376	733
113423	3376	734
113424	3376	740
113425	3376	744
113426	3376	747
113427	3376	749
113428	3376	753
113429	3376	758
113430	3376	761
113431	3376	764
113432	3376	769
113433	3376	775
113434	3376	777
113435	3376	783
113436	3376	787
113437	3376	789
113438	3376	792
113439	3376	794
113440	3376	806
113441	3376	815
113442	3376	819
113443	3376	822
113444	3376	827
113445	3376	832
113446	3376	835
113447	3376	841
113448	3376	845
113449	3376	846
113450	3376	851
113451	3376	852
113452	3376	859
113453	3376	860
113454	3376	871
113455	3376	872
113456	3376	874
113457	3377	732
113458	3377	734
113459	3377	740
113460	3377	743
113461	3377	746
113462	3377	748
113463	3377	753
113464	3377	760
113465	3377	761
113466	3377	764
113467	3377	768
113468	3377	772
113469	3377	777
113470	3377	783
113471	3377	787
113472	3377	789
113473	3377	792
113474	3377	795
113475	3377	797
113476	3377	802
113477	3377	806
113478	3377	811
113479	3377	819
113480	3377	823
113481	3377	828
113482	3377	832
113483	3377	835
113484	3377	842
113485	3377	844
113486	3377	847
113487	3377	850
113488	3377	854
113489	3377	856
113490	3377	860
113491	3377	871
113492	3377	872
113493	3377	874
113494	3378	732
113495	3378	734
113496	3378	740
113497	3378	742
113498	3378	746
113499	3378	749
113500	3378	753
113501	3378	760
113502	3378	761
113503	3378	764
113504	3378	769
113505	3378	774
113506	3378	777
113507	3378	784
113508	3378	787
113509	3378	789
113510	3378	792
113511	3378	794
113512	3378	809
113513	3378	814
113514	3378	818
113515	3378	821
113516	3378	828
113517	3378	833
113518	3378	835
113519	3378	841
113520	3378	844
113521	3378	848
113522	3378	850
113523	3378	854
113524	3378	856
113525	3378	860
113526	3378	871
113527	3378	873
113528	3378	874
113529	3379	731
113530	3379	734
113531	3379	740
113532	3379	744
113533	3379	746
113534	3379	749
113535	3379	753
113536	3379	758
113537	3379	761
113538	3379	764
113539	3379	768
113540	3379	772
113541	3379	777
113542	3379	784
113543	3379	787
113544	3379	789
113545	3379	792
113546	3379	795
113547	3379	800
113548	3379	803
113549	3379	807
113550	3379	815
113551	3379	819
113552	3379	823
113553	3379	827
113554	3379	832
113555	3379	837
113556	3379	842
113557	3379	845
113558	3379	848
113559	3379	851
113560	3379	854
113561	3379	857
113562	3379	860
113563	3379	871
113564	3379	872
113565	3379	874
113566	3380	732
113567	3380	734
113568	3380	740
113569	3380	743
113570	3380	746
113571	3380	748
113572	3380	752
113573	3380	760
113574	3380	761
113575	3380	764
113576	3380	768
113577	3380	772
113578	3380	777
113579	3380	783
113580	3380	787
113581	3380	789
113582	3380	793
113583	3380	795
113584	3380	796
113585	3380	803
113586	3380	806
113587	3380	811
113588	3380	819
113589	3380	823
113590	3380	828
113591	3380	833
113592	3380	835
113593	3380	841
113594	3380	845
113595	3380	846
113596	3380	851
113597	3380	852
113598	3380	859
113599	3380	860
113600	3380	871
113601	3380	874
113602	3381	732
113603	3381	734
113604	3381	740
113605	3381	743
113606	3381	747
113607	3381	749
113608	3381	754
113609	3381	760
113610	3381	761
113611	3381	764
113612	3381	768
113613	3381	772
113614	3381	777
113615	3381	783
113616	3381	787
113617	3381	789
113618	3381	792
113619	3381	794
113620	3381	809
113621	3381	811
113622	3381	818
113623	3381	821
113624	3381	828
113625	3381	833
113626	3381	835
113627	3381	840
113628	3381	844
113629	3381	847
113630	3381	850
113631	3381	853
113632	3381	857
113633	3381	860
113634	3381	871
113635	3381	874
113636	3382	732
113637	3382	734
113638	3382	740
113639	3382	744
113640	3382	746
113641	3382	750
113642	3382	754
113643	3382	757
113644	3382	761
113645	3382	764
113646	3382	768
113647	3382	772
113648	3382	777
113649	3382	783
113650	3382	787
113651	3382	789
113652	3382	792
113653	3382	794
113654	3382	809
113655	3382	811
113656	3382	819
113657	3382	822
113658	3382	827
113659	3382	830
113660	3382	835
113661	3382	841
113662	3382	844
113663	3382	847
113664	3382	850
113665	3382	853
113666	3382	857
113667	3382	860
113668	3382	869
113669	3382	872
113670	3382	874
113671	3383	733
113672	3383	734
113673	3383	740
113674	3383	742
113675	3383	747
113676	3383	749
113677	3383	753
113678	3383	760
113679	3383	761
113680	3383	764
113681	3383	768
113682	3383	772
113683	3383	777
113684	3383	782
113685	3383	787
113686	3383	789
113687	3383	792
113688	3383	794
113689	3383	809
113690	3383	811
113691	3383	819
113692	3383	821
113693	3383	826
113694	3383	833
113695	3383	835
113696	3383	841
113697	3383	844
113698	3383	848
113699	3383	850
113700	3383	854
113701	3383	856
113702	3383	860
113703	3383	871
113704	3383	872
113705	3383	874
113706	3384	732
113707	3384	734
113708	3384	740
113709	3384	744
113710	3384	746
113711	3384	749
113712	3384	753
113713	3384	760
113714	3384	761
113715	3384	764
113716	3384	768
113717	3384	775
113718	3384	780
113719	3384	782
113720	3384	787
113721	3384	789
113722	3384	792
113723	3384	795
113724	3384	797
113725	3384	803
113726	3384	807
113727	3384	814
113728	3384	819
113729	3384	822
113730	3384	826
113731	3384	833
113732	3384	835
113733	3384	840
113734	3384	845
113735	3384	846
113736	3384	851
113737	3384	852
113738	3384	859
113739	3384	860
113740	3384	871
113741	3384	872
113742	3384	874
113743	3385	733
113744	3385	734
113745	3385	740
113746	3385	742
113747	3385	746
113748	3385	749
113749	3385	753
113750	3385	760
113751	3385	761
113752	3385	764
113753	3385	768
113754	3385	772
113755	3385	777
113756	3385	782
113757	3385	787
113758	3385	789
113759	3385	792
113760	3385	794
113761	3385	806
113762	3385	811
113763	3385	819
113764	3385	822
113765	3385	826
113766	3385	833
113767	3385	835
113768	3385	841
113769	3385	845
113770	3385	847
113771	3385	851
113772	3385	853
113773	3385	858
113774	3385	860
113775	3385	871
113776	3385	872
113777	3385	874
113778	3386	733
113779	3386	734
113780	3386	740
113781	3386	743
113782	3386	746
113783	3386	749
113784	3386	754
113785	3386	760
113786	3386	761
113787	3386	764
113788	3386	768
113789	3386	775
113790	3386	781
113791	3386	782
113792	3386	787
113793	3386	789
113794	3386	793
113795	3386	794
113796	3386	806
113797	3386	815
113798	3386	819
113799	3386	822
113800	3386	826
113801	3386	832
113802	3386	835
113803	3386	841
113804	3386	845
113805	3386	846
113806	3386	851
113807	3386	852
113808	3386	859
113809	3386	860
113810	3386	871
113811	3386	874
113812	3387	732
113813	3387	734
113814	3387	740
113815	3387	744
113816	3387	747
113817	3387	749
113818	3387	753
113819	3387	760
113820	3387	761
113821	3387	767
113822	3387	771
113823	3387	775
113824	3387	777
113825	3387	784
113826	3387	787
113827	3387	789
113828	3387	793
113829	3387	795
113830	3387	800
113831	3387	805
113832	3387	808
113833	3387	814
113834	3387	819
113835	3387	823
113836	3387	828
113837	3387	832
113838	3387	836
113839	3387	841
113840	3387	845
113841	3387	848
113842	3387	851
113843	3387	854
113844	3387	857
113845	3387	860
113846	3387	871
113847	3387	873
113848	3387	874
113849	3388	732
113850	3388	734
113851	3388	740
113852	3388	744
113853	3388	745
113854	3388	749
113855	3388	754
113856	3388	758
113857	3388	761
113858	3388	764
113859	3388	768
113860	3388	772
113861	3388	777
113862	3388	783
113863	3388	787
113864	3388	789
113865	3388	792
113866	3388	795
113867	3388	798
113868	3388	802
113869	3388	806
113870	3388	811
113871	3388	819
113872	3388	823
113873	3388	827
113874	3388	831
113875	3388	834
113876	3388	841
113877	3388	845
113878	3388	846
113879	3388	851
113880	3388	852
113881	3388	859
113882	3388	860
113883	3388	871
113884	3388	872
113885	3388	874
113886	3389	732
113887	3389	734
113888	3389	740
113889	3389	744
113890	3389	746
113891	3389	749
113892	3389	753
113893	3389	760
113894	3389	761
113895	3389	764
113896	3389	768
113897	3389	772
113898	3389	777
113899	3389	784
113900	3389	787
113901	3389	789
113902	3389	792
113903	3389	794
113904	3389	808
113905	3389	811
113906	3389	818
113907	3389	822
113908	3389	827
113909	3389	832
113910	3389	835
113911	3389	841
113912	3389	844
113913	3389	847
113914	3389	850
113915	3389	853
113916	3389	857
113917	3389	860
113918	3389	871
113919	3389	874
113920	3390	732
113921	3390	734
113922	3390	740
113923	3390	744
113924	3390	746
113925	3390	750
113926	3390	754
113927	3390	757
113928	3390	761
113929	3390	764
113930	3390	768
113931	3390	772
113932	3390	777
113933	3390	785
113934	3390	787
113935	3390	789
113936	3390	792
113937	3390	794
113938	3390	808
113939	3390	811
113940	3390	819
113941	3390	823
113942	3390	828
113943	3390	831
113944	3390	835
113945	3390	841
113946	3390	845
113947	3390	847
113948	3390	851
113949	3390	853
113950	3390	858
113951	3390	860
113952	3390	871
113953	3390	872
113954	3390	874
113955	3391	732
113956	3391	734
113957	3391	740
113958	3391	744
113959	3391	747
113960	3391	750
113961	3391	755
113962	3391	760
113963	3391	761
113964	3391	764
113965	3391	768
113966	3391	772
113967	3391	777
113968	3391	786
113969	3391	787
113970	3391	789
113971	3391	793
113972	3391	794
113973	3391	808
113974	3391	811
113975	3391	819
113976	3391	823
113977	3391	828
113978	3391	833
113979	3391	835
113980	3391	840
113981	3391	844
113982	3391	847
113983	3391	850
113984	3391	853
113985	3391	857
113986	3391	860
113987	3391	871
113988	3391	874
113989	3392	733
113990	3392	734
113991	3392	740
113992	3392	743
113993	3392	747
113994	3392	749
113995	3392	753
113996	3392	758
113997	3392	761
113998	3392	764
113999	3392	768
114000	3392	775
114001	3392	777
114002	3392	783
114003	3392	787
114004	3392	789
114005	3392	792
114006	3392	794
114007	3392	807
114008	3392	816
114009	3392	819
114010	3392	822
114011	3392	828
114012	3392	831
114013	3392	835
114014	3392	840
114015	3392	845
114016	3392	846
114017	3392	851
114018	3392	852
114019	3392	859
114020	3392	860
114021	3392	871
114022	3392	873
114023	3392	874
114024	3393	732
114025	3393	734
114026	3393	740
114027	3393	742
114028	3393	745
114029	3393	748
114030	3393	752
114031	3393	759
114032	3393	761
114033	3393	764
114034	3393	768
114035	3393	772
114036	3393	777
114037	3393	782
114038	3393	787
114039	3393	789
114040	3393	792
114041	3393	794
114042	3393	806
114043	3393	811
114044	3393	818
114045	3393	823
114046	3393	826
114047	3393	832
114048	3393	835
114049	3393	841
114050	3393	845
114051	3393	846
114052	3393	851
114053	3393	852
114054	3393	858
114055	3393	860
114056	3393	871
114057	3393	873
114058	3393	874
114059	3394	732
114060	3394	734
114061	3394	740
114062	3394	744
114063	3394	747
114064	3394	749
114065	3394	757
114066	3394	761
114067	3394	766
114068	3394	770
114069	3394	775
114070	3394	777
114071	3394	784
114072	3394	787
114073	3394	789
114074	3394	793
114075	3394	808
114076	3394	814
114077	3394	828
114078	3394	832
114079	3394	836
114080	3394	842
114081	3394	845
114082	3394	848
114083	3394	851
114084	3394	854
114085	3394	857
114086	3394	860
114087	3394	871
114088	3394	872
114089	3394	874
114090	3395	732
114091	3395	734
114092	3395	740
114093	3395	743
114094	3395	745
114095	3395	748
114096	3395	753
114097	3395	760
114098	3395	761
114099	3395	764
114100	3395	768
114101	3395	774
114102	3395	777
114103	3395	783
114104	3395	787
114105	3395	789
114106	3395	793
114107	3395	794
114108	3395	806
114109	3395	815
114110	3395	819
114111	3395	822
114112	3395	827
114113	3395	833
114114	3395	834
114115	3395	840
114116	3395	845
114117	3395	846
114118	3395	851
114119	3395	852
114120	3395	859
114121	3395	860
114122	3395	871
114123	3395	873
114124	3395	874
114125	3396	732
114126	3396	734
114127	3396	740
114128	3396	744
114129	3396	746
114130	3396	749
114131	3396	754
114132	3396	758
114133	3396	761
114134	3396	764
114135	3396	768
114136	3396	772
114137	3396	777
114138	3396	783
114139	3396	787
114140	3396	789
114141	3396	792
114142	3396	795
114143	3396	797
114144	3396	801
114145	3396	806
114146	3396	811
114147	3396	819
114148	3396	822
114149	3396	825
114150	3396	831
114151	3396	835
114152	3396	842
114153	3396	845
114154	3396	847
114155	3396	851
114156	3396	853
114157	3396	858
114158	3396	860
114159	3396	871
114160	3396	872
114161	3396	874
114162	3397	732
114163	3397	734
114164	3397	740
114165	3397	743
114166	3397	746
114167	3397	749
114168	3397	753
114169	3397	757
114170	3397	761
114171	3397	764
114172	3397	768
114173	3397	772
114174	3397	777
114175	3397	783
114176	3397	787
114177	3397	789
114178	3397	792
114179	3397	794
114180	3397	808
114181	3397	811
114182	3397	818
114183	3397	822
114184	3397	828
114185	3397	830
114186	3397	835
114187	3397	840
114188	3397	844
114189	3397	847
114190	3397	850
114191	3397	853
114192	3397	857
114193	3397	860
114194	3397	871
114195	3397	872
114196	3397	874
114197	3398	732
114198	3398	734
114199	3398	740
114200	3398	744
114201	3398	747
114202	3398	749
114203	3398	754
114204	3398	758
114205	3398	761
114206	3398	764
114207	3398	768
114208	3398	775
114209	3398	781
114210	3398	783
114211	3398	787
114212	3398	789
114213	3398	792
114214	3398	794
114215	3398	808
114216	3398	815
114217	3398	819
114218	3398	822
114219	3398	825
114220	3398	831
114221	3398	835
114222	3398	841
114223	3398	845
114224	3398	847
114225	3398	851
114226	3398	853
114227	3398	857
114228	3398	860
114229	3398	871
114230	3398	872
114231	3398	874
114232	3399	732
114233	3399	734
114234	3399	736
114235	3399	740
114236	3399	744
114237	3399	746
114238	3399	750
114239	3399	754
114240	3399	758
114241	3399	761
114242	3399	764
114243	3399	768
114244	3399	774
114245	3399	777
114246	3399	783
114247	3399	787
114248	3399	789
114249	3399	792
114250	3399	794
114251	3399	808
114252	3399	814
114253	3399	819
114254	3399	822
114255	3399	825
114256	3399	831
114257	3399	835
114258	3399	841
114259	3399	844
114260	3399	848
114261	3399	850
114262	3399	854
114263	3399	856
114264	3399	860
114265	3399	871
114266	3399	872
114267	3399	874
114268	3400	732
114269	3400	734
114270	3400	740
114271	3400	742
114272	3400	745
114273	3400	750
114274	3400	754
114275	3400	757
114276	3400	761
114277	3400	764
114278	3400	768
114279	3400	772
114280	3400	777
114281	3400	783
114282	3400	787
114283	3400	789
114284	3400	791
114285	3400	794
114286	3400	807
114287	3400	811
114288	3400	818
114289	3400	821
114290	3400	827
114291	3400	830
114292	3400	835
114293	3400	841
114294	3400	845
114295	3400	847
114296	3400	851
114297	3400	853
114298	3400	857
114299	3400	860
114300	3400	871
114301	3400	872
114302	3400	874
114303	3401	732
114304	3401	734
114305	3401	740
114306	3401	744
114307	3401	747
114308	3401	749
114309	3401	753
114310	3401	759
114311	3401	761
114312	3401	764
114313	3401	768
114314	3401	772
114315	3401	777
114316	3401	785
114317	3401	787
114318	3401	789
114319	3401	793
114320	3401	794
114321	3401	808
114322	3401	811
114323	3401	819
114324	3401	823
114325	3401	828
114326	3401	831
114327	3401	835
114328	3401	841
114329	3401	843
114330	3401	847
114331	3401	849
114332	3401	854
114333	3401	856
114334	3401	860
114335	3401	871
114336	3401	874
114337	3402	731
114338	3402	734
114339	3402	740
114340	3402	742
114341	3402	747
114342	3402	749
114343	3402	753
114344	3402	758
114345	3402	761
114346	3402	764
114347	3402	768
114348	3402	772
114349	3402	777
114350	3402	783
114351	3402	787
114352	3402	789
114353	3402	792
114354	3402	794
114355	3402	806
114356	3402	811
114357	3402	819
114358	3402	822
114359	3402	826
114360	3402	830
114361	3402	835
114362	3402	841
114363	3402	845
114364	3402	847
114365	3402	851
114366	3402	853
114367	3402	858
114368	3402	860
114369	3402	871
114370	3402	872
114371	3402	874
114372	3403	731
114373	3403	734
114374	3403	740
114375	3403	743
114376	3403	747
114377	3403	749
114378	3403	753
114379	3403	759
114380	3403	761
114381	3403	764
114382	3403	768
114383	3403	772
114384	3403	777
114385	3403	784
114386	3403	787
114387	3403	789
114388	3403	791
114389	3403	794
114390	3403	809
114391	3403	811
114392	3403	818
114393	3403	821
114394	3403	827
114395	3403	832
114396	3403	834
114397	3403	841
114398	3403	845
114399	3403	847
114400	3403	851
114401	3403	853
114402	3403	857
114403	3403	860
114404	3403	871
114405	3403	872
114406	3403	874
114407	3404	732
114408	3404	734
114409	3404	740
114410	3404	744
114411	3404	747
114412	3404	749
114413	3404	754
114414	3404	756
114415	3404	761
114416	3404	764
114417	3404	768
114418	3404	774
114419	3404	777
114420	3404	783
114421	3404	787
114422	3404	789
114423	3404	792
114424	3404	794
114425	3404	808
114426	3404	814
114427	3404	819
114428	3404	823
114429	3404	828
114430	3404	830
114431	3404	835
114432	3404	841
114433	3404	843
114434	3404	848
114435	3404	850
114436	3404	854
114437	3404	856
114438	3404	860
114439	3404	871
114440	3404	872
114441	3404	874
114442	3405	733
114443	3405	734
114444	3405	740
114445	3405	743
114446	3405	746
114447	3405	749
114448	3405	754
114449	3405	760
114450	3405	761
114451	3405	764
114452	3405	768
114453	3405	772
114454	3405	777
114455	3405	783
114456	3405	787
114457	3405	789
114458	3405	792
114459	3405	794
114460	3405	808
114461	3405	811
114462	3405	818
114463	3405	821
114464	3405	827
114465	3405	833
114466	3405	835
114467	3405	841
114468	3405	844
114469	3405	847
114470	3405	850
114471	3405	853
114472	3405	857
114473	3405	860
114474	3405	871
114475	3405	874
114476	3406	731
114477	3406	734
114478	3406	740
114479	3406	744
114480	3406	747
114481	3406	749
114482	3406	754
114483	3406	759
114484	3406	761
114485	3406	764
114486	3406	768
114487	3406	772
114488	3406	777
114489	3406	784
114490	3406	787
114491	3406	789
114492	3406	792
114493	3406	794
114494	3406	808
114495	3406	811
114496	3406	819
114497	3406	823
114498	3406	828
114499	3406	832
114500	3406	835
114501	3406	841
114502	3406	845
114503	3406	847
114504	3406	851
114505	3406	853
114506	3406	858
114507	3406	860
114508	3406	871
114509	3406	874
114510	3407	731
114511	3407	734
114512	3407	740
114513	3407	743
114514	3407	746
114515	3407	749
114516	3407	754
114517	3407	760
114518	3407	761
114519	3407	764
114520	3407	768
114521	3407	775
114522	3407	777
114523	3407	783
114524	3407	787
114525	3407	789
114526	3407	792
114527	3407	794
114528	3407	806
114529	3407	815
114530	3407	819
114531	3407	822
114532	3407	826
114533	3407	833
114534	3407	835
114535	3407	841
114536	3407	845
114537	3407	846
114538	3407	851
114539	3407	852
114540	3407	859
114541	3407	860
114542	3407	871
114543	3407	872
114544	3407	874
114545	3408	732
114546	3408	734
114547	3408	740
114548	3408	744
114549	3408	746
114550	3408	749
114551	3408	753
114552	3408	757
114553	3408	761
114554	3408	764
114555	3408	768
114556	3408	772
114557	3408	777
114558	3408	784
114559	3408	787
114560	3408	789
114561	3408	792
114562	3408	794
114563	3408	808
114564	3408	811
114565	3408	819
114566	3408	822
114567	3408	828
114568	3408	831
114569	3408	835
114570	3408	841
114571	3408	844
114572	3408	848
114573	3408	850
114574	3408	854
114575	3408	856
114576	3408	860
114577	3408	871
114578	3408	872
114579	3408	874
114580	3409	732
114581	3409	734
114582	3409	740
114583	3409	744
114584	3409	746
114585	3409	749
114586	3409	753
114587	3409	761
114588	3409	764
114589	3409	768
114590	3409	775
114591	3409	781
114592	3409	783
114593	3409	787
114594	3409	789
114595	3409	792
114596	3409	794
114597	3409	806
114598	3409	816
114599	3409	819
114600	3409	822
114601	3409	826
114602	3409	835
114603	3409	841
114604	3409	845
114605	3409	846
114606	3409	851
114607	3409	852
114608	3409	859
114609	3409	860
114610	3409	871
114611	3409	873
114612	3409	874
114613	3410	732
114614	3410	734
114615	3410	740
114616	3410	743
114617	3410	746
114618	3410	749
114619	3410	753
114620	3410	760
114621	3410	761
114622	3410	764
114623	3410	768
114624	3410	772
114625	3410	777
114626	3410	783
114627	3410	787
114628	3410	789
114629	3410	792
114630	3410	794
114631	3410	806
114632	3410	811
114633	3410	819
114634	3410	823
114635	3410	828
114636	3410	833
114637	3410	835
114638	3410	841
114639	3410	845
114640	3410	847
114641	3410	851
114642	3410	853
114643	3410	858
114644	3410	860
114645	3410	871
114646	3410	872
114647	3410	874
114648	3411	733
114649	3411	734
114650	3411	740
114651	3411	742
114652	3411	747
114653	3411	749
114654	3411	753
114655	3411	758
114656	3411	761
114657	3411	764
114658	3411	768
114659	3411	772
114660	3411	777
114661	3411	784
114662	3411	787
114663	3411	789
114664	3411	792
114665	3411	794
114666	3411	809
114667	3411	811
114668	3411	818
114669	3411	822
114670	3411	827
114671	3411	831
114672	3411	835
114673	3411	841
114674	3411	843
114675	3411	847
114676	3411	849
114677	3411	853
114678	3411	856
114679	3411	860
114680	3411	871
114681	3411	872
114682	3411	874
114683	3412	732
114684	3412	734
114685	3412	740
114686	3412	744
114687	3412	746
114688	3412	749
114689	3412	753
114690	3412	760
114691	3412	761
114692	3412	764
114693	3412	768
114694	3412	772
114695	3412	777
114696	3412	783
114697	3412	787
114698	3412	789
114699	3412	793
114700	3412	794
114701	3412	806
114702	3412	811
114703	3412	819
114704	3412	823
114705	3412	828
114706	3412	833
114707	3412	835
114708	3412	842
114709	3412	845
114710	3412	847
114711	3412	851
114712	3412	854
114713	3412	857
114714	3412	860
114715	3412	871
114716	3412	872
114717	3412	874
114718	3413	732
114719	3413	734
114720	3413	740
114721	3413	743
114722	3413	745
114723	3413	750
114724	3413	754
114725	3413	757
114726	3413	761
114727	3413	764
114728	3413	768
114729	3413	772
114730	3413	777
114731	3413	783
114732	3413	787
114733	3413	789
114734	3413	792
114735	3413	794
114736	3413	806
114737	3413	811
114738	3413	819
114739	3413	822
114740	3413	826
114741	3413	831
114742	3413	835
114743	3413	841
114744	3413	845
114745	3413	846
114746	3413	851
114747	3413	852
114748	3413	859
114749	3413	860
114750	3413	871
114751	3413	873
114752	3413	874
114753	3414	732
114754	3414	734
114755	3414	740
114756	3414	744
114757	3414	746
114758	3414	749
114759	3414	753
114760	3414	760
114761	3414	761
114762	3414	764
114763	3414	768
114764	3414	774
114765	3414	781
114766	3414	783
114767	3414	787
114768	3414	789
114769	3414	792
114770	3414	794
114771	3414	806
114772	3414	814
114773	3414	819
114774	3414	823
114775	3414	826
114776	3414	833
114777	3414	835
114778	3414	841
114779	3414	845
114780	3414	846
114781	3414	851
114782	3414	852
114783	3414	859
114784	3414	860
114785	3414	871
114786	3414	873
114787	3414	874
114788	3415	732
114789	3415	734
114790	3415	740
114791	3415	744
114792	3415	746
114793	3415	749
114794	3415	753
114795	3415	760
114796	3415	761
114797	3415	764
114798	3415	768
114799	3415	775
114800	3415	777
114801	3415	784
114802	3415	787
114803	3415	789
114804	3415	792
114805	3415	794
114806	3415	808
114807	3415	814
114808	3415	819
114809	3415	822
114810	3415	827
114811	3415	833
114812	3415	836
114813	3415	841
114814	3415	845
114815	3415	847
114816	3415	851
114817	3415	853
114818	3415	858
114819	3415	860
114820	3415	871
114821	3415	874
114822	3416	731
114823	3416	734
114824	3416	740
114825	3416	743
114826	3416	745
114827	3416	749
114828	3416	754
114829	3416	760
114830	3416	761
114831	3416	764
114832	3416	768
114833	3416	772
114834	3416	777
114835	3416	782
114836	3416	787
114837	3416	789
114838	3416	792
114839	3416	794
114840	3416	808
114841	3416	811
114842	3416	819
114843	3416	822
114844	3416	826
114845	3416	832
114846	3416	835
114847	3416	841
114848	3416	845
114849	3416	846
114850	3416	851
114851	3416	852
114852	3416	859
114853	3416	860
114854	3416	871
114855	3416	874
114856	3417	733
114857	3417	734
114858	3417	740
114859	3417	744
114860	3417	746
114861	3417	749
114862	3417	753
114863	3417	760
114864	3417	761
114865	3417	764
114866	3417	768
114867	3417	774
114868	3417	777
114869	3417	783
114870	3417	787
114871	3417	789
114872	3417	792
114873	3417	795
114874	3417	796
114875	3417	801
114876	3417	808
114877	3417	814
114878	3417	819
114879	3417	822
114880	3417	827
114881	3417	833
114882	3417	836
114883	3417	841
114884	3417	845
114885	3417	847
114886	3417	851
114887	3417	853
114888	3417	858
114889	3417	860
114890	3417	871
114891	3417	874
114892	3418	732
114893	3418	734
114894	3418	740
114895	3418	744
114896	3418	747
114897	3418	749
114898	3418	754
114899	3418	758
114900	3418	761
114901	3418	764
114902	3418	768
114903	3418	772
114904	3418	777
114905	3418	785
114906	3418	787
114907	3418	789
114908	3418	793
114909	3418	794
114910	3418	809
114911	3418	811
114912	3418	819
114913	3418	822
114914	3418	828
114915	3418	831
114916	3418	835
114917	3418	842
114918	3418	845
114919	3418	847
114920	3418	851
114921	3418	854
114922	3418	857
114923	3418	860
114924	3418	871
114925	3418	874
114926	3419	733
114927	3419	734
114928	3419	736
114929	3419	740
114930	3419	743
114931	3419	746
114932	3419	750
114933	3419	755
114934	3419	758
114935	3419	761
114936	3419	764
114937	3419	768
114938	3419	772
114939	3419	777
114940	3419	784
114941	3419	787
114942	3419	789
114943	3419	791
114944	3419	794
114945	3419	808
114946	3419	811
114947	3419	818
114948	3419	822
114949	3419	826
114950	3419	830
114951	3419	835
114952	3419	841
114953	3419	844
114954	3419	847
114955	3419	851
114956	3419	853
114957	3419	858
114958	3419	860
114959	3419	871
114960	3419	872
114961	3419	874
114962	3420	732
114963	3420	734
114964	3420	740
114965	3420	744
114966	3420	747
114967	3420	749
114968	3420	754
114969	3420	758
114970	3420	761
114971	3420	765
114972	3420	769
114973	3420	774
114974	3420	777
114975	3420	785
114976	3420	788
114977	3420	789
114978	3420	793
114979	3420	794
114980	3420	809
114981	3420	814
114982	3420	819
114983	3420	823
114984	3420	828
114985	3420	831
114986	3420	837
114987	3420	841
114988	3420	844
114989	3420	848
114990	3420	850
114991	3420	854
114992	3420	856
114993	3420	860
114994	3420	871
114995	3420	874
114996	3421	732
114997	3421	734
114998	3421	740
114999	3421	743
115000	3421	747
115001	3421	749
115002	3421	754
115003	3421	760
115004	3421	761
115005	3421	764
115006	3421	768
115007	3421	772
115008	3421	777
115009	3421	783
115010	3421	787
115011	3421	789
115012	3421	791
115013	3421	794
115014	3421	808
115015	3421	811
115016	3421	818
115017	3421	821
115018	3421	827
115019	3421	833
115020	3421	835
115021	3421	842
115022	3421	844
115023	3421	848
115024	3421	850
115025	3421	854
115026	3421	856
115027	3421	860
115028	3421	871
115029	3421	872
115030	3421	874
115031	3422	731
115032	3422	734
115033	3422	740
115034	3422	743
115035	3422	746
115036	3422	749
115037	3422	754
115038	3422	757
115039	3422	761
115040	3422	764
115041	3422	768
115042	3422	775
115043	3422	781
115044	3422	784
115045	3422	787
115046	3422	789
115047	3422	792
115048	3422	794
115049	3422	806
115050	3422	816
115051	3422	818
115052	3422	822
115053	3422	826
115054	3422	830
115055	3422	835
115056	3422	841
115057	3422	844
115058	3422	847
115059	3422	850
115060	3422	853
115061	3422	857
115062	3422	860
115063	3422	871
115064	3422	872
115065	3422	874
115066	3423	732
115067	3423	734
115068	3423	740
115069	3423	743
115070	3423	746
115071	3423	749
115072	3423	753
115073	3423	760
115074	3423	761
115075	3423	764
115076	3423	768
115077	3423	772
115078	3423	777
115079	3423	784
115080	3423	787
115081	3423	789
115082	3423	792
115083	3423	794
115084	3423	808
115085	3423	811
115086	3423	818
115087	3423	821
115088	3423	827
115089	3423	831
115090	3423	835
115091	3423	841
115092	3423	844
115093	3423	847
115094	3423	850
115095	3423	853
115096	3423	857
115097	3423	860
115098	3423	871
115099	3423	872
115100	3423	874
115101	3424	732
115102	3424	734
115103	3424	740
115104	3424	743
115105	3424	746
115106	3424	749
115107	3424	754
115108	3424	757
115109	3424	761
115110	3424	764
115111	3424	768
115112	3424	772
115113	3424	777
115114	3424	783
115115	3424	787
115116	3424	789
115117	3424	792
115118	3424	794
115119	3424	808
115120	3424	811
115121	3424	819
115122	3424	823
115123	3424	826
115124	3424	829
115125	3424	838
115126	3424	841
115127	3424	845
115128	3424	847
115129	3424	850
115130	3424	853
115131	3424	857
115132	3424	868
115133	3424	871
115134	3424	872
115135	3424	876
115136	3425	733
115137	3425	734
115138	3425	740
115139	3425	744
115140	3425	745
115141	3425	749
115142	3425	753
115143	3425	760
115144	3425	761
115145	3425	764
115146	3425	768
115147	3425	775
115148	3425	781
115149	3425	783
115150	3425	787
115151	3425	789
115152	3425	793
115153	3425	794
115154	3425	806
115155	3425	815
115156	3425	819
115157	3425	822
115158	3425	826
115159	3425	833
115160	3425	835
115161	3425	841
115162	3425	845
115163	3425	846
115164	3425	851
115165	3425	852
115166	3425	859
115167	3425	860
115168	3425	871
115169	3425	874
115170	3426	733
115171	3426	734
115172	3426	740
115173	3426	744
115174	3426	746
115175	3426	749
115176	3426	753
115177	3426	760
115178	3426	761
115179	3426	764
115180	3426	768
115181	3426	772
115182	3426	777
115183	3426	784
115184	3426	787
115185	3426	789
115186	3426	792
115187	3426	794
115188	3426	808
115189	3426	811
115190	3426	819
115191	3426	822
115192	3426	828
115193	3426	833
115194	3426	835
115195	3426	841
115196	3426	844
115197	3426	847
115198	3426	850
115199	3426	854
115200	3426	856
115201	3426	860
115202	3426	871
115203	3426	872
115204	3426	874
115205	3427	732
115206	3427	734
115207	3427	740
115208	3427	744
115209	3427	746
115210	3427	749
115211	3427	755
115212	3427	757
115213	3427	761
115214	3427	764
115215	3427	768
115216	3427	772
115217	3427	777
115218	3427	785
115219	3427	787
115220	3427	789
115221	3427	793
115222	3427	795
115223	3427	800
115224	3427	805
115225	3427	808
115226	3427	811
115227	3427	819
115228	3427	823
115229	3427	828
115230	3427	831
115231	3427	835
115232	3427	841
115233	3427	844
115234	3427	847
115235	3427	850
115236	3427	854
115237	3427	856
115238	3427	860
115239	3427	871
115240	3427	874
115241	3428	732
115242	3428	734
115243	3428	740
115244	3428	742
115245	3428	747
115246	3428	749
115247	3428	754
115248	3428	757
115249	3428	761
115250	3428	764
115251	3428	768
115252	3428	772
115253	3428	777
115254	3428	783
115255	3428	787
115256	3428	789
115257	3428	792
115258	3428	795
115259	3428	797
115260	3428	802
115261	3428	808
115262	3428	811
115263	3428	818
115264	3428	821
115265	3428	827
115266	3428	831
115267	3428	835
115268	3428	842
115269	3428	844
115270	3428	848
115271	3428	850
115272	3428	854
115273	3428	856
115274	3428	860
115275	3428	871
115276	3428	873
115277	3428	874
115278	3429	733
115279	3429	734
115280	3429	740
115281	3429	743
115282	3429	745
115283	3429	748
115284	3429	753
115285	3429	760
115286	3429	761
115287	3429	764
115288	3429	768
115289	3429	772
115290	3429	777
115291	3429	784
115292	3429	787
115293	3429	789
115294	3429	792
115295	3429	795
115296	3429	798
115297	3429	803
115298	3429	808
115299	3429	811
115300	3429	819
115301	3429	823
115302	3429	828
115303	3429	833
115304	3429	834
115305	3429	841
115306	3429	843
115307	3429	847
115308	3429	849
115309	3429	853
115310	3429	856
115311	3429	860
115312	3429	871
115313	3429	872
115314	3429	874
115315	3430	732
115316	3430	734
115317	3430	740
115318	3430	743
115319	3430	746
115320	3430	748
115321	3430	752
115322	3430	760
115323	3430	761
115324	3430	764
115325	3430	768
115326	3430	772
115327	3430	777
115328	3430	782
115329	3430	787
115330	3430	789
115331	3430	792
115332	3430	794
115333	3430	806
115334	3430	811
115335	3430	819
115336	3430	823
115337	3430	826
115338	3430	832
115339	3430	834
115340	3430	840
115341	3430	845
115342	3430	846
115343	3430	851
115344	3430	852
115345	3430	859
115346	3430	860
115347	3430	871
115348	3430	874
115349	3431	732
115350	3431	734
115351	3431	740
115352	3431	743
115353	3431	746
115354	3431	749
115355	3431	753
115356	3431	757
115357	3431	761
115358	3431	764
115359	3431	768
115360	3431	772
115361	3431	777
115362	3431	783
115363	3431	787
115364	3431	789
115365	3431	791
115366	3431	794
115367	3431	809
115368	3431	811
115369	3431	818
115370	3431	821
115371	3431	826
115372	3431	835
115373	3431	842
115374	3431	845
115375	3431	847
115376	3431	851
115377	3431	854
115378	3431	857
115379	3431	860
115380	3431	871
115381	3431	872
115382	3431	874
115383	3432	731
115384	3432	734
115385	3432	740
115386	3432	743
115387	3432	746
115388	3432	749
115389	3432	753
115390	3432	758
115391	3432	761
115392	3432	764
115393	3432	768
115394	3432	772
115395	3432	777
115396	3432	784
115397	3432	787
115398	3432	789
115399	3432	792
115400	3432	794
115401	3432	808
115402	3432	811
115403	3432	818
115404	3432	821
115405	3432	827
115406	3432	831
115407	3432	835
115408	3432	841
115409	3432	845
115410	3432	847
115411	3432	851
115412	3432	853
115413	3432	857
115414	3432	860
115415	3432	871
115416	3432	872
115417	3432	874
115418	3433	732
115419	3433	734
115420	3433	740
115421	3433	744
115422	3433	746
115423	3433	748
115424	3433	753
115425	3433	760
115426	3433	761
115427	3433	764
115428	3433	768
115429	3433	772
115430	3433	777
115431	3433	783
115432	3433	787
115433	3433	789
115434	3433	793
115435	3433	794
115436	3433	806
115437	3433	811
115438	3433	819
115439	3433	823
115440	3433	828
115441	3433	833
115442	3433	835
115443	3433	842
115444	3433	845
115445	3433	848
115446	3433	851
115447	3433	854
115448	3433	856
115449	3433	860
115450	3433	871
115451	3433	872
115452	3433	874
115453	3434	732
115454	3434	734
115455	3434	740
115456	3434	743
115457	3434	745
115458	3434	749
115459	3434	754
115460	3434	758
115461	3434	761
115462	3434	764
115463	3434	768
115464	3434	772
115465	3434	777
115466	3434	786
115467	3434	787
115468	3434	789
115469	3434	792
115470	3434	794
115471	3434	803
115472	3434	808
115473	3434	811
115474	3434	819
115475	3434	823
115476	3434	828
115477	3434	833
115478	3434	835
115479	3434	841
115480	3434	843
115481	3434	848
115482	3434	849
115483	3434	854
115484	3434	856
115485	3434	860
115486	3434	871
115487	3434	874
115488	3435	733
115489	3435	734
115490	3435	740
115491	3435	743
115492	3435	747
115493	3435	748
115494	3435	753
115495	3435	758
115496	3435	761
115497	3435	764
115498	3435	768
115499	3435	772
115500	3435	777
115501	3435	784
115502	3435	787
115503	3435	789
115504	3435	792
115505	3435	794
115506	3435	808
115507	3435	811
115508	3435	818
115509	3435	822
115510	3435	827
115511	3435	835
115512	3435	841
115513	3435	844
115514	3435	848
115515	3435	850
115516	3435	854
115517	3435	856
115518	3435	860
115519	3435	871
115520	3435	872
115521	3435	874
115522	3436	732
115523	3436	734
115524	3436	737
115525	3436	741
115526	3436	744
115527	3436	747
115528	3436	749
115529	3436	753
115530	3436	757
115531	3436	761
115532	3436	764
115533	3436	768
115534	3436	772
115535	3436	777
115536	3436	786
115537	3436	788
115538	3436	789
115539	3436	793
115540	3436	795
115541	3436	800
115542	3436	805
115543	3436	808
115544	3436	811
115545	3436	819
115546	3436	823
115547	3436	828
115548	3436	831
115549	3436	835
115550	3436	841
115551	3436	844
115552	3436	847
115553	3436	850
115554	3436	854
115555	3436	856
115556	3436	860
115557	3436	871
115558	3436	874
115559	3437	732
115560	3437	734
115561	3437	740
115562	3437	743
115563	3437	745
115564	3437	751
115565	3437	755
115566	3437	758
115567	3437	761
115568	3437	764
115569	3437	768
115570	3437	772
115571	3437	777
115572	3437	784
115573	3437	787
115574	3437	789
115575	3437	793
115576	3437	794
115577	3437	808
115578	3437	811
115579	3437	819
115580	3437	823
115581	3437	828
115582	3437	831
115583	3437	835
115584	3437	840
115585	3437	845
115586	3437	846
115587	3437	851
115588	3437	852
115589	3437	859
115590	3437	860
115591	3437	871
115592	3437	872
115593	3437	874
115594	3438	732
115595	3438	734
115596	3438	740
115597	3438	742
115598	3438	746
115599	3438	750
115600	3438	754
115601	3438	758
115602	3438	761
115603	3438	764
115604	3438	768
115605	3438	772
115606	3438	777
115607	3438	784
115608	3438	787
115609	3438	789
115610	3438	791
115611	3438	794
115612	3438	809
115613	3438	811
115614	3438	818
115615	3438	822
115616	3438	827
115617	3438	830
115618	3438	835
115619	3438	841
115620	3438	845
115621	3438	846
115622	3438	851
115623	3438	852
115624	3438	859
115625	3438	860
115626	3438	871
115627	3438	873
115628	3438	874
115629	3439	732
115630	3439	734
115631	3439	740
115632	3439	742
115633	3439	745
115634	3439	749
115635	3439	753
115636	3439	758
115637	3439	761
115638	3439	764
115639	3439	768
115640	3439	772
115641	3439	777
115642	3439	783
115643	3439	787
115644	3439	789
115645	3439	792
115646	3439	794
115647	3439	808
115648	3439	811
115649	3439	819
115650	3439	823
115651	3439	828
115652	3439	831
115653	3439	835
115654	3439	841
115655	3439	843
115656	3439	847
115657	3439	849
115658	3439	853
115659	3439	856
115660	3439	860
115661	3439	871
115662	3439	872
115663	3439	874
115664	3440	732
115665	3440	734
115666	3440	740
115667	3440	743
115668	3440	747
115669	3440	749
115670	3440	753
115671	3440	757
115672	3440	761
115673	3440	764
115674	3440	768
115675	3440	772
115676	3440	777
115677	3440	784
115678	3440	787
115679	3440	789
115680	3440	793
115681	3440	794
115682	3440	808
115683	3440	811
115684	3440	819
115685	3440	823
115686	3440	828
115687	3440	831
115688	3440	835
115689	3440	840
115690	3440	843
115691	3440	847
115692	3440	849
115693	3440	853
115694	3440	856
115695	3440	865
115696	3440	871
115697	3440	874
115698	3441	732
115699	3441	734
115700	3441	740
115701	3441	744
115702	3441	745
115703	3441	750
115704	3441	755
115705	3441	758
115706	3441	761
115707	3441	764
115708	3441	768
115709	3441	774
115710	3441	777
115711	3441	783
115712	3441	787
115713	3441	789
115714	3441	792
115715	3441	794
115716	3441	806
115717	3441	816
115718	3441	819
115719	3441	822
115720	3441	827
115721	3441	830
115722	3441	835
115723	3441	840
115724	3441	845
115725	3441	846
115726	3441	851
115727	3441	852
115728	3441	859
115729	3441	860
115730	3441	871
115731	3441	873
115732	3441	874
115733	3442	733
115734	3442	734
115735	3442	740
115736	3442	743
115737	3442	747
115738	3442	749
115739	3442	753
115740	3442	758
115741	3442	761
115742	3442	764
115743	3442	769
115744	3442	775
115745	3442	777
115746	3442	784
115747	3442	787
115748	3442	789
115749	3442	792
115750	3442	794
115751	3442	809
115752	3442	814
115753	3442	818
115754	3442	821
115755	3442	826
115756	3442	832
115757	3442	836
115758	3442	842
115759	3442	844
115760	3442	848
115761	3442	850
115762	3442	854
115763	3442	856
115764	3442	860
115765	3442	871
115766	3442	872
115767	3442	874
115768	3443	732
115769	3443	734
115770	3443	740
115771	3443	744
115772	3443	746
115773	3443	748
115774	3443	753
115775	3443	757
115776	3443	761
115777	3443	764
115778	3443	768
115779	3443	772
115780	3443	777
115781	3443	784
115782	3443	787
115783	3443	789
115784	3443	792
115785	3443	794
115786	3443	807
115787	3443	811
115788	3443	819
115789	3443	823
115790	3443	827
115791	3443	830
115792	3443	835
115793	3443	841
115794	3443	843
115795	3443	847
115796	3443	849
115797	3443	853
115798	3443	856
115799	3443	860
115800	3443	871
115801	3443	872
115802	3443	874
115803	3444	732
115804	3444	734
115805	3444	740
115806	3444	744
115807	3444	746
115808	3444	749
115809	3444	754
115810	3444	760
115811	3444	761
115812	3444	764
115813	3444	768
115814	3444	775
115815	3444	781
115816	3444	783
115817	3444	787
115818	3444	789
115819	3444	792
115820	3444	794
115821	3444	806
115822	3444	815
115823	3444	819
115824	3444	822
115825	3444	825
115826	3444	832
115827	3444	835
115828	3444	841
115829	3444	845
115830	3444	846
115831	3444	851
115832	3444	852
115833	3444	859
115834	3444	860
115835	3444	871
115836	3444	873
115837	3444	874
115838	3445	732
115839	3445	734
115840	3445	740
115841	3445	743
115842	3445	746
115843	3445	749
115844	3445	754
115845	3445	756
115846	3445	761
115847	3445	764
115848	3445	768
115849	3445	772
115850	3445	777
115851	3445	783
115852	3445	787
115853	3445	789
115854	3445	792
115855	3445	794
115856	3445	808
115857	3445	811
115858	3445	819
115859	3445	823
115860	3445	828
115861	3445	830
115862	3445	835
115863	3445	841
115864	3445	844
115865	3445	847
115866	3445	850
115867	3445	854
115868	3445	856
115869	3445	860
115870	3445	871
115871	3445	872
115872	3445	874
115873	3446	732
115874	3446	734
115875	3446	741
115876	3446	744
115877	3446	746
115878	3446	749
115879	3446	754
115880	3446	757
115881	3446	761
115882	3446	764
115883	3446	768
115884	3446	774
115885	3446	777
115886	3446	784
115887	3446	788
115888	3446	790
115889	3446	792
115890	3446	795
115891	3446	797
115892	3446	802
115893	3446	808
115894	3446	815
115895	3446	819
115896	3446	823
115897	3446	826
115898	3446	831
115899	3446	837
115900	3446	842
115901	3446	845
115902	3446	848
115903	3446	851
115904	3446	854
115905	3446	857
115906	3446	860
115907	3446	871
115908	3446	873
115909	3446	874
115910	3447	732
115911	3447	734
115912	3447	740
115913	3447	743
115914	3447	747
115915	3447	748
115916	3447	752
115917	3447	758
115918	3447	761
115919	3447	764
115920	3447	768
115921	3447	772
115922	3447	777
115923	3447	784
115924	3447	787
115925	3447	789
115926	3447	791
115927	3447	794
115928	3447	806
115929	3447	811
115930	3447	818
115931	3447	822
115932	3447	827
115933	3447	830
115934	3447	835
115935	3447	841
115936	3447	845
115937	3447	847
115938	3447	851
115939	3447	853
115940	3447	858
115941	3447	860
115942	3447	871
115943	3447	872
115944	3447	874
115945	3448	732
115946	3448	734
115947	3448	740
115948	3448	744
115949	3448	746
115950	3448	750
115951	3448	755
115952	3448	758
115953	3448	761
115954	3448	765
115955	3448	769
115956	3448	775
115957	3448	777
115958	3448	785
115959	3448	787
115960	3448	789
115961	3448	793
115962	3448	794
115963	3448	809
115964	3448	814
115965	3448	819
115966	3448	822
115967	3448	828
115968	3448	832
115969	3448	835
115970	3448	841
115971	3448	843
115972	3448	847
115973	3448	850
115974	3448	853
115975	3448	856
115976	3448	860
115977	3448	871
115978	3448	872
115979	3448	874
115980	3449	732
115981	3449	734
115982	3449	740
115983	3449	743
115984	3449	746
115985	3449	749
115986	3449	754
115987	3449	759
115988	3449	761
115989	3449	764
115990	3449	768
115991	3449	772
115992	3449	777
115993	3449	783
115994	3449	787
115995	3449	789
115996	3449	792
115997	3449	795
115998	3449	798
115999	3449	803
116000	3449	807
116001	3449	811
116002	3449	819
116003	3449	823
116004	3449	828
116005	3449	832
116006	3449	835
116007	3449	842
116008	3449	845
116009	3449	848
116010	3449	850
116011	3449	854
116012	3449	856
116013	3449	860
116014	3449	871
116015	3449	872
116016	3449	874
116017	3450	733
116018	3450	735
116019	3450	737
116020	3450	741
116021	3450	743
116022	3450	746
116023	3450	750
116024	3450	754
116025	3450	757
116026	3450	761
116027	3450	764
116028	3450	768
116029	3450	775
116030	3450	781
116031	3450	783
116032	3450	788
116033	3450	789
116034	3450	792
116035	3450	794
116036	3450	806
116037	3450	815
116038	3450	819
116039	3450	822
116040	3450	825
116041	3450	835
116042	3450	841
116043	3450	845
116044	3450	847
116045	3450	851
116046	3450	853
116047	3450	857
116048	3450	860
116049	3450	871
116050	3450	872
116051	3450	874
116052	3451	733
116053	3451	734
116054	3451	740
116055	3451	744
116056	3451	746
116057	3451	749
116058	3451	753
116059	3451	760
116060	3451	761
116061	3451	764
116062	3451	768
116063	3451	775
116064	3451	781
116065	3451	783
116066	3451	787
116067	3451	789
116068	3451	792
116069	3451	794
116070	3451	806
116071	3451	815
116072	3451	819
116073	3451	823
116074	3451	825
116075	3451	832
116076	3451	834
116077	3451	841
116078	3451	845
116079	3451	846
116080	3451	851
116081	3451	852
116082	3451	859
116083	3451	860
116084	3451	871
116085	3451	873
116086	3451	874
116087	3452	732
116088	3452	734
116089	3452	740
116090	3452	743
116091	3452	745
116092	3452	749
116093	3452	754
116094	3452	757
116095	3452	761
116096	3452	764
116097	3452	768
116098	3452	772
116099	3452	777
116100	3452	786
116101	3452	787
116102	3452	789
116103	3452	792
116104	3452	794
116105	3452	810
116106	3452	811
116107	3452	819
116108	3452	822
116109	3452	828
116110	3452	832
116111	3452	835
116112	3452	842
116113	3452	845
116114	3452	848
116115	3452	851
116116	3452	854
116117	3452	857
116118	3452	860
116119	3452	871
116120	3452	874
116121	3453	732
116122	3453	734
116123	3453	740
116124	3453	744
116125	3453	747
116126	3453	748
116127	3453	753
116128	3453	760
116129	3453	761
116130	3453	764
116131	3453	768
116132	3453	772
116133	3453	777
116134	3453	785
116135	3453	787
116136	3453	789
116137	3453	793
116138	3453	794
116139	3453	806
116140	3453	811
116141	3453	819
116142	3453	823
116143	3453	828
116144	3453	831
116145	3453	836
116146	3453	840
116147	3453	845
116148	3453	846
116149	3453	851
116150	3453	852
116151	3453	859
116152	3453	860
116153	3453	871
116154	3453	874
116155	3454	732
116156	3454	734
116157	3454	740
116158	3454	744
116159	3454	746
116160	3454	749
116161	3454	754
116162	3454	759
116163	3454	761
116164	3454	764
116165	3454	769
116166	3454	774
116167	3454	777
116168	3454	785
116169	3454	787
116170	3454	789
116171	3454	792
116172	3454	794
116173	3454	809
116174	3454	814
116175	3454	819
116176	3454	823
116177	3454	828
116178	3454	832
116179	3454	835
116180	3454	842
116181	3454	845
116182	3454	848
116183	3454	851
116184	3454	854
116185	3454	857
116186	3454	860
116187	3454	871
116188	3454	872
116189	3454	874
116190	3455	732
116191	3455	734
116192	3455	740
116193	3455	744
116194	3455	747
116195	3455	749
116196	3455	754
116197	3455	758
116198	3455	761
116199	3455	764
116200	3455	769
116201	3455	774
116202	3455	777
116203	3455	784
116204	3455	787
116205	3455	789
116206	3455	792
116207	3455	794
116208	3455	808
116209	3455	814
116210	3455	818
116211	3455	822
116212	3455	826
116213	3455	831
116214	3455	836
116215	3455	842
116216	3455	845
116217	3455	847
116218	3455	851
116219	3455	853
116220	3455	857
116221	3455	860
116222	3455	871
116223	3455	872
116224	3455	874
116225	3456	732
116226	3456	734
116227	3456	740
116228	3456	742
116229	3456	746
116230	3456	749
116231	3456	753
116232	3456	758
116233	3456	761
116234	3456	764
116235	3456	770
116236	3456	774
116237	3456	777
116238	3456	784
116239	3456	787
116240	3456	789
116241	3456	792
116242	3456	794
116243	3456	808
116244	3456	815
116245	3456	819
116246	3456	822
116247	3456	827
116248	3456	832
116249	3456	836
116250	3456	841
116251	3456	845
116252	3456	847
116253	3456	851
116254	3456	853
116255	3456	857
116256	3456	860
116257	3456	871
116258	3456	872
116259	3456	874
116260	3457	732
116261	3457	734
116262	3457	740
116263	3457	744
116264	3457	746
116265	3457	749
116266	3457	754
116267	3457	758
116268	3457	761
116269	3457	764
116270	3457	768
116271	3457	774
116272	3457	777
116273	3457	785
116274	3457	787
116275	3457	789
116276	3457	793
116277	3457	795
116278	3457	800
116279	3457	803
116280	3457	808
116281	3457	815
116282	3457	819
116283	3457	823
116284	3457	828
116285	3457	832
116286	3457	836
116287	3457	842
116288	3457	845
116289	3457	847
116290	3457	851
116291	3457	853
116292	3457	857
116293	3457	860
116294	3457	871
116295	3457	874
116296	3458	732
116297	3458	734
116298	3458	740
116299	3458	743
116300	3458	747
116301	3458	749
116302	3458	754
116303	3458	758
116304	3458	761
116305	3458	764
116306	3458	768
116307	3458	772
116308	3458	779
116309	3458	784
116310	3458	787
116311	3458	789
116312	3458	792
116313	3458	795
116314	3458	798
116315	3458	803
116316	3458	808
116317	3458	811
116318	3458	819
116319	3458	822
116320	3458	826
116321	3458	832
116322	3458	835
116323	3458	841
116324	3458	845
116325	3458	847
116326	3458	851
116327	3458	853
116328	3458	857
116329	3458	860
116330	3458	871
116331	3458	872
116332	3458	874
116333	3459	732
116334	3459	734
116335	3459	740
116336	3459	743
116337	3459	746
116338	3459	749
116339	3459	753
116340	3459	759
116341	3459	761
116342	3459	764
116343	3459	768
116344	3459	775
116345	3459	777
116346	3459	783
116347	3459	787
116348	3459	789
116349	3459	793
116350	3459	794
116351	3459	806
116352	3459	815
116353	3459	819
116354	3459	823
116355	3459	828
116356	3459	832
116357	3459	835
116358	3459	841
116359	3459	845
116360	3459	846
116361	3459	851
116362	3459	852
116363	3459	859
116364	3459	860
116365	3459	871
116366	3459	873
116367	3459	874
116368	3460	732
116369	3460	734
116370	3460	740
116371	3460	742
116372	3460	746
116373	3460	749
116374	3460	754
116375	3460	757
116376	3460	761
116377	3460	764
116378	3460	768
116379	3460	772
116380	3460	777
116381	3460	783
116382	3460	787
116383	3460	789
116384	3460	792
116385	3460	794
116386	3460	808
116387	3460	811
116388	3460	818
116389	3460	822
116390	3460	826
116391	3460	830
116392	3460	835
116393	3460	841
116394	3460	844
116395	3460	847
116396	3460	851
116397	3460	853
116398	3460	857
116399	3460	860
116400	3460	871
116401	3460	872
116402	3460	874
116403	3461	731
116404	3461	734
116405	3461	740
116406	3461	744
116407	3461	747
116408	3461	749
116409	3461	755
116410	3461	758
116411	3461	761
116412	3461	764
116413	3461	768
116414	3461	772
116415	3461	777
116416	3461	786
116417	3461	787
116418	3461	789
116419	3461	792
116420	3461	794
116421	3461	808
116422	3461	811
116423	3461	819
116424	3461	822
116425	3461	828
116426	3461	832
116427	3461	835
116428	3461	842
116429	3461	845
116430	3461	847
116431	3461	851
116432	3461	854
116433	3461	857
116434	3461	860
116435	3461	871
116436	3461	872
116437	3461	874
116438	3462	732
116439	3462	734
116440	3462	740
116441	3462	743
116442	3462	747
116443	3462	748
116444	3462	752
116445	3462	758
116446	3462	761
116447	3462	764
116448	3462	768
116449	3462	772
116450	3462	777
116451	3462	784
116452	3462	787
116453	3462	789
116454	3462	791
116455	3462	794
116456	3462	806
116457	3462	811
116458	3462	817
116459	3462	821
116460	3462	827
116461	3462	831
116462	3462	835
116463	3462	841
116464	3462	845
116465	3462	847
116466	3462	851
116467	3462	853
116468	3462	858
116469	3462	860
116470	3462	871
116471	3462	873
116472	3462	874
116473	3463	732
116474	3463	734
116475	3463	740
116476	3463	742
116477	3463	747
116478	3463	749
116479	3463	754
116480	3463	759
116481	3463	761
116482	3463	764
116483	3463	769
116484	3463	775
116485	3463	777
116486	3463	782
116487	3463	787
116488	3463	789
116489	3463	792
116490	3463	794
116491	3463	809
116492	3463	814
116493	3463	819
116494	3463	822
116495	3463	827
116496	3463	832
116497	3463	837
116498	3463	842
116499	3463	845
116500	3463	847
116501	3463	851
116502	3463	854
116503	3463	857
116504	3463	860
116505	3463	871
116506	3463	873
116507	3463	874
116508	3464	732
116509	3464	734
116510	3464	740
116511	3464	743
116512	3464	746
116513	3464	748
116514	3464	753
116515	3464	758
116516	3464	761
116517	3464	764
116518	3464	768
116519	3464	772
116520	3464	777
116521	3464	783
116522	3464	787
116523	3464	789
116524	3464	792
116525	3464	795
116526	3464	797
116527	3464	802
116528	3464	806
116529	3464	811
116530	3464	819
116531	3464	822
116532	3464	827
116533	3464	831
116534	3464	835
116535	3464	841
116536	3464	845
116537	3464	847
116538	3464	851
116539	3464	853
116540	3464	857
116541	3464	860
116542	3464	871
116543	3464	872
116544	3464	874
116545	3465	732
116546	3465	734
116547	3465	740
116548	3465	743
116549	3465	745
116550	3465	749
116551	3465	754
116552	3465	757
116553	3465	761
116554	3465	764
116555	3465	768
116556	3465	772
116557	3465	777
116558	3465	784
116559	3465	787
116560	3465	789
116561	3465	793
116562	3465	794
116563	3465	810
116564	3465	811
116565	3465	819
116566	3465	822
116567	3465	828
116568	3465	830
116569	3465	835
116570	3465	841
116571	3465	845
116572	3465	847
116573	3465	850
116574	3465	853
116575	3465	857
116576	3465	860
116577	3465	871
116578	3465	872
116579	3465	874
116580	3466	731
116581	3466	734
116582	3466	740
116583	3466	743
116584	3466	747
116585	3466	749
116586	3466	753
116587	3466	760
116588	3466	761
116589	3466	764
116590	3466	768
116591	3466	772
116592	3466	777
116593	3466	783
116594	3466	787
116595	3466	789
116596	3466	792
116597	3466	795
116598	3466	798
116599	3466	803
116600	3466	808
116601	3466	811
116602	3466	818
116603	3466	822
116604	3466	828
116605	3466	833
116606	3466	835
116607	3466	842
116608	3466	845
116609	3466	847
116610	3466	851
116611	3466	853
116612	3466	857
116613	3466	860
116614	3466	871
116615	3466	874
116616	3467	732
116617	3467	734
116618	3467	740
116619	3467	744
116620	3467	746
116621	3467	748
116622	3467	752
116623	3467	760
116624	3467	761
116625	3467	764
116626	3467	768
116627	3467	775
116628	3467	780
116629	3467	782
116630	3467	787
116631	3467	789
116632	3467	792
116633	3467	794
116634	3467	806
116635	3467	815
116636	3467	819
116637	3467	823
116638	3467	824
116639	3467	833
116640	3467	835
116641	3467	840
116642	3467	845
116643	3467	846
116644	3467	851
116645	3467	852
116646	3467	859
116647	3467	860
116648	3467	871
116649	3467	873
116650	3467	874
116651	3468	732
116652	3468	735
116653	3468	737
116654	3468	740
116655	3468	742
116656	3468	745
116657	3468	748
116658	3468	752
116659	3468	760
116660	3468	761
116661	3468	764
116662	3468	768
116663	3468	775
116664	3468	781
116665	3468	782
116666	3468	787
116667	3468	789
116668	3468	791
116669	3468	795
116670	3468	797
116671	3468	802
116672	3468	808
116673	3468	816
116674	3468	819
116675	3468	823
116676	3468	824
116677	3468	833
116678	3468	835
116679	3468	840
116680	3468	845
116681	3468	846
116682	3468	851
116683	3468	852
116684	3468	858
116685	3468	860
116686	3468	871
116687	3468	872
116688	3468	874
116689	3469	731
116690	3469	734
116691	3469	740
116692	3469	743
116693	3469	746
116694	3469	748
116695	3469	754
116696	3469	760
116697	3469	761
116698	3469	764
116699	3469	768
116700	3469	772
116701	3469	777
116702	3469	783
116703	3469	787
116704	3469	789
116705	3469	792
116706	3469	794
116707	3469	808
116708	3469	811
116709	3469	819
116710	3469	822
116711	3469	827
116712	3469	830
116713	3469	835
116714	3469	841
116715	3469	845
116716	3469	847
116717	3469	851
116718	3469	852
116719	3469	858
116720	3469	860
116721	3469	871
116722	3469	874
116723	3470	732
116724	3470	734
116725	3470	740
116726	3470	744
116727	3470	746
116728	3470	750
116729	3470	755
116730	3470	758
116731	3470	761
116732	3470	764
116733	3470	768
116734	3470	772
116735	3470	777
116736	3470	785
116737	3470	787
116738	3470	789
116739	3470	792
116740	3470	795
116741	3470	797
116742	3470	802
116743	3470	810
116744	3470	811
116745	3470	819
116746	3470	823
116747	3470	828
116748	3470	831
116749	3470	834
116750	3470	841
116751	3470	845
116752	3470	848
116753	3470	851
116754	3470	854
116755	3470	857
116756	3470	860
116757	3470	871
116758	3470	872
116759	3470	874
116760	3471	731
116761	3471	734
116762	3471	740
116763	3471	744
116764	3471	745
116765	3471	749
116766	3471	753
116767	3471	758
116768	3471	761
116769	3471	764
116770	3471	768
116771	3471	772
116772	3471	777
116773	3471	785
116774	3471	787
116775	3471	789
116776	3471	792
116777	3471	794
116778	3471	806
116779	3471	811
116780	3471	819
116781	3471	823
116782	3471	827
116783	3471	834
116784	3471	841
116785	3471	845
116786	3471	846
116787	3471	851
116788	3471	852
116789	3471	859
116790	3471	860
116791	3471	871
116792	3471	872
116793	3471	874
116794	3472	732
116795	3472	734
116796	3472	740
116797	3472	744
116798	3472	746
116799	3472	749
116800	3472	753
116801	3472	758
116802	3472	761
116803	3472	764
116804	3472	768
116805	3472	772
116806	3472	777
116807	3472	784
116808	3472	787
116809	3472	789
116810	3472	792
116811	3472	795
116812	3472	799
116813	3472	801
116814	3472	809
116815	3472	811
116816	3472	819
116817	3472	822
116818	3472	828
116819	3472	834
116820	3472	842
116821	3472	845
116822	3472	848
116823	3472	851
116824	3472	854
116825	3472	857
116826	3472	860
116827	3472	871
116828	3472	872
116829	3472	874
116830	3473	732
116831	3473	734
116832	3473	740
116833	3473	744
116834	3473	746
116835	3473	749
116836	3473	755
116837	3473	760
116838	3473	761
116839	3473	764
116840	3473	768
116841	3473	772
116842	3473	777
116843	3473	783
116844	3473	787
116845	3473	789
116846	3473	793
116847	3473	794
116848	3473	808
116849	3473	811
116850	3473	819
116851	3473	823
116852	3473	828
116853	3473	832
116854	3473	835
116855	3473	841
116856	3473	845
116857	3473	846
116858	3473	851
116859	3473	852
116860	3473	859
116861	3473	860
116862	3473	871
116863	3473	874
116864	3474	732
116865	3474	734
116866	3474	740
116867	3474	744
116868	3474	745
116869	3474	749
116870	3474	754
116871	3474	759
116872	3474	761
116873	3474	764
116874	3474	768
116875	3474	772
116876	3474	777
116877	3474	784
116878	3474	787
116879	3474	789
116880	3474	792
116881	3474	794
116882	3474	809
116883	3474	811
116884	3474	819
116885	3474	822
116886	3474	828
116887	3474	831
116888	3474	835
116889	3474	840
116890	3474	844
116891	3474	847
116892	3474	850
116893	3474	854
116894	3474	857
116895	3474	860
116896	3474	871
116897	3474	874
116898	3475	732
116899	3475	734
116900	3475	740
116901	3475	743
116902	3475	746
116903	3475	748
116904	3475	752
116905	3475	760
116906	3475	761
116907	3475	764
116908	3475	768
116909	3475	772
116910	3475	777
116911	3475	784
116912	3475	787
116913	3475	789
116914	3475	792
116915	3475	794
116916	3475	806
116917	3475	811
116918	3475	819
116919	3475	823
116920	3475	827
116921	3475	831
116922	3475	835
116923	3475	840
116924	3475	845
116925	3475	846
116926	3475	851
116927	3475	852
116928	3475	859
116929	3475	860
116930	3475	871
116931	3475	873
116932	3475	874
116933	3476	732
116934	3476	734
116935	3476	740
116936	3476	743
116937	3476	747
116938	3476	749
116939	3476	753
116940	3476	758
116941	3476	761
116942	3476	764
116943	3476	768
116944	3476	772
116945	3476	777
116946	3476	784
116947	3476	787
116948	3476	789
116949	3476	792
116950	3476	794
116951	3476	808
116952	3476	811
116953	3476	818
116954	3476	821
116955	3476	828
116956	3476	832
116957	3476	835
116958	3476	841
116959	3476	845
116960	3476	847
116961	3476	851
116962	3476	853
116963	3476	857
116964	3476	860
116965	3476	871
116966	3476	872
116967	3476	874
116968	3477	732
116969	3477	734
116970	3477	740
116971	3477	743
116972	3477	747
116973	3477	748
116974	3477	753
116975	3477	759
116976	3477	761
116977	3477	764
116978	3477	768
116979	3477	772
116980	3477	777
116981	3477	783
116982	3477	787
116983	3477	789
116984	3477	791
116985	3477	794
116986	3477	808
116987	3477	811
116988	3477	819
116989	3477	822
116990	3477	827
116991	3477	833
116992	3477	835
116993	3477	842
116994	3477	844
116995	3477	848
116996	3477	850
116997	3477	854
116998	3477	856
116999	3477	860
117000	3477	871
117001	3477	872
117002	3477	874
117003	3478	733
117004	3478	734
117005	3478	740
117006	3478	742
117007	3478	745
117008	3478	749
117009	3478	752
117010	3478	758
117011	3478	761
117012	3478	764
117013	3478	768
117014	3478	772
117015	3478	777
117016	3478	783
117017	3478	787
117018	3478	789
117019	3478	792
117020	3478	794
117021	3478	806
117022	3478	811
117023	3478	819
117024	3478	823
117025	3478	827
117026	3478	831
117027	3478	835
117028	3478	841
117029	3478	845
117030	3478	846
117031	3478	851
117032	3478	852
117033	3478	859
117034	3478	860
117035	3478	871
117036	3478	872
117037	3478	874
117038	3479	733
117039	3479	734
117040	3479	740
117041	3479	743
117042	3479	747
117043	3479	749
117044	3479	753
117045	3479	758
117046	3479	761
117047	3479	764
117048	3479	768
117049	3479	772
117050	3479	777
117051	3479	784
117052	3479	787
117053	3479	789
117054	3479	791
117055	3479	794
117056	3479	806
117057	3479	811
117058	3479	818
117059	3479	822
117060	3479	828
117061	3479	831
117062	3479	835
117063	3479	841
117064	3479	845
117065	3479	847
117066	3479	851
117067	3479	853
117068	3479	858
117069	3479	860
117070	3479	871
117071	3479	872
117072	3479	874
117073	3480	732
117074	3480	734
117075	3480	740
117076	3480	744
117077	3480	746
117078	3480	748
117079	3480	753
117080	3480	758
117081	3480	761
117082	3480	764
117083	3480	768
117084	3480	772
117085	3480	777
117086	3480	782
117087	3480	787
117088	3480	789
117089	3480	792
117090	3480	794
117091	3480	806
117092	3480	811
117093	3480	819
117094	3480	822
117095	3480	828
117096	3480	830
117097	3480	835
117098	3480	841
117099	3480	845
117100	3480	847
117101	3480	851
117102	3480	853
117103	3480	857
117104	3480	860
117105	3480	871
117106	3480	872
117107	3480	874
117108	3481	732
117109	3481	734
117110	3481	740
117111	3481	743
117112	3481	746
117113	3481	749
117114	3481	753
117115	3481	759
117116	3481	761
117117	3481	764
117118	3481	768
117119	3481	775
117120	3481	777
117121	3481	784
117122	3481	787
117123	3481	789
117124	3481	792
117125	3481	794
117126	3481	806
117127	3481	816
117128	3481	819
117129	3481	823
117130	3481	828
117131	3481	832
117132	3481	835
117133	3481	840
117134	3481	845
117135	3481	846
117136	3481	851
117137	3481	852
117138	3481	859
117139	3481	860
117140	3481	871
117141	3481	872
117142	3481	874
117143	3482	733
117144	3482	734
117145	3482	740
117146	3482	743
117147	3482	746
117148	3482	749
117149	3482	753
117150	3482	760
117151	3482	761
117152	3482	764
117153	3482	768
117154	3482	772
117155	3482	777
117156	3482	782
117157	3482	787
117158	3482	789
117159	3482	792
117160	3482	794
117161	3482	809
117162	3482	811
117163	3482	819
117164	3482	822
117165	3482	826
117166	3482	833
117167	3482	835
117168	3482	841
117169	3482	844
117170	3482	848
117171	3482	850
117172	3482	854
117173	3482	856
117174	3482	860
117175	3482	871
117176	3482	873
117177	3482	874
117178	3483	732
117179	3483	734
117180	3483	740
117181	3483	743
117182	3483	746
117183	3483	749
117184	3483	753
117185	3483	758
117186	3483	761
117187	3483	764
117188	3483	768
117189	3483	772
117190	3483	777
117191	3483	784
117192	3483	787
117193	3483	789
117194	3483	792
117195	3483	795
117196	3483	798
117197	3483	803
117198	3483	808
117199	3483	811
117200	3483	818
117201	3483	822
117202	3483	828
117203	3483	835
117204	3483	841
117205	3483	843
117206	3483	847
117207	3483	849
117208	3483	853
117209	3483	856
117210	3483	860
117211	3483	871
117212	3483	872
117213	3483	874
117214	3484	732
117215	3484	734
117216	3484	740
117217	3484	744
117218	3484	746
117219	3484	749
117220	3484	753
117221	3484	760
117222	3484	761
117223	3484	764
117224	3484	768
117225	3484	772
117226	3484	777
117227	3484	783
117228	3484	787
117229	3484	789
117230	3484	792
117231	3484	795
117232	3484	797
117233	3484	801
117234	3484	809
117235	3484	811
117236	3484	819
117237	3484	821
117238	3484	827
117239	3484	833
117240	3484	835
117241	3484	842
117242	3484	844
117243	3484	847
117244	3484	850
117245	3484	854
117246	3484	856
117247	3484	860
117248	3484	871
117249	3484	872
117250	3484	874
117251	3485	732
117252	3485	734
117253	3485	740
117254	3485	743
117255	3485	746
117256	3485	750
117257	3485	754
117258	3485	757
117259	3485	761
117260	3485	765
117261	3485	769
117262	3485	775
117263	3485	777
117264	3485	784
117265	3485	787
117266	3485	789
117267	3485	792
117268	3485	794
117269	3485	809
117270	3485	813
117271	3485	818
117272	3485	822
117273	3485	826
117274	3485	831
117275	3485	835
117276	3485	841
117277	3485	844
117278	3485	847
117279	3485	850
117280	3485	854
117281	3485	856
117282	3485	860
117283	3485	871
117284	3485	873
117285	3485	874
117286	3486	732
117287	3486	734
117288	3486	740
117289	3486	743
117290	3486	746
117291	3486	749
117292	3486	753
117293	3486	760
117294	3486	761
117295	3486	764
117296	3486	768
117297	3486	772
117298	3486	777
117299	3486	784
117300	3486	787
117301	3486	789
117302	3486	793
117303	3486	794
117304	3486	809
117305	3486	811
117306	3486	819
117307	3486	823
117308	3486	828
117309	3486	831
117310	3486	835
117311	3486	841
117312	3486	844
117313	3486	847
117314	3486	849
117315	3486	853
117316	3486	856
117317	3486	860
117318	3486	869
117319	3486	872
117320	3486	874
117321	3487	732
117322	3487	734
117323	3487	740
117324	3487	744
117325	3487	746
117326	3487	750
117327	3487	755
117328	3487	758
117329	3487	761
117330	3487	764
117331	3487	768
117332	3487	772
117333	3487	777
117334	3487	784
117335	3487	787
117336	3487	789
117337	3487	792
117338	3487	794
117339	3487	808
117340	3487	811
117341	3487	819
117342	3487	822
117343	3487	827
117344	3487	831
117345	3487	835
117346	3487	842
117347	3487	845
117348	3487	847
117349	3487	851
117350	3487	853
117351	3487	858
117352	3487	860
117353	3487	871
117354	3487	874
117355	3488	732
117356	3488	734
117357	3488	740
117358	3488	743
117359	3488	746
117360	3488	750
117361	3488	754
117362	3488	758
117363	3488	761
117364	3488	764
117365	3488	768
117366	3488	774
117367	3488	777
117368	3488	783
117369	3488	787
117370	3488	789
117371	3488	792
117372	3488	794
117373	3488	806
117374	3488	814
117375	3488	819
117376	3488	823
117377	3488	828
117378	3488	830
117379	3488	835
117380	3488	841
117381	3488	845
117382	3488	846
117383	3488	851
117384	3488	852
117385	3488	859
117386	3488	860
117387	3488	871
117388	3488	873
117389	3488	874
117390	3489	732
117391	3489	734
117392	3489	740
117393	3489	744
117394	3489	747
117395	3489	750
117396	3489	754
117397	3489	760
117398	3489	761
117399	3489	764
117400	3489	768
117401	3489	772
117402	3489	777
117403	3489	782
117404	3489	787
117405	3489	789
117406	3489	792
117407	3489	794
117408	3489	809
117409	3489	811
117410	3489	819
117411	3489	822
117412	3489	826
117413	3489	833
117414	3489	835
117415	3489	841
117416	3489	845
117417	3489	847
117418	3489	851
117419	3489	852
117420	3489	858
117421	3489	860
117422	3489	871
117423	3489	874
117424	3490	732
117425	3490	734
117426	3490	740
117427	3490	743
117428	3490	745
117429	3490	749
117430	3490	754
117431	3490	757
117432	3490	761
117433	3490	764
117434	3490	768
117435	3490	775
117436	3490	781
117437	3490	783
117438	3490	787
117439	3490	789
117440	3490	792
117441	3490	794
117442	3490	806
117443	3490	815
117444	3490	819
117445	3490	822
117446	3490	827
117447	3490	830
117448	3490	834
117449	3490	840
117450	3490	845
117451	3490	846
117452	3490	851
117453	3490	852
117454	3490	859
117455	3490	860
117456	3490	871
117457	3490	873
117458	3490	874
117459	3491	732
117460	3491	734
117461	3491	740
117462	3491	743
117463	3491	746
117464	3491	749
117465	3491	754
117466	3491	758
117467	3491	761
117468	3491	764
117469	3491	768
117470	3491	772
117471	3491	777
117472	3491	783
117473	3491	787
117474	3491	789
117475	3491	793
117476	3491	795
117477	3491	796
117478	3491	801
117479	3491	806
117480	3491	811
117481	3491	819
117482	3491	823
117483	3491	828
117484	3491	830
117485	3491	835
117486	3491	841
117487	3491	845
117488	3491	847
117489	3491	851
117490	3491	853
117491	3491	858
117492	3491	860
117493	3491	871
117494	3491	872
117495	3491	874
117496	3492	732
117497	3492	734
117498	3492	740
117499	3492	743
117500	3492	746
117501	3492	748
117502	3492	752
117503	3492	758
117504	3492	761
117505	3492	764
117506	3492	768
117507	3492	772
117508	3492	781
117509	3492	783
117510	3492	787
117511	3492	789
117512	3492	793
117513	3492	794
117514	3492	806
117515	3492	811
117516	3492	819
117517	3492	823
117518	3492	826
117519	3492	831
117520	3492	835
117521	3492	841
117522	3492	845
117523	3492	847
117524	3492	851
117525	3492	852
117526	3492	858
117527	3492	860
117528	3492	871
117529	3492	872
117530	3492	874
117531	3493	733
117532	3493	734
117533	3493	740
117534	3493	743
117535	3493	747
117536	3493	749
117537	3493	753
117538	3493	759
117539	3493	761
117540	3493	764
117541	3493	768
117542	3493	772
117543	3493	777
117544	3493	782
117545	3493	787
117546	3493	789
117547	3493	792
117548	3493	794
117549	3493	809
117550	3493	811
117551	3493	818
117552	3493	821
117553	3493	827
117554	3493	832
117555	3493	835
117556	3493	842
117557	3493	844
117558	3493	848
117559	3493	850
117560	3493	854
117561	3493	856
117562	3493	860
117563	3493	871
117564	3493	872
117565	3493	874
117566	3494	732
117567	3494	734
117568	3494	740
117569	3494	743
117570	3494	746
117571	3494	749
117572	3494	754
117573	3494	758
117574	3494	761
117575	3494	764
117576	3494	768
117577	3494	772
117578	3494	777
117579	3494	783
117580	3494	787
117581	3494	789
117582	3494	792
117583	3494	794
117584	3494	809
117585	3494	811
117586	3494	818
117587	3494	822
117588	3494	826
117589	3494	832
117590	3494	835
117591	3494	841
117592	3494	845
117593	3494	847
117594	3494	851
117595	3494	853
117596	3494	858
117597	3494	860
117598	3494	871
117599	3494	872
117600	3494	874
117601	3495	732
117602	3495	734
117603	3495	740
117604	3495	743
117605	3495	747
117606	3495	749
117607	3495	753
117608	3495	758
117609	3495	761
117610	3495	764
117611	3495	768
117612	3495	772
117613	3495	777
117614	3495	784
117615	3495	787
117616	3495	789
117617	3495	792
117618	3495	795
117619	3495	798
117620	3495	804
117621	3495	809
117622	3495	811
117623	3495	819
117624	3495	822
117625	3495	826
117626	3495	831
117627	3495	835
117628	3495	841
117629	3495	843
117630	3495	847
117631	3495	849
117632	3495	853
117633	3495	856
117634	3495	860
117635	3495	871
117636	3495	872
117637	3495	874
117638	3496	732
117639	3496	734
117640	3496	740
117641	3496	744
117642	3496	745
117643	3496	749
117644	3496	753
117645	3496	758
117646	3496	761
117647	3496	764
117648	3496	768
117649	3496	772
117650	3496	777
117651	3496	782
117652	3496	787
117653	3496	789
117654	3496	792
117655	3496	794
117656	3496	808
117657	3496	811
117658	3496	819
117659	3496	823
117660	3496	827
117661	3496	831
117662	3496	835
117663	3496	841
117664	3496	845
117665	3496	846
117666	3496	851
117667	3496	852
117668	3496	859
117669	3496	860
117670	3496	871
117671	3496	874
117672	3497	732
117673	3497	734
117674	3497	740
117675	3497	742
117676	3497	747
117677	3497	748
117678	3497	753
117679	3497	758
117680	3497	761
117681	3497	764
117682	3497	768
117683	3497	772
117684	3497	777
117685	3497	783
117686	3497	787
117687	3497	789
117688	3497	791
117689	3497	794
117690	3497	807
117691	3497	811
117692	3497	818
117693	3497	821
117694	3497	828
117695	3497	831
117696	3497	835
117697	3497	841
117698	3497	843
117699	3497	847
117700	3497	849
117701	3497	853
117702	3497	856
117703	3497	860
117704	3497	871
117705	3497	872
117706	3497	874
117707	3498	732
117708	3498	735
117709	3498	737
117710	3498	741
117711	3498	744
117712	3498	746
117713	3498	748
117714	3498	752
117715	3498	760
117716	3498	761
117717	3498	764
117718	3498	768
117719	3498	775
117720	3498	781
117721	3498	784
117722	3498	787
117723	3498	789
117724	3498	793
117725	3498	795
117726	3498	797
117727	3498	803
117728	3498	807
117729	3498	814
117730	3498	819
117731	3498	823
117732	3498	827
117733	3498	833
117734	3498	835
117735	3498	841
117736	3498	845
117737	3498	846
117738	3498	851
117739	3498	852
117740	3498	858
117741	3498	860
117742	3498	871
117743	3498	872
117744	3498	874
117745	3499	732
117746	3499	734
117747	3499	740
117748	3499	744
117749	3499	746
117750	3499	748
117751	3499	752
117752	3499	760
117753	3499	761
117754	3499	764
117755	3499	768
117756	3499	772
117757	3499	777
117758	3499	784
117759	3499	787
117760	3499	789
117761	3499	793
117762	3499	795
117763	3499	797
117764	3499	801
117765	3499	807
117766	3499	811
117767	3499	819
117768	3499	823
117769	3499	827
117770	3499	833
117771	3499	835
117772	3499	840
117773	3499	845
117774	3499	846
117775	3499	851
117776	3499	852
117777	3499	858
117778	3499	860
117779	3499	871
117780	3499	872
117781	3499	874
117782	3500	732
117783	3500	734
117784	3500	740
117785	3500	743
117786	3500	746
117787	3500	748
117788	3500	753
117789	3500	758
117790	3500	761
117791	3500	764
117792	3500	769
117793	3500	775
117794	3500	777
117795	3500	785
117796	3500	787
117797	3500	789
117798	3500	792
117799	3500	795
117800	3500	797
117801	3500	802
117802	3500	807
117803	3500	814
117804	3500	818
117805	3500	822
117806	3500	827
117807	3500	831
117808	3500	835
117809	3500	841
117810	3500	843
117811	3500	847
117812	3500	849
117813	3500	854
117814	3500	856
117815	3500	860
117816	3500	871
117817	3500	872
117818	3500	874
117819	3501	733
117820	3501	734
117821	3501	740
117822	3501	743
117823	3501	746
117824	3501	749
117825	3501	753
117826	3501	758
117827	3501	761
117828	3501	764
117829	3501	768
117830	3501	772
117831	3501	777
117832	3501	783
117833	3501	787
117834	3501	789
117835	3501	792
117836	3501	794
117837	3501	806
117838	3501	811
117839	3501	819
117840	3501	822
117841	3501	828
117842	3501	830
117843	3501	835
117844	3501	841
117845	3501	845
117846	3501	846
117847	3501	851
117848	3501	852
117849	3501	859
117850	3501	860
117851	3501	871
117852	3501	873
117853	3501	874
117854	3502	732
117855	3502	734
117856	3502	740
117857	3502	743
117858	3502	745
117859	3502	748
117860	3502	752
117861	3502	758
117862	3502	761
117863	3502	764
117864	3502	768
117865	3502	772
117866	3502	777
117867	3502	783
117868	3502	787
117869	3502	789
117870	3502	792
117871	3502	794
117872	3502	808
117873	3502	811
117874	3502	818
117875	3502	822
117876	3502	828
117877	3502	831
117878	3502	835
117879	3502	841
117880	3502	843
117881	3502	847
117882	3502	849
117883	3502	853
117884	3502	856
117885	3502	860
117886	3502	871
117887	3502	872
117888	3502	874
117889	3503	732
117890	3503	734
117891	3503	740
117892	3503	744
117893	3503	746
117894	3503	749
117895	3503	753
117896	3503	760
117897	3503	761
117898	3503	764
117899	3503	768
117900	3503	775
117901	3503	777
117902	3503	784
117903	3503	787
117904	3503	789
117905	3503	792
117906	3503	795
117907	3503	796
117908	3503	801
117909	3503	808
117910	3503	814
117911	3503	819
117912	3503	822
117913	3503	826
117914	3503	833
117915	3503	837
117916	3503	841
117917	3503	845
117918	3503	847
117919	3503	850
117920	3503	853
117921	3503	857
117922	3503	860
117923	3503	871
117924	3503	874
117925	3504	732
117926	3504	734
117927	3504	740
117928	3504	743
117929	3504	747
117930	3504	749
117931	3504	755
117932	3504	760
117933	3504	761
117934	3504	764
117935	3504	768
117936	3504	772
117937	3504	777
117938	3504	783
117939	3504	787
117940	3504	789
117941	3504	792
117942	3504	795
117943	3504	796
117944	3504	801
117945	3504	809
117946	3504	811
117947	3504	819
117948	3504	823
117949	3504	828
117950	3504	833
117951	3504	835
117952	3504	842
117953	3504	845
117954	3504	848
117955	3504	851
117956	3504	854
117957	3504	857
117958	3504	860
117959	3504	871
117960	3504	872
117961	3504	874
117962	3505	732
117963	3505	734
117964	3505	740
117965	3505	744
117966	3505	747
117967	3505	748
117968	3505	752
117969	3505	760
117970	3505	761
117971	3505	764
117972	3505	768
117973	3505	775
117974	3505	777
117975	3505	784
117976	3505	787
117977	3505	789
117978	3505	792
117979	3505	794
117980	3505	808
117981	3505	814
117982	3505	819
117983	3505	823
117984	3505	824
117985	3505	833
117986	3505	835
117987	3505	841
117988	3505	845
117989	3505	847
117990	3505	851
117991	3505	853
117992	3505	858
117993	3505	860
117994	3505	871
117995	3505	872
117996	3505	874
117997	3506	732
117998	3506	734
117999	3506	740
118000	3506	744
118001	3506	747
118002	3506	748
118003	3506	752
118004	3506	760
118005	3506	761
118006	3506	764
118007	3506	768
118008	3506	773
118009	3506	777
118010	3506	784
118011	3506	787
118012	3506	789
118013	3506	793
118014	3506	795
118015	3506	796
118016	3506	801
118017	3506	808
118018	3506	811
118019	3506	819
118020	3506	823
118021	3506	828
118022	3506	833
118023	3506	835
118024	3506	840
118025	3506	844
118026	3506	847
118027	3506	850
118028	3506	853
118029	3506	856
118030	3506	860
118031	3506	871
118032	3506	872
118033	3506	874
118034	3507	733
118035	3507	734
118036	3507	740
118037	3507	743
118038	3507	747
118039	3507	748
118040	3507	752
118041	3507	760
118042	3507	761
118043	3507	764
118044	3507	768
118045	3507	772
118046	3507	777
118047	3507	783
118048	3507	787
118049	3507	789
118050	3507	791
118051	3507	795
118052	3507	796
118053	3507	802
118054	3507	808
118055	3507	811
118056	3507	818
118057	3507	821
118058	3507	827
118059	3507	833
118060	3507	835
118061	3507	840
118062	3507	843
118063	3507	847
118064	3507	849
118065	3507	853
118066	3507	856
118067	3507	860
118068	3507	871
118069	3507	872
118070	3507	874
118071	3508	732
118072	3508	734
118073	3508	741
118074	3508	744
118075	3508	747
118076	3508	748
118077	3508	752
118078	3508	760
118079	3508	761
118080	3508	764
118081	3508	768
118082	3508	776
118083	3508	781
118084	3508	784
118085	3508	787
118086	3508	789
118087	3508	793
118088	3508	795
118089	3508	799
118090	3508	803
118091	3508	807
118092	3508	814
118093	3508	819
118094	3508	823
118095	3508	827
118096	3508	833
118097	3508	835
118098	3508	840
118099	3508	845
118100	3508	847
118101	3508	851
118102	3508	852
118103	3508	858
118104	3508	860
118105	3508	871
118106	3508	872
118107	3508	874
118108	3509	732
118109	3509	734
118110	3509	741
118111	3509	743
118112	3509	746
118113	3509	748
118114	3509	752
118115	3509	760
118116	3509	761
118117	3509	764
118118	3509	768
118119	3509	775
118120	3509	781
118121	3509	784
118122	3509	787
118123	3509	789
118124	3509	793
118125	3509	795
118126	3509	796
118127	3509	802
118128	3509	807
118129	3509	814
118130	3509	819
118131	3509	823
118132	3509	827
118133	3509	833
118134	3509	835
118135	3509	840
118136	3509	845
118137	3509	847
118138	3509	851
118139	3509	853
118140	3509	858
118141	3509	860
118142	3509	871
118143	3509	872
118144	3509	874
118145	3510	732
118146	3510	734
118147	3510	740
118148	3510	743
118149	3510	747
118150	3510	748
118151	3510	752
118152	3510	760
118153	3510	761
118154	3510	764
118155	3510	768
118156	3510	775
118157	3510	777
118158	3510	783
118159	3510	787
118160	3510	789
118161	3510	793
118162	3510	795
118163	3510	796
118164	3510	802
118165	3510	807
118166	3510	814
118167	3510	819
118168	3510	822
118169	3510	825
118170	3510	833
118171	3510	835
118172	3510	841
118173	3510	845
118174	3510	847
118175	3510	851
118176	3510	853
118177	3510	858
118178	3510	860
118179	3510	871
118180	3510	872
118181	3510	874
118182	3511	732
118183	3511	734
118184	3511	740
118185	3511	744
118186	3511	747
118187	3511	749
118188	3511	754
118189	3511	760
118190	3511	761
118191	3511	764
118192	3511	768
118193	3511	772
118194	3511	777
118195	3511	782
118196	3511	787
118197	3511	789
118198	3511	792
118199	3511	795
118200	3511	798
118201	3511	802
118202	3511	809
118203	3511	811
118204	3511	819
118205	3511	822
118206	3511	827
118207	3511	833
118208	3511	835
118209	3511	841
118210	3511	845
118211	3511	847
118212	3511	851
118213	3511	853
118214	3511	858
118215	3511	860
118216	3511	871
118217	3511	874
118218	3512	732
118219	3512	734
118220	3512	740
118221	3512	743
118222	3512	746
118223	3512	749
118224	3512	754
118225	3512	759
118226	3512	761
118227	3512	764
118228	3512	768
118229	3512	773
118230	3512	780
118231	3512	784
118232	3512	787
118233	3512	790
118234	3512	792
118235	3512	794
118236	3512	806
118237	3512	816
118238	3512	819
118239	3512	823
118240	3512	826
118241	3512	831
118242	3512	836
118243	3512	840
118244	3512	845
118245	3512	846
118246	3512	851
118247	3512	852
118248	3512	859
118249	3512	860
118250	3512	871
118251	3512	874
118252	3513	732
118253	3513	734
118254	3513	740
118255	3513	742
118256	3513	747
118257	3513	750
118258	3513	754
118259	3513	756
118260	3513	761
118261	3513	764
118262	3513	768
118263	3513	772
118264	3513	777
118265	3513	782
118266	3513	787
118267	3513	789
118268	3513	791
118269	3513	794
118270	3513	808
118271	3513	811
118272	3513	818
118273	3513	821
118274	3513	827
118275	3513	829
118276	3513	835
118277	3513	840
118278	3513	844
118279	3513	847
118280	3513	850
118281	3513	853
118282	3513	857
118283	3513	860
118284	3513	871
118285	3513	872
118286	3513	874
118287	3514	733
118288	3514	734
118289	3514	740
118290	3514	744
118291	3514	747
118292	3514	749
118293	3514	753
118294	3514	760
118295	3514	761
118296	3514	764
118297	3514	768
118298	3514	772
118299	3514	777
118300	3514	784
118301	3514	787
118302	3514	789
118303	3514	792
118304	3514	794
118305	3514	808
118306	3514	811
118307	3514	818
118308	3514	821
118309	3514	828
118310	3514	833
118311	3514	835
118312	3514	841
118313	3514	844
118314	3514	848
118315	3514	850
118316	3514	854
118317	3514	856
118318	3514	860
118319	3514	871
118320	3514	872
118321	3514	874
118322	3515	732
118323	3515	734
118324	3515	740
118325	3515	743
118326	3515	745
118327	3515	748
118328	3515	752
118329	3515	760
118330	3515	761
118331	3515	764
118332	3515	768
118333	3515	772
118334	3515	777
118335	3515	782
118336	3515	787
118337	3515	789
118338	3515	793
118339	3515	794
118340	3515	806
118341	3515	811
118342	3515	819
118343	3515	823
118344	3515	827
118345	3515	832
118346	3515	835
118347	3515	841
118348	3515	845
118349	3515	847
118350	3515	851
118351	3515	853
118352	3515	858
118353	3515	860
118354	3515	871
118355	3515	873
118356	3515	874
118357	3516	732
118358	3516	734
118359	3516	740
118360	3516	744
118361	3516	747
118362	3516	748
118363	3516	752
118364	3516	760
118365	3516	761
118366	3516	764
118367	3516	768
118368	3516	772
118369	3516	777
118370	3516	783
118371	3516	787
118372	3516	789
118373	3516	792
118374	3516	794
118375	3516	807
118376	3516	811
118377	3516	819
118378	3516	823
118379	3516	826
118380	3516	833
118381	3516	835
118382	3516	840
118383	3516	844
118384	3516	847
118385	3516	850
118386	3516	853
118387	3516	857
118388	3516	860
118389	3516	871
118390	3516	874
118391	3517	732
118392	3517	734
118393	3517	740
118394	3517	744
118395	3517	746
118396	3517	749
118397	3517	753
118398	3517	758
118399	3517	761
118400	3517	764
118401	3517	768
118402	3517	775
118403	3517	781
118404	3517	783
118405	3517	787
118406	3517	789
118407	3517	792
118408	3517	794
118409	3517	806
118410	3517	816
118411	3517	819
118412	3517	822
118413	3517	826
118414	3517	831
118415	3517	835
118416	3517	841
118417	3517	845
118418	3517	846
118419	3517	851
118420	3517	852
118421	3517	859
118422	3517	860
118423	3517	871
118424	3517	873
118425	3517	874
118426	3518	733
118427	3518	734
118428	3518	740
118429	3518	744
118430	3518	746
118431	3518	748
118432	3518	753
118433	3518	760
118434	3518	761
118435	3518	764
118436	3518	768
118437	3518	772
118438	3518	777
118439	3518	783
118440	3518	787
118441	3518	789
118442	3518	793
118443	3518	795
118444	3518	797
118445	3518	803
118446	3518	806
118447	3518	811
118448	3518	819
118449	3518	823
118450	3518	828
118451	3518	832
118452	3518	834
118453	3518	841
118454	3518	844
118455	3518	847
118456	3518	850
118457	3518	853
118458	3518	857
118459	3518	860
118460	3518	871
118461	3518	872
118462	3518	874
118463	3519	733
118464	3519	734
118465	3519	740
118466	3519	744
118467	3519	745
118468	3519	749
118469	3519	753
118470	3519	760
118471	3519	761
118472	3519	764
118473	3519	768
118474	3519	772
118475	3519	777
118476	3519	783
118477	3519	787
118478	3519	789
118479	3519	793
118480	3519	795
118481	3519	798
118482	3519	801
118483	3519	807
118484	3519	811
118485	3519	819
118486	3519	823
118487	3519	828
118488	3519	833
118489	3519	835
118490	3519	841
118491	3519	844
118492	3519	847
118493	3519	850
118494	3519	853
118495	3519	857
118496	3519	860
118497	3519	871
118498	3519	872
118499	3519	874
118500	3520	732
118501	3520	734
118502	3520	740
118503	3520	743
118504	3520	747
118505	3520	749
118506	3520	754
118507	3520	756
118508	3520	761
118509	3520	764
118510	3520	770
118511	3520	775
118512	3520	777
118513	3520	783
118514	3520	787
118515	3520	789
118516	3520	791
118517	3520	794
118518	3520	809
118519	3520	814
118520	3520	818
118521	3520	821
118522	3520	826
118523	3520	829
118524	3520	836
118525	3520	841
118526	3520	844
118527	3520	847
118528	3520	851
118529	3520	854
118530	3520	857
118531	3520	860
118532	3520	871
118533	3520	872
118534	3520	874
118535	3521	732
118536	3521	734
118537	3521	740
118538	3521	744
118539	3521	747
118540	3521	750
118541	3521	754
118542	3521	758
118543	3521	761
118544	3521	764
118545	3521	768
118546	3521	772
118547	3521	777
118548	3521	785
118549	3521	787
118550	3521	789
118551	3521	792
118552	3521	794
118553	3521	808
118554	3521	811
118555	3521	819
118556	3521	822
118557	3521	827
118558	3521	831
118559	3521	835
118560	3521	842
118561	3521	845
118562	3521	848
118563	3521	851
118564	3521	854
118565	3521	857
118566	3521	860
118567	3521	871
118568	3521	872
118569	3521	874
118570	3522	732
118571	3522	734
118572	3522	740
118573	3522	743
118574	3522	746
118575	3522	749
118576	3522	753
118577	3522	758
118578	3522	761
118579	3522	764
118580	3522	768
118581	3522	772
118582	3522	777
118583	3522	784
118584	3522	787
118585	3522	789
118586	3522	792
118587	3522	794
118588	3522	809
118589	3522	811
118590	3522	819
118591	3522	822
118592	3522	828
118593	3522	835
118594	3522	842
118595	3522	845
118596	3522	848
118597	3522	851
118598	3522	854
118599	3522	856
118600	3522	860
118601	3522	871
118602	3522	872
118603	3522	874
118604	3523	733
118605	3523	734
118606	3523	740
118607	3523	743
118608	3523	747
118609	3523	749
118610	3523	753
118611	3523	760
118612	3523	761
118613	3523	764
118614	3523	768
118615	3523	772
118616	3523	777
118617	3523	782
118618	3523	787
118619	3523	789
118620	3523	792
118621	3523	794
118622	3523	806
118623	3523	811
118624	3523	818
118625	3523	822
118626	3523	826
118627	3523	833
118628	3523	835
118629	3523	841
118630	3523	844
118631	3523	847
118632	3523	850
118633	3523	853
118634	3523	856
118635	3523	860
118636	3523	871
118637	3523	872
118638	3523	874
118639	3524	732
118640	3524	734
118641	3524	740
118642	3524	743
118643	3524	746
118644	3524	749
118645	3524	754
118646	3524	758
118647	3524	761
118648	3524	764
118649	3524	768
118650	3524	772
118651	3524	777
118652	3524	783
118653	3524	787
118654	3524	789
118655	3524	793
118656	3524	794
118657	3524	806
118658	3524	811
118659	3524	819
118660	3524	822
118661	3524	828
118662	3524	830
118663	3524	834
118664	3524	840
118665	3524	845
118666	3524	846
118667	3524	851
118668	3524	852
118669	3524	859
118670	3524	860
118671	3524	871
118672	3524	872
118673	3524	874
118674	3525	732
118675	3525	734
118676	3525	740
118677	3525	743
118678	3525	747
118679	3525	749
118680	3525	753
118681	3525	759
118682	3525	761
118683	3525	764
118684	3525	769
118685	3525	775
118686	3525	777
118687	3525	784
118688	3525	787
118689	3525	789
118690	3525	792
118691	3525	794
118692	3525	809
118693	3525	814
118694	3525	818
118695	3525	821
118696	3525	827
118697	3525	832
118698	3525	835
118699	3525	841
118700	3525	844
118701	3525	848
118702	3525	850
118703	3525	854
118704	3525	856
118705	3525	860
118706	3525	871
118707	3525	873
118708	3525	874
118709	3526	732
118710	3526	734
118711	3526	740
118712	3526	743
118713	3526	746
118714	3526	749
118715	3526	754
118716	3526	757
118717	3526	761
118718	3526	764
118719	3526	768
118720	3526	772
118721	3526	777
118722	3526	784
118723	3526	787
118724	3526	789
118725	3526	792
118726	3526	794
118727	3526	808
118728	3526	811
118729	3526	819
118730	3526	823
118731	3526	828
118732	3526	830
118733	3526	835
118734	3526	840
118735	3526	844
118736	3526	847
118737	3526	850
118738	3526	853
118739	3526	857
118740	3526	868
118741	3526	871
118742	3526	872
118743	3526	876
118744	3527	732
118745	3527	734
118746	3527	740
118747	3527	744
118748	3527	746
118749	3527	750
118750	3527	754
118751	3527	759
118752	3527	761
118753	3527	764
118754	3527	768
118755	3527	772
118756	3527	777
118757	3527	784
118758	3527	787
118759	3527	789
118760	3527	792
118761	3527	794
118762	3527	809
118763	3527	811
118764	3527	819
118765	3527	822
118766	3527	827
118767	3527	832
118768	3527	835
118769	3527	841
118770	3527	845
118771	3527	847
118772	3527	851
118773	3527	853
118774	3527	857
118775	3527	860
118776	3527	871
118777	3527	872
118778	3527	874
118779	3528	733
118780	3528	734
118781	3528	740
118782	3528	743
118783	3528	745
118784	3528	749
118785	3528	754
118786	3528	757
118787	3528	761
118788	3528	764
118789	3528	768
118790	3528	772
118791	3528	777
118792	3528	782
118793	3528	787
118794	3528	789
118795	3528	792
118796	3528	795
118797	3528	800
118798	3528	804
118799	3528	809
118800	3528	811
118801	3528	819
118802	3528	822
118803	3528	828
118804	3528	831
118805	3528	835
118806	3528	841
118807	3528	843
118808	3528	847
118809	3528	849
118810	3528	853
118811	3528	856
118812	3528	860
118813	3528	871
118814	3528	874
118815	3529	733
118816	3529	735
118817	3529	737
118818	3529	741
118819	3529	744
118820	3529	746
118821	3529	749
118822	3529	754
118823	3529	759
118824	3529	761
118825	3529	766
118826	3529	771
118827	3529	776
118828	3529	781
118829	3529	785
118830	3529	788
118831	3529	790
118832	3529	792
118833	3529	794
118834	3529	808
118835	3529	815
118836	3529	819
118837	3529	823
118838	3529	828
118839	3529	831
118840	3529	838
118841	3529	841
118842	3529	845
118843	3529	848
118844	3529	851
118845	3529	854
118846	3529	856
118847	3529	860
118848	3529	871
118849	3529	874
118850	3530	732
118851	3530	735
118852	3530	737
118853	3530	741
118854	3530	744
118855	3530	747
118856	3530	749
118857	3530	755
118858	3530	759
118859	3530	761
118860	3530	767
118861	3530	771
118862	3530	776
118863	3530	781
118864	3530	784
118865	3530	788
118866	3530	790
118867	3530	792
118868	3530	794
118869	3530	808
118870	3530	815
118871	3530	819
118872	3530	822
118873	3530	828
118874	3530	832
118875	3530	838
118876	3530	841
118877	3530	844
118878	3530	848
118879	3530	850
118880	3530	854
118881	3530	856
118882	3530	860
118883	3530	871
118884	3530	873
118885	3530	874
118886	3531	732
118887	3531	734
118888	3531	740
118889	3531	744
118890	3531	747
118891	3531	748
118892	3531	752
118893	3531	758
118894	3531	761
118895	3531	764
118896	3531	768
118897	3531	772
118898	3531	777
118899	3531	783
118900	3531	787
118901	3531	789
118902	3531	792
118903	3531	794
118904	3531	808
118905	3531	811
118906	3531	818
118907	3531	822
118908	3531	826
118909	3531	832
118910	3531	835
118911	3531	841
118912	3531	844
118913	3531	847
118914	3531	850
118915	3531	853
118916	3531	856
118917	3531	860
118918	3531	871
118919	3531	872
118920	3531	874
118921	3532	731
118922	3532	734
118923	3532	740
118924	3532	744
118925	3532	746
118926	3532	749
118927	3532	754
118928	3532	758
118929	3532	761
118930	3532	764
118931	3532	768
118932	3532	772
118933	3532	777
118934	3532	786
118935	3532	787
118936	3532	789
118937	3532	792
118938	3532	795
118939	3532	797
118940	3532	802
118941	3532	808
118942	3532	811
118943	3532	819
118944	3532	823
118945	3532	827
118946	3532	831
118947	3532	835
118948	3532	842
118949	3532	845
118950	3532	848
118951	3532	851
118952	3532	854
118953	3532	857
118954	3532	860
118955	3532	871
118956	3532	872
118957	3532	874
118958	3533	732
118959	3533	734
118960	3533	740
118961	3533	744
118962	3533	747
118963	3533	748
118964	3533	753
118965	3533	759
118966	3533	761
118967	3533	764
118968	3533	768
118969	3533	772
118970	3533	777
118971	3533	784
118972	3533	787
118973	3533	789
118974	3533	792
118975	3533	794
118976	3533	808
118977	3533	811
118978	3533	819
118979	3533	822
118980	3533	827
118981	3533	832
118982	3533	835
118983	3533	842
118984	3533	845
118985	3533	847
118986	3533	851
118987	3533	854
118988	3533	857
118989	3533	860
118990	3533	871
118991	3533	872
118992	3533	874
118993	3534	732
118994	3534	734
118995	3534	740
118996	3534	743
118997	3534	745
118998	3534	748
118999	3534	753
119000	3534	759
119001	3534	761
119002	3534	764
119003	3534	768
119004	3534	772
119005	3534	777
119006	3534	784
119007	3534	787
119008	3534	789
119009	3534	792
119010	3534	795
119011	3534	798
119012	3534	804
119013	3534	807
119014	3534	811
119015	3534	818
119016	3534	823
119017	3534	828
119018	3534	832
119019	3534	835
119020	3534	841
119021	3534	843
119022	3534	847
119023	3534	849
119024	3534	853
119025	3534	856
119026	3534	860
119027	3534	871
119028	3534	872
119029	3534	874
119030	3535	731
119031	3535	734
119032	3535	740
119033	3535	744
119034	3535	746
119035	3535	749
119036	3535	755
119037	3535	761
119038	3535	764
119039	3535	768
119040	3535	772
119041	3535	777
119042	3535	784
119043	3535	787
119044	3535	789
119045	3535	792
119046	3535	794
119047	3535	806
119048	3535	811
119049	3535	819
119050	3535	823
119051	3535	827
119052	3535	830
119053	3535	835
119054	3535	841
119055	3535	845
119056	3535	848
119057	3535	851
119058	3535	853
119059	3535	858
119060	3535	860
119061	3535	871
119062	3535	872
119063	3535	874
119064	3536	732
119065	3536	734
119066	3536	740
119067	3536	744
119068	3536	746
119069	3536	748
119070	3536	753
119071	3536	757
119072	3536	761
119073	3536	764
119074	3536	768
119075	3536	772
119076	3536	777
119077	3536	783
119078	3536	787
119079	3536	789
119080	3536	793
119081	3536	794
119082	3536	806
119083	3536	811
119084	3536	818
119085	3536	822
119086	3536	827
119087	3536	830
119088	3536	835
119089	3536	840
119090	3536	845
119091	3536	846
119092	3536	851
119093	3536	852
119094	3536	859
119095	3536	860
119096	3536	871
119097	3536	873
119098	3536	874
119099	3537	732
119100	3537	734
119101	3537	740
119102	3537	744
119103	3537	746
119104	3537	750
119105	3537	754
119106	3537	759
119107	3537	761
119108	3537	764
119109	3537	768
119110	3537	772
119111	3537	777
119112	3537	784
119113	3537	787
119114	3537	789
119115	3537	792
119116	3537	794
119117	3537	808
119118	3537	811
119119	3537	818
119120	3537	822
119121	3537	828
119122	3537	832
119123	3537	835
119124	3537	841
119125	3537	845
119126	3537	847
119127	3537	851
119128	3537	853
119129	3537	858
119130	3537	860
119131	3537	871
119132	3537	872
119133	3537	874
119134	3538	732
119135	3538	734
119136	3538	740
119137	3538	743
119138	3538	746
119139	3538	749
119140	3538	753
119141	3538	760
119142	3538	761
119143	3538	764
119144	3538	768
119145	3538	772
119146	3538	777
119147	3538	784
119148	3538	787
119149	3538	789
119150	3538	792
119151	3538	794
119152	3538	808
119153	3538	811
119154	3538	818
119155	3538	821
119156	3538	827
119157	3538	831
119158	3538	835
119159	3538	841
119160	3538	844
119161	3538	847
119162	3538	850
119163	3538	853
119164	3538	857
119165	3538	860
119166	3538	871
119167	3538	872
119168	3538	874
119169	3539	732
119170	3539	734
119171	3539	740
119172	3539	742
119173	3539	747
119174	3539	748
119175	3539	753
119176	3539	760
119177	3539	761
119178	3539	764
119179	3539	768
119180	3539	772
119181	3539	777
119182	3539	783
119183	3539	787
119184	3539	789
119185	3539	791
119186	3539	794
119187	3539	807
119188	3539	811
119189	3539	818
119190	3539	821
119191	3539	828
119192	3539	831
119193	3539	835
119194	3539	841
119195	3539	843
119196	3539	847
119197	3539	849
119198	3539	854
119199	3539	856
119200	3539	860
119201	3539	871
119202	3539	872
119203	3539	874
119204	3540	731
119205	3540	734
119206	3540	740
119207	3540	743
119208	3540	745
119209	3540	748
119210	3540	752
119211	3540	759
119212	3540	761
119213	3540	764
119214	3540	768
119215	3540	772
119216	3540	777
119217	3540	783
119218	3540	787
119219	3540	789
119220	3540	793
119221	3540	794
119222	3540	806
119223	3540	811
119224	3540	819
119225	3540	823
119226	3540	828
119227	3540	832
119228	3540	835
119229	3540	840
119230	3540	845
119231	3540	846
119232	3540	851
119233	3540	852
119234	3540	859
119235	3540	860
119236	3540	871
119237	3540	874
119238	3541	732
119239	3541	734
119240	3541	740
119241	3541	744
119242	3541	746
119243	3541	749
119244	3541	754
119245	3541	760
119246	3541	761
119247	3541	764
119248	3541	768
119249	3541	772
119250	3541	777
119251	3541	785
119252	3541	787
119253	3541	789
119254	3541	792
119255	3541	794
119256	3541	808
119257	3541	811
119258	3541	819
119259	3541	822
119260	3541	828
119261	3541	831
119262	3541	835
119263	3541	841
119264	3541	845
119265	3541	847
119266	3541	851
119267	3541	853
119268	3541	858
119269	3541	860
119270	3541	871
119271	3541	872
119272	3541	874
119273	3542	732
119274	3542	734
119275	3542	740
119276	3542	742
119277	3542	746
119278	3542	748
119279	3542	752
119280	3542	760
119281	3542	761
119282	3542	764
119283	3542	768
119284	3542	772
119285	3542	777
119286	3542	783
119287	3542	787
119288	3542	789
119289	3542	792
119290	3542	794
119291	3542	808
119292	3542	811
119293	3542	818
119294	3542	823
119295	3542	828
119296	3542	831
119297	3542	835
119298	3542	840
119299	3542	843
119300	3542	847
119301	3542	849
119302	3542	853
119303	3542	856
119304	3542	860
119305	3542	871
119306	3542	872
119307	3542	874
119308	3543	732
119309	3543	734
119310	3543	740
119311	3543	744
119312	3543	747
119313	3543	749
119314	3543	754
119315	3543	758
119316	3543	761
119317	3543	764
119318	3543	769
119319	3543	774
119320	3543	777
119321	3543	784
119322	3543	787
119323	3543	789
119324	3543	792
119325	3543	794
119326	3543	808
119327	3543	814
119328	3543	818
119329	3543	822
119330	3543	826
119331	3543	832
119332	3543	836
119333	3543	841
119334	3543	845
119335	3543	847
119336	3543	851
119337	3543	853
119338	3543	857
119339	3543	860
119340	3543	871
119341	3543	872
119342	3543	874
119343	3544	732
119344	3544	734
119345	3544	740
119346	3544	743
119347	3544	746
119348	3544	749
119349	3544	753
119350	3544	758
119351	3544	761
119352	3544	764
119353	3544	768
119354	3544	772
119355	3544	777
119356	3544	784
119357	3544	787
119358	3544	789
119359	3544	792
119360	3544	794
119361	3544	806
119362	3544	811
119363	3544	819
119364	3544	823
119365	3544	826
119366	3544	831
119367	3544	835
119368	3544	841
119369	3544	844
119370	3544	847
119371	3544	850
119372	3544	853
119373	3544	857
119374	3544	860
119375	3544	871
119376	3544	872
119377	3544	874
119378	3545	732
119379	3545	734
119380	3545	740
119381	3545	743
119382	3545	746
119383	3545	749
119384	3545	753
119385	3545	758
119386	3545	761
119387	3545	764
119388	3545	768
119389	3545	772
119390	3545	777
119391	3545	783
119392	3545	787
119393	3545	789
119394	3545	791
119395	3545	794
119396	3545	808
119397	3545	811
119398	3545	818
119399	3545	821
119400	3545	827
119401	3545	832
119402	3545	835
119403	3545	841
119404	3545	843
119405	3545	847
119406	3545	849
119407	3545	854
119408	3545	856
119409	3545	860
119410	3545	871
119411	3545	872
119412	3545	874
119413	3546	732
119414	3546	734
119415	3546	740
119416	3546	744
119417	3546	746
119418	3546	749
119419	3546	753
119420	3546	758
119421	3546	761
119422	3546	764
119423	3546	768
119424	3546	775
119425	3546	777
119426	3546	782
119427	3546	787
119428	3546	789
119429	3546	793
119430	3546	795
119431	3546	797
119432	3546	803
119433	3546	806
119434	3546	814
119435	3546	819
119436	3546	823
119437	3546	825
119438	3546	831
119439	3546	835
119440	3546	840
119441	3546	845
119442	3546	846
119443	3546	851
119444	3546	852
119445	3546	859
119446	3546	860
119447	3546	871
119448	3546	872
119449	3546	874
119450	3547	732
119451	3547	734
119452	3547	740
119453	3547	743
119454	3547	747
119455	3547	749
119456	3547	753
119457	3547	758
119458	3547	761
119459	3547	764
119460	3547	768
119461	3547	772
119462	3547	777
119463	3547	784
119464	3547	787
119465	3547	789
119466	3547	792
119467	3547	794
119468	3547	809
119469	3547	811
119470	3547	818
119471	3547	821
119472	3547	827
119473	3547	832
119474	3547	835
119475	3547	841
119476	3547	844
119477	3547	847
119478	3547	850
119479	3547	853
119480	3547	857
119481	3547	860
119482	3547	871
119483	3547	872
119484	3547	874
119485	3548	731
119486	3548	734
119487	3548	740
119488	3548	744
119489	3548	746
119490	3548	749
119491	3548	754
119492	3548	760
119493	3548	761
119494	3548	764
119495	3548	768
119496	3548	775
119497	3548	777
119498	3548	782
119499	3548	787
119500	3548	789
119501	3548	792
119502	3548	795
119503	3548	797
119504	3548	801
119505	3548	806
119506	3548	815
119507	3548	819
119508	3548	823
119509	3548	828
119510	3548	833
119511	3548	835
119512	3548	841
119513	3548	845
119514	3548	846
119515	3548	851
119516	3548	852
119517	3548	859
119518	3548	860
119519	3548	871
119520	3548	873
119521	3548	874
119522	3549	731
119523	3549	734
119524	3549	740
119525	3549	744
119526	3549	747
119527	3549	749
119528	3549	754
119529	3549	760
119530	3549	764
119531	3549	768
119532	3549	776
119533	3549	781
119534	3549	786
119535	3549	787
119536	3549	789
119537	3549	793
119538	3549	794
119539	3549	809
119540	3549	815
119541	3549	819
119542	3549	823
119543	3549	828
119544	3549	832
119545	3549	835
119546	3549	842
119547	3549	845
119548	3549	848
119549	3549	851
119550	3549	854
119551	3549	857
119552	3549	860
119553	3549	871
119554	3549	873
119555	3549	874
119556	3550	732
119557	3550	734
119558	3550	740
119559	3550	744
119560	3550	746
119561	3550	748
119562	3550	754
119563	3550	758
119564	3550	761
119565	3550	764
119566	3550	768
119567	3550	775
119568	3550	784
119569	3550	787
119570	3550	789
119571	3550	793
119572	3550	794
119573	3550	806
119574	3550	815
119575	3550	819
119576	3550	823
119577	3550	826
119578	3550	831
119579	3550	835
119580	3550	841
119581	3550	845
119582	3550	846
119583	3550	851
119584	3550	852
119585	3550	859
119586	3550	860
119587	3550	871
119588	3550	872
119589	3550	874
119590	3551	732
119591	3551	734
119592	3551	740
119593	3551	743
119594	3551	746
119595	3551	749
119596	3551	753
119597	3551	759
119598	3551	761
119599	3551	764
119600	3551	768
119601	3551	772
119602	3551	777
119603	3551	784
119604	3551	787
119605	3551	789
119606	3551	792
119607	3551	794
119608	3551	809
119609	3551	811
119610	3551	818
119611	3551	821
119612	3551	827
119613	3551	832
119614	3551	835
119615	3551	840
119616	3551	845
119617	3551	846
119618	3551	851
119619	3551	852
119620	3551	858
119621	3551	860
119622	3551	871
119623	3551	872
119624	3551	874
119625	3552	732
119626	3552	734
119627	3552	740
119628	3552	743
119629	3552	746
119630	3552	748
119631	3552	753
119632	3552	759
119633	3552	761
119634	3552	764
119635	3552	768
119636	3552	772
119637	3552	777
119638	3552	783
119639	3552	787
119640	3552	789
119641	3552	792
119642	3552	794
119643	3552	808
119644	3552	811
119645	3552	818
119646	3552	821
119647	3552	827
119648	3552	832
119649	3552	835
119650	3552	840
119651	3552	845
119652	3552	846
119653	3552	851
119654	3552	852
119655	3552	859
119656	3552	860
119657	3552	871
119658	3552	873
119659	3552	874
119660	3553	732
119661	3553	734
119662	3553	740
119663	3553	743
119664	3553	746
119665	3553	748
119666	3553	753
119667	3553	757
119668	3553	761
119669	3553	764
119670	3553	768
119671	3553	774
119672	3553	777
119673	3553	783
119674	3553	787
119675	3553	789
119676	3553	792
119677	3553	794
119678	3553	808
119679	3553	814
119680	3553	818
119681	3553	822
119682	3553	827
119683	3553	830
119684	3553	836
119685	3553	841
119686	3553	844
119687	3553	847
119688	3553	850
119689	3553	854
119690	3553	856
119691	3553	860
119692	3553	871
119693	3553	873
119694	3553	874
119695	3554	732
119696	3554	734
119697	3554	740
119698	3554	743
119699	3554	745
119700	3554	749
119701	3554	753
119702	3554	758
119703	3554	761
119704	3554	764
119705	3554	768
119706	3554	772
119707	3554	777
119708	3554	783
119709	3554	787
119710	3554	789
119711	3554	792
119712	3554	794
119713	3554	808
119714	3554	811
119715	3554	819
119716	3554	822
119717	3554	827
119718	3554	830
119719	3554	835
119720	3554	841
119721	3554	843
119722	3554	847
119723	3554	849
119724	3554	853
119725	3554	856
119726	3554	860
119727	3554	871
119728	3554	872
119729	3554	874
119730	3555	731
119731	3555	734
119732	3555	740
119733	3555	743
119734	3555	746
119735	3555	749
119736	3555	753
119737	3555	758
119738	3555	761
119739	3555	764
119740	3555	768
119741	3555	772
119742	3555	777
119743	3555	783
119744	3555	787
119745	3555	789
119746	3555	792
119747	3555	794
119748	3555	808
119749	3555	811
119750	3555	818
119751	3555	822
119752	3555	828
119753	3555	830
119754	3555	835
119755	3555	842
119756	3555	844
119757	3555	848
119758	3555	850
119759	3555	854
119760	3555	856
119761	3555	860
119762	3555	871
119763	3555	872
119764	3555	874
119765	3556	732
119766	3556	734
119767	3556	740
119768	3556	743
119769	3556	745
119770	3556	748
119771	3556	752
119772	3556	757
119773	3556	761
119774	3556	764
119775	3556	768
119776	3556	772
119777	3556	777
119778	3556	782
119779	3556	787
119780	3556	789
119781	3556	793
119782	3556	795
119783	3556	797
119784	3556	801
119785	3556	806
119786	3556	811
119787	3556	819
119788	3556	822
119789	3556	827
119790	3556	831
119791	3556	835
119792	3556	840
119793	3556	845
119794	3556	846
119795	3556	851
119796	3556	852
119797	3556	859
119798	3556	860
119799	3556	871
119800	3556	873
119801	3556	874
119802	3557	731
119803	3557	734
119804	3557	740
119805	3557	743
119806	3557	746
119807	3557	750
119808	3557	754
119809	3557	758
119810	3557	761
119811	3557	764
119812	3557	768
119813	3557	772
119814	3557	777
119815	3557	784
119816	3557	787
119817	3557	789
119818	3557	793
119819	3557	794
119820	3557	809
119821	3557	811
119822	3557	819
119823	3557	822
119824	3557	828
119825	3557	831
119826	3557	835
119827	3557	841
119828	3557	845
119829	3557	847
119830	3557	851
119831	3557	853
119832	3557	857
119833	3557	860
119834	3557	871
119835	3557	872
119836	3557	874
119837	3558	732
119838	3558	734
119839	3558	740
119840	3558	742
119841	3558	745
119842	3558	749
119843	3558	754
119844	3558	757
119845	3558	761
119846	3558	764
119847	3558	768
119848	3558	772
119849	3558	777
119850	3558	784
119851	3558	787
119852	3558	789
119853	3558	791
119854	3558	794
119855	3558	807
119856	3558	811
119857	3558	818
119858	3558	821
119859	3558	827
119860	3558	830
119861	3558	835
119862	3558	841
119863	3558	845
119864	3558	847
119865	3558	851
119866	3558	853
119867	3558	857
119868	3558	860
119869	3558	871
119870	3558	872
119871	3558	874
119872	3559	732
119873	3559	734
119874	3559	740
119875	3559	744
119876	3559	746
119877	3559	750
119878	3559	754
119879	3559	758
119880	3559	761
119881	3559	764
119882	3559	775
119883	3559	777
119884	3559	783
119885	3559	787
119886	3559	789
119887	3559	792
119888	3559	794
119889	3559	806
119890	3559	814
119891	3559	819
119892	3559	822
119893	3559	826
119894	3559	830
119895	3559	835
119896	3559	840
119897	3559	845
119898	3559	846
119899	3559	851
119900	3559	852
119901	3559	859
119902	3559	860
119903	3559	871
119904	3559	873
119905	3559	874
119906	3560	731
119907	3560	734
119908	3560	740
119909	3560	743
119910	3560	746
119911	3560	749
119912	3560	754
119913	3560	759
119914	3560	761
119915	3560	764
119916	3560	768
119917	3560	772
119918	3560	777
119919	3560	784
119920	3560	787
119921	3560	789
119922	3560	792
119923	3560	795
119924	3560	796
119925	3560	801
119926	3560	809
119927	3560	811
119928	3560	818
119929	3560	821
119930	3560	826
119931	3560	832
119932	3560	835
119933	3560	841
119934	3560	844
119935	3560	847
119936	3560	851
119937	3560	853
119938	3560	857
119939	3560	860
119940	3560	871
119941	3560	874
119942	3561	732
119943	3561	734
119944	3561	740
119945	3561	743
119946	3561	746
119947	3561	749
119948	3561	753
119949	3561	758
119950	3561	761
119951	3561	764
119952	3561	768
119953	3561	772
119954	3561	777
119955	3561	783
119956	3561	787
119957	3561	789
119958	3561	792
119959	3561	794
119960	3561	809
119961	3561	811
119962	3561	818
119963	3561	822
119964	3561	828
119965	3561	830
119966	3561	835
119967	3561	841
119968	3561	845
119969	3561	847
119970	3561	851
119971	3561	853
119972	3561	857
119973	3561	860
119974	3561	871
119975	3561	874
119976	3562	732
119977	3562	734
119978	3562	740
119979	3562	744
119980	3562	746
119981	3562	749
119982	3562	754
119983	3562	758
119984	3562	761
119985	3562	764
119986	3562	768
119987	3562	772
119988	3562	777
119989	3562	783
119990	3562	787
119991	3562	789
119992	3562	792
119993	3562	794
119994	3562	808
119995	3562	811
119996	3562	819
119997	3562	823
119998	3562	827
119999	3562	835
120000	3562	841
120001	3562	844
120002	3562	847
120003	3562	851
120004	3562	853
120005	3562	857
120006	3562	860
120007	3562	871
120008	3562	872
120009	3562	874
120010	3563	732
120011	3563	734
120012	3563	740
120013	3563	743
120014	3563	746
120015	3563	748
120016	3563	752
120017	3563	758
120018	3563	761
120019	3563	764
120020	3563	768
120021	3563	772
120022	3563	777
120023	3563	784
120024	3563	787
120025	3563	789
120026	3563	792
120027	3563	794
120028	3563	809
120029	3563	811
120030	3563	819
120031	3563	823
120032	3563	828
120033	3563	832
120034	3563	835
120035	3563	841
120036	3563	843
120037	3563	847
120038	3563	849
120039	3563	854
120040	3563	856
120041	3563	860
120042	3563	871
120043	3563	874
120044	3564	732
120045	3564	734
120046	3564	740
120047	3564	744
120048	3564	745
120049	3564	748
120050	3564	752
120051	3564	758
120052	3564	761
120053	3564	764
120054	3564	768
120055	3564	774
120056	3564	780
120057	3564	782
120058	3564	787
120059	3564	789
120060	3564	792
120061	3564	794
120062	3564	806
120063	3564	815
120064	3564	818
120065	3564	822
120066	3564	826
120067	3564	831
120068	3564	841
120069	3564	845
120070	3564	846
120071	3564	851
120072	3564	852
120073	3564	859
120074	3564	860
120075	3564	871
120076	3564	876
120077	3565	732
120078	3565	734
120079	3565	740
120080	3565	744
120081	3565	746
120082	3565	748
120083	3565	752
120084	3565	759
120085	3565	761
120086	3565	764
120087	3565	768
120088	3565	772
120089	3565	777
120090	3565	782
120091	3565	787
120092	3565	789
120093	3565	792
120094	3565	794
120095	3565	808
120096	3565	811
120097	3565	819
120098	3565	822
120099	3565	827
120100	3565	832
120101	3565	835
120102	3565	842
120103	3565	845
120104	3565	848
120105	3565	851
120106	3565	854
120107	3565	857
120108	3565	860
120109	3565	871
120110	3565	874
120111	3566	732
120112	3566	734
120113	3566	740
120114	3566	744
120115	3566	746
120116	3566	749
120117	3566	753
120118	3566	759
120119	3566	761
120120	3566	765
120121	3566	769
120122	3566	774
120123	3566	777
120124	3566	784
120125	3566	787
120126	3566	789
120127	3566	792
120128	3566	795
120129	3566	797
120130	3566	801
120131	3566	808
120132	3566	814
120133	3566	818
120134	3566	822
120135	3566	827
120136	3566	831
120137	3566	836
120138	3566	842
120139	3566	845
120140	3566	848
120141	3566	851
120142	3566	854
120143	3566	857
120144	3566	860
120145	3566	871
120146	3566	872
120147	3566	874
120148	3567	732
120149	3567	734
120150	3567	740
120151	3567	744
120152	3567	746
120153	3567	749
120154	3567	754
120155	3567	760
120156	3567	761
120157	3567	764
120158	3567	768
120159	3567	773
120160	3567	777
120161	3567	782
120162	3567	787
120163	3567	789
120164	3567	792
120165	3567	794
120166	3567	806
120167	3567	811
120168	3567	818
120169	3567	823
120170	3567	828
120171	3567	832
120172	3567	835
120173	3567	840
120174	3567	845
120175	3567	846
120176	3567	851
120177	3567	852
120178	3567	858
120179	3567	860
120180	3568	731
120181	3568	734
120182	3568	740
120183	3568	743
120184	3568	746
120185	3568	749
120186	3568	753
120187	3568	760
120188	3568	761
120189	3568	764
120190	3568	768
120191	3568	772
120192	3568	777
120193	3568	782
120194	3568	787
120195	3568	789
120196	3568	793
120197	3568	794
120198	3568	806
120199	3568	811
120200	3568	819
120201	3568	822
120202	3568	827
120203	3568	833
120204	3568	835
120205	3568	840
120206	3568	845
120207	3568	846
120208	3568	851
120209	3568	852
120210	3568	858
120211	3568	860
120212	3568	871
120213	3568	874
120214	3569	732
120215	3569	734
120216	3569	740
120217	3569	743
120218	3569	746
120219	3569	749
120220	3569	753
120221	3569	758
120222	3569	761
120223	3569	764
120224	3569	768
120225	3569	772
120226	3569	777
120227	3569	784
120228	3569	787
120229	3569	789
120230	3569	792
120231	3569	794
120232	3569	809
120233	3569	811
120234	3569	818
120235	3569	822
120236	3569	828
120237	3569	832
120238	3569	835
120239	3569	841
120240	3569	844
120241	3569	847
120242	3569	850
120243	3569	853
120244	3569	856
120245	3569	860
120246	3570	731
120247	3570	734
120248	3570	740
120249	3570	744
120250	3570	746
120251	3570	750
120252	3570	754
120253	3570	758
120254	3570	761
120255	3570	764
120256	3570	768
120257	3570	772
120258	3570	777
120259	3570	784
120260	3570	787
120261	3570	789
120262	3570	793
120263	3570	794
120264	3570	806
120265	3570	811
120266	3570	819
120267	3570	823
120268	3570	827
120269	3570	831
120270	3570	835
120271	3570	841
120272	3570	845
120273	3570	847
120274	3570	851
120275	3570	853
120276	3570	858
120277	3570	860
120278	3570	871
120279	3570	872
120280	3570	874
120281	3571	731
120282	3571	734
120283	3571	740
120284	3571	743
120285	3571	746
120286	3571	749
120287	3571	753
120288	3571	760
120289	3571	761
120290	3571	764
120291	3571	768
120292	3571	772
120293	3571	777
120294	3571	783
120295	3571	787
120296	3571	789
120297	3571	792
120298	3571	795
120299	3571	798
120300	3571	803
120301	3571	809
120302	3571	811
120303	3571	818
120304	3571	822
120305	3571	827
120306	3571	833
120307	3571	835
120308	3571	841
120309	3571	844
120310	3571	847
120311	3571	850
120312	3571	853
120313	3571	857
120314	3571	860
120315	3571	874
120316	3572	732
120317	3572	735
120318	3572	737
120319	3572	741
120320	3572	744
120321	3572	746
120322	3572	750
120323	3572	754
120324	3572	758
120325	3572	761
120326	3572	765
120327	3572	770
120328	3572	775
120329	3572	777
120330	3572	784
120331	3572	788
120332	3572	790
120333	3572	792
120334	3572	794
120335	3572	808
120336	3572	813
120337	3572	819
120338	3572	823
120339	3572	827
120340	3572	830
120341	3572	836
120342	3572	842
120343	3572	843
120344	3572	848
120345	3572	851
120346	3572	854
120347	3572	857
120348	3572	860
120349	3572	871
120350	3572	872
120351	3572	874
120352	3573	733
120353	3573	734
120354	3573	740
120355	3573	743
120356	3573	746
120357	3573	748
120358	3573	752
120359	3573	760
120360	3573	761
120361	3573	764
120362	3573	768
120363	3573	775
120364	3573	781
120365	3573	783
120366	3573	787
120367	3573	789
120368	3573	792
120369	3573	794
120370	3573	806
120371	3573	815
120372	3573	819
120373	3573	823
120374	3573	828
120375	3573	832
120376	3573	835
120377	3573	841
120378	3573	845
120379	3573	846
120380	3573	851
120381	3573	852
120382	3573	859
120383	3573	860
120384	3573	871
120385	3573	873
120386	3574	732
120387	3574	734
120388	3574	740
120389	3574	743
120390	3574	745
120391	3574	749
120392	3574	754
120393	3574	758
120394	3574	761
120395	3574	764
120396	3574	768
120397	3574	772
120398	3574	777
120399	3574	784
120400	3574	787
120401	3574	789
120402	3574	791
120403	3574	794
120404	3574	807
120405	3574	811
120406	3574	819
120407	3574	823
120408	3574	828
120409	3574	831
120410	3574	841
120411	3574	845
120412	3574	847
120413	3574	851
120414	3574	853
120415	3574	858
120416	3574	860
120417	3574	871
120418	3574	872
120419	3574	874
120420	3575	734
120421	3575	740
120422	3575	742
120423	3575	746
120424	3575	749
120425	3575	753
120426	3575	759
120427	3575	761
120428	3575	767
120429	3575	771
120430	3575	775
120431	3575	777
120432	3575	784
120433	3575	787
120434	3575	790
120435	3575	791
120436	3575	794
120437	3575	808
120438	3575	814
120439	3575	818
120440	3575	821
120441	3575	827
120442	3575	832
120443	3575	835
120444	3575	841
120445	3575	843
120446	3575	847
120447	3575	849
120448	3575	854
120449	3575	856
120450	3575	860
120451	3575	871
120452	3575	872
120453	3575	874
120454	3576	731
120455	3576	734
120456	3576	740
120457	3576	743
120458	3576	745
120459	3576	749
120460	3576	755
120461	3576	757
120462	3576	761
120463	3576	764
120464	3576	768
120465	3576	772
120466	3576	777
120467	3576	784
120468	3576	787
120469	3576	789
120470	3576	793
120471	3576	794
120472	3576	806
120473	3576	811
120474	3576	819
120475	3576	823
120476	3576	828
120477	3576	830
120478	3576	835
120479	3576	841
120480	3576	845
120481	3576	846
120482	3576	851
120483	3576	852
120484	3576	859
120485	3576	860
120486	3576	874
120487	3577	734
120488	3577	740
120489	3577	744
120490	3577	747
120491	3577	754
120492	3577	758
120493	3577	761
120494	3577	764
120495	3577	768
120496	3577	772
120497	3577	777
120498	3577	785
120499	3577	787
120500	3577	789
120501	3577	792
120502	3577	794
120503	3577	806
120504	3577	811
120505	3577	819
120506	3577	822
120507	3577	828
120508	3577	831
120509	3577	835
120510	3577	842
120511	3577	845
120512	3577	848
120513	3577	851
120514	3577	854
120515	3577	857
120516	3577	860
120517	3577	871
120518	3577	872
120519	3577	874
120520	3578	732
120521	3578	734
120522	3578	740
120523	3578	744
120524	3578	746
120525	3578	748
120526	3578	752
120527	3578	759
120528	3578	761
120529	3578	764
120530	3578	768
120531	3578	772
120532	3578	777
120533	3578	783
120534	3578	787
120535	3578	789
120536	3578	793
120537	3578	794
120538	3578	808
120539	3578	811
120540	3578	819
120541	3578	823
120542	3578	828
120543	3578	832
120544	3578	835
120545	3578	841
120546	3578	845
120547	3578	846
120548	3578	851
120549	3578	852
120550	3578	859
120551	3578	860
120552	3578	871
120553	3578	872
120554	3578	874
120555	3579	734
120556	3579	740
120557	3579	742
120558	3579	747
120559	3579	749
120560	3579	754
120561	3579	758
120562	3579	761
120563	3579	764
120564	3579	768
120565	3579	777
120566	3579	783
120567	3579	787
120568	3579	789
120569	3579	792
120570	3579	794
120571	3579	808
120572	3579	811
120573	3579	817
120574	3579	821
120575	3579	827
120576	3579	831
120577	3579	835
120578	3579	841
120579	3579	844
120580	3579	847
120581	3579	850
120582	3579	853
120583	3579	857
120584	3579	860
120585	3579	874
120586	3580	734
120587	3580	740
120588	3580	743
120589	3580	746
120590	3580	749
120591	3580	753
120592	3580	757
120593	3580	761
120594	3580	764
120595	3580	768
120596	3580	772
120597	3580	777
120598	3580	783
120599	3580	787
120600	3580	789
120601	3580	792
120602	3580	794
120603	3580	807
120604	3580	811
120605	3580	818
120606	3580	821
120607	3580	827
120608	3580	831
120609	3580	835
120610	3580	840
120611	3580	844
120612	3580	847
120613	3580	850
120614	3580	852
120615	3580	857
120616	3580	860
120617	3580	871
120618	3580	872
120619	3580	874
120620	3581	734
120621	3581	740
120622	3581	744
120623	3581	746
120624	3581	749
120625	3581	753
120626	3581	758
120627	3581	761
120628	3581	764
120629	3581	768
120630	3581	774
120631	3581	777
120632	3581	784
120633	3581	787
120634	3581	789
120635	3581	793
120636	3581	808
120637	3581	814
120638	3581	819
120639	3581	821
120640	3581	828
120641	3581	831
120642	3581	835
120643	3581	842
120644	3581	844
120645	3581	848
120646	3581	850
120647	3581	854
120648	3581	856
120649	3581	860
120650	3581	871
120651	3581	872
120652	3581	874
120653	3582	733
120654	3582	735
120655	3582	737
120656	3582	741
120657	3582	744
120658	3582	747
120659	3582	748
120660	3582	752
120661	3582	759
120662	3582	761
120663	3582	764
120664	3582	768
120665	3582	775
120666	3582	781
120667	3582	784
120668	3582	787
120669	3582	789
120670	3582	792
120671	3582	795
120672	3582	800
120673	3582	803
120674	3582	808
120675	3582	819
120676	3582	822
120677	3582	827
120678	3582	832
120679	3582	835
120680	3582	841
120681	3582	845
120682	3582	847
120683	3582	851
120684	3582	853
120685	3582	857
120686	3582	868
120687	3582	869
120688	3582	872
120689	3582	874
120690	3583	732
120691	3583	734
120692	3583	740
120693	3583	743
120694	3583	746
120695	3583	748
120696	3583	753
120697	3583	758
120698	3583	761
120699	3583	764
120700	3583	768
120701	3583	772
120702	3583	777
120703	3583	782
120704	3583	787
120705	3583	789
120706	3583	792
120707	3583	794
120708	3583	806
120709	3583	811
120710	3583	818
120711	3583	822
120712	3583	826
120713	3583	831
120714	3583	835
120715	3583	841
120716	3583	845
120717	3583	847
120718	3583	851
120719	3583	853
120720	3583	858
120721	3583	860
120722	3583	871
120723	3583	872
120724	3583	874
120725	3584	734
120726	3584	740
120727	3584	743
120728	3584	746
120729	3584	748
120730	3584	752
120731	3584	759
120732	3584	761
120733	3584	764
120734	3584	768
120735	3584	775
120736	3584	781
120737	3584	782
120738	3584	787
120739	3584	789
120740	3584	792
120741	3584	795
120742	3584	797
120743	3584	805
120744	3584	806
120745	3584	815
120746	3584	819
120747	3584	822
120748	3584	826
120749	3584	832
120750	3584	835
120751	3584	841
120752	3584	845
120753	3584	846
120754	3584	851
120755	3584	852
120756	3584	859
120757	3584	860
120758	3584	871
120759	3584	873
120760	3584	876
120761	3585	734
120762	3585	740
120763	3585	744
120764	3585	747
120765	3585	749
120766	3585	753
120767	3585	758
120768	3585	761
120769	3585	764
120770	3585	769
120771	3585	774
120772	3585	777
120773	3585	783
120774	3585	787
120775	3585	789
120776	3585	791
120777	3585	794
120778	3585	808
120779	3585	814
120780	3585	817
120781	3585	821
120782	3585	827
120783	3585	831
120784	3585	835
120785	3585	841
120786	3585	843
120787	3585	848
120788	3585	849
120789	3585	854
120790	3585	856
120791	3585	860
120792	3585	871
120793	3585	874
120794	3586	734
120795	3586	740
120796	3586	744
120797	3586	745
120798	3586	750
120799	3586	754
120800	3586	759
120801	3586	761
120802	3586	764
120803	3586	768
120804	3586	772
120805	3586	777
120806	3586	783
120807	3586	787
120808	3586	789
120809	3586	792
120810	3586	795
120811	3586	798
120812	3586	801
120813	3586	808
120814	3586	811
120815	3586	819
120816	3586	822
120817	3586	827
120818	3586	832
120819	3586	835
120820	3586	841
120821	3586	845
120822	3586	847
120823	3586	851
120824	3586	853
120825	3586	858
120826	3586	860
120827	3586	871
120828	3586	872
120829	3586	874
120830	3587	732
120831	3587	734
120832	3587	740
120833	3587	743
120834	3587	746
120835	3587	750
120836	3587	754
120837	3587	758
120838	3587	761
120839	3587	764
120840	3587	768
120841	3587	772
120842	3587	777
120843	3587	783
120844	3587	787
120845	3587	789
120846	3587	792
120847	3587	794
120848	3587	808
120849	3587	811
120850	3587	819
120851	3587	823
120852	3587	827
120853	3587	831
120854	3587	835
120855	3587	841
120856	3587	845
120857	3587	846
120858	3587	851
120859	3587	852
120860	3587	859
120861	3587	860
120862	3587	871
120863	3587	873
120864	3587	874
120865	3588	732
120866	3588	734
120867	3588	740
120868	3588	742
120869	3588	745
120870	3588	748
120871	3588	752
120872	3588	757
120873	3588	761
120874	3588	764
120875	3588	768
120876	3588	772
120877	3588	777
120878	3588	782
120879	3588	787
120880	3588	789
120881	3588	791
120882	3588	794
120883	3588	808
120884	3588	811
120885	3588	818
120886	3588	822
120887	3588	827
120888	3588	831
120889	3588	835
120890	3588	841
120891	3588	843
120892	3588	847
120893	3588	849
120894	3588	854
120895	3588	856
120896	3588	860
120897	3588	871
120898	3588	872
120899	3588	874
120900	3589	732
120901	3589	734
120902	3589	740
120903	3589	743
120904	3589	745
120905	3589	748
120906	3589	752
120907	3589	757
120908	3589	761
120909	3589	764
120910	3589	768
120911	3589	775
120912	3589	781
120913	3589	782
120914	3589	787
120915	3589	789
120916	3589	792
120917	3589	795
120918	3589	797
120919	3589	801
120920	3589	807
120921	3589	814
120922	3589	819
120923	3589	823
120924	3589	827
120925	3589	830
120926	3589	835
120927	3589	841
120928	3589	845
120929	3589	846
120930	3589	851
120931	3589	852
120932	3589	859
120933	3589	860
120934	3589	871
120935	3589	873
120936	3589	876
120937	3590	732
120938	3590	734
120939	3590	740
120940	3590	742
120941	3590	746
120942	3590	749
120943	3590	753
120944	3590	757
120945	3590	761
120946	3590	764
120947	3590	768
120948	3590	772
120949	3590	777
120950	3590	782
120951	3590	787
120952	3590	789
120953	3590	792
120954	3590	794
120955	3590	806
120956	3590	811
120957	3590	819
120958	3590	822
120959	3590	827
120960	3590	830
120961	3590	835
120962	3590	841
120963	3590	845
120964	3590	846
120965	3590	851
120966	3590	852
120967	3590	859
120968	3590	860
120969	3590	871
120970	3590	873
120971	3590	874
120972	3591	732
120973	3591	734
120974	3591	740
120975	3591	743
120976	3591	746
120977	3591	748
120978	3591	752
120979	3591	758
120980	3591	761
120981	3591	764
120982	3591	768
120983	3591	772
120984	3591	777
120985	3591	782
120986	3591	787
120987	3591	789
120988	3591	792
120989	3591	794
120990	3591	808
120991	3591	811
120992	3591	819
120993	3591	822
120994	3591	826
120995	3591	835
120996	3591	841
120997	3591	843
120998	3591	847
120999	3591	849
121000	3591	854
121001	3591	856
121002	3591	860
121003	3591	871
121004	3591	872
121005	3591	874
121006	3592	732
121007	3592	734
121008	3592	740
121009	3592	742
121010	3592	746
121011	3592	748
121012	3592	753
121013	3592	756
121014	3592	761
121015	3592	764
121016	3592	768
121017	3592	772
121018	3592	777
121019	3592	782
121020	3592	787
121021	3592	789
121022	3592	792
121023	3592	795
121024	3592	797
121025	3592	801
121026	3592	806
121027	3592	811
121028	3592	819
121029	3592	822
121030	3592	827
121031	3592	830
121032	3592	835
121033	3592	842
121034	3592	845
121035	3592	847
121036	3592	851
121037	3592	853
121038	3592	857
121039	3592	860
121040	3592	871
121041	3592	872
121042	3592	874
121043	3593	732
121044	3593	734
121045	3593	740
121046	3593	742
121047	3593	746
121048	3593	749
121049	3593	754
121050	3593	758
121051	3593	761
121052	3593	764
121053	3593	768
121054	3593	772
121055	3593	777
121056	3593	782
121057	3593	787
121058	3593	789
121059	3593	792
121060	3593	794
121061	3593	806
121062	3593	811
121063	3593	819
121064	3593	822
121065	3593	827
121066	3593	831
121067	3593	835
121068	3593	841
121069	3593	845
121070	3593	846
121071	3593	851
121072	3593	852
121073	3593	859
121074	3593	860
121075	3593	871
121076	3593	873
121077	3593	874
121078	3594	732
121079	3594	734
121080	3594	740
121081	3594	743
121082	3594	746
121083	3594	748
121084	3594	753
121085	3594	758
121086	3594	761
121087	3594	764
121088	3594	768
121089	3594	775
121090	3594	781
121091	3594	784
121092	3594	787
121093	3594	789
121094	3594	792
121095	3594	794
121096	3594	807
121097	3594	816
121098	3594	819
121099	3594	822
121100	3594	827
121101	3594	832
121102	3594	835
121103	3594	841
121104	3594	845
121105	3594	847
121106	3594	851
121107	3594	853
121108	3594	857
121109	3594	860
121110	3594	871
121111	3594	872
121112	3594	874
121113	3595	732
121114	3595	734
121115	3595	740
121116	3595	743
121117	3595	746
121118	3595	749
121119	3595	754
121120	3595	757
121121	3595	761
121122	3595	764
121123	3595	768
121124	3595	776
121125	3595	780
121126	3595	782
121127	3595	787
121128	3595	789
121129	3595	792
121130	3595	794
121131	3595	807
121132	3595	815
121133	3595	819
121134	3595	822
121135	3595	826
121136	3595	835
121137	3595	842
121138	3595	845
121139	3595	847
121140	3595	851
121141	3595	854
121142	3595	857
121143	3595	860
121144	3595	871
121145	3595	872
121146	3595	874
121147	3596	732
121148	3596	734
121149	3596	740
121150	3596	743
121151	3596	746
121152	3596	749
121153	3596	753
121154	3596	757
121155	3596	761
121156	3596	764
121157	3596	768
121158	3596	774
121159	3596	777
121160	3596	782
121161	3596	787
121162	3596	789
121163	3596	792
121164	3596	795
121165	3596	800
121166	3596	804
121167	3596	806
121168	3596	814
121169	3596	819
121170	3596	822
121171	3596	826
121172	3596	830
121173	3596	835
121174	3596	841
121175	3596	845
121176	3596	846
121177	3596	851
121178	3596	852
121179	3596	859
121180	3596	860
121181	3596	871
121182	3596	872
121183	3596	876
121184	3597	732
121185	3597	734
121186	3597	740
121187	3597	743
121188	3597	746
121189	3597	749
121190	3597	754
121191	3597	758
121192	3597	761
121193	3597	764
121194	3597	768
121195	3597	772
121196	3597	777
121197	3597	782
121198	3597	787
121199	3597	789
121200	3597	792
121201	3597	794
121202	3597	807
121203	3597	811
121204	3597	819
121205	3597	822
121206	3597	825
121207	3597	831
121208	3597	835
121209	3597	842
121210	3597	845
121211	3597	847
121212	3597	851
121213	3597	854
121214	3597	857
121215	3597	860
121216	3597	871
121217	3597	872
121218	3597	874
121219	3598	733
121220	3598	734
121221	3598	740
121222	3598	742
121223	3598	746
121224	3598	749
121225	3598	753
121226	3598	757
121227	3598	761
121228	3598	764
121229	3598	768
121230	3598	772
121231	3598	777
121232	3598	782
121233	3598	787
121234	3598	789
121235	3598	792
121236	3598	794
121237	3598	806
121238	3598	811
121239	3598	819
121240	3598	822
121241	3598	826
121242	3598	835
121243	3598	841
121244	3598	845
121245	3598	846
121246	3598	851
121247	3598	852
121248	3598	859
121249	3598	860
121250	3598	871
121251	3598	872
121252	3598	876
121253	3599	732
121254	3599	734
121255	3599	740
121256	3599	743
121257	3599	746
121258	3599	749
121259	3599	753
121260	3599	758
121261	3599	761
121262	3599	764
121263	3599	768
121264	3599	775
121265	3599	781
121266	3599	782
121267	3599	787
121268	3599	789
121269	3599	792
121270	3599	794
121271	3599	806
121272	3599	815
121273	3599	819
121274	3599	823
121275	3599	828
121276	3599	831
121277	3599	835
121278	3599	840
121279	3599	845
121280	3599	846
121281	3599	851
121282	3599	852
121283	3599	859
121284	3599	860
121285	3599	871
121286	3599	873
121287	3599	874
121288	3600	732
121289	3600	734
121290	3600	740
121291	3600	744
121292	3600	746
121293	3600	748
121294	3600	752
121295	3600	759
121296	3600	761
121297	3600	764
121298	3600	768
121299	3600	774
121300	3600	781
121301	3600	782
121302	3600	787
121303	3600	789
121304	3600	792
121305	3600	794
121306	3600	806
121307	3600	816
121308	3600	819
121309	3600	823
121310	3600	827
121311	3600	832
121312	3600	834
121313	3600	840
121314	3600	845
121315	3600	846
121316	3600	851
121317	3600	852
121318	3600	859
121319	3600	860
121320	3600	871
121321	3600	873
121322	3600	874
121323	3601	732
121324	3601	734
121325	3601	740
121326	3601	743
121327	3601	746
121328	3601	749
121329	3601	754
121330	3601	757
121331	3601	761
121332	3601	764
121333	3601	768
121334	3601	772
121335	3601	777
121336	3601	782
121337	3601	787
121338	3601	789
121339	3601	792
121340	3601	794
121341	3601	808
121342	3601	811
121343	3601	818
121344	3601	822
121345	3601	827
121346	3601	831
121347	3601	835
121348	3601	841
121349	3601	843
121350	3601	847
121351	3601	849
121352	3601	853
121353	3601	856
121354	3601	860
121355	3601	871
121356	3601	872
121357	3601	874
121358	3602	731
121359	3602	734
121360	3602	740
121361	3602	743
121362	3602	746
121363	3602	748
121364	3602	753
121365	3602	758
121366	3602	761
121367	3602	764
121368	3602	768
121369	3602	775
121370	3602	777
121371	3602	783
121372	3602	787
121373	3602	789
121374	3602	792
121375	3602	794
121376	3602	806
121377	3602	815
121378	3602	819
121379	3602	822
121380	3602	826
121381	3602	831
121382	3602	835
121383	3602	841
121384	3602	845
121385	3602	846
121386	3602	851
121387	3602	852
121388	3602	859
121389	3602	860
121390	3602	871
121391	3602	873
121392	3602	874
121393	3603	732
121394	3603	734
121395	3603	740
121396	3603	742
121397	3603	746
121398	3603	748
121399	3603	752
121400	3603	757
121401	3603	761
121402	3603	764
121403	3603	768
121404	3603	772
121405	3603	777
121406	3603	782
121407	3603	787
121408	3603	789
121409	3603	792
121410	3603	794
121411	3603	806
121412	3603	811
121413	3603	818
121414	3603	821
121415	3603	825
121416	3603	831
121417	3603	835
121418	3603	842
121419	3603	845
121420	3603	847
121421	3603	851
121422	3603	854
121423	3603	857
121424	3603	860
121425	3603	871
121426	3603	872
121427	3603	874
121428	3604	732
121429	3604	734
121430	3604	740
121431	3604	744
121432	3604	746
121433	3604	749
121434	3604	753
121435	3604	758
121436	3604	761
121437	3604	764
121438	3604	768
121439	3604	772
121440	3604	777
121441	3604	784
121442	3604	787
121443	3604	789
121444	3604	792
121445	3604	794
121446	3604	808
121447	3604	811
121448	3604	819
121449	3604	823
121450	3604	828
121451	3604	832
121452	3604	835
121453	3604	840
121454	3604	845
121455	3604	847
121456	3604	851
121457	3604	853
121458	3604	858
121459	3604	860
121460	3604	871
121461	3604	872
121462	3604	874
121463	3605	732
121464	3605	734
121465	3605	740
121466	3605	744
121467	3605	745
121468	3605	751
121469	3605	755
121470	3605	758
121471	3605	761
121472	3605	764
121473	3605	769
121474	3605	775
121475	3605	777
121476	3605	784
121477	3605	787
121478	3605	789
121479	3605	792
121480	3605	794
121481	3605	808
121482	3605	814
121483	3605	820
121484	3605	823
121485	3605	828
121486	3605	831
121487	3605	836
121488	3605	842
121489	3605	845
121490	3605	848
121491	3605	851
121492	3605	854
121493	3605	857
121494	3605	860
121495	3605	871
121496	3605	874
121497	3606	732
121498	3606	734
121499	3606	740
121500	3606	744
121501	3606	746
121502	3606	749
121503	3606	754
121504	3606	758
121505	3606	761
121506	3606	764
121507	3606	768
121508	3606	772
121509	3606	777
121510	3606	785
121511	3606	787
121512	3606	789
121513	3606	793
121514	3606	794
121515	3606	808
121516	3606	811
121517	3606	819
121518	3606	823
121519	3606	828
121520	3606	832
121521	3606	835
121522	3606	841
121523	3606	844
121524	3606	847
121525	3606	850
121526	3606	854
121527	3606	856
121528	3606	860
121529	3606	871
121530	3606	874
121531	3607	732
121532	3607	734
121533	3607	740
121534	3607	743
121535	3607	746
121536	3607	750
121537	3607	755
121538	3607	756
121539	3607	761
121540	3607	764
121541	3607	768
121542	3607	772
121543	3607	777
121544	3607	784
121545	3607	787
121546	3607	789
121547	3607	792
121548	3607	794
121549	3607	808
121550	3607	811
121551	3607	819
121552	3607	823
121553	3607	827
121554	3607	830
121555	3607	835
121556	3607	860
121557	3607	871
121558	3607	874
121559	3608	732
121560	3608	734
121561	3608	740
121562	3608	744
121563	3608	746
121564	3608	749
121565	3608	754
121566	3608	758
121567	3608	761
121568	3608	764
121569	3608	768
121570	3608	772
121571	3608	777
121572	3608	786
121573	3608	787
121574	3608	789
121575	3608	793
121576	3608	794
121577	3608	809
121578	3608	811
121579	3608	819
121580	3608	822
121581	3608	828
121582	3608	831
121583	3608	835
121584	3608	841
121585	3608	845
121586	3608	847
121587	3608	851
121588	3608	853
121589	3608	857
121590	3608	860
121591	3608	871
121592	3608	874
121593	3609	732
121594	3609	734
121595	3609	740
121596	3609	744
121597	3609	745
121598	3609	749
121599	3609	753
121600	3609	759
121601	3609	761
121602	3609	764
121603	3609	768
121604	3609	772
121605	3609	777
121606	3609	784
121607	3609	787
121608	3609	789
121609	3609	792
121610	3609	794
121611	3609	808
121612	3609	811
121613	3609	818
121614	3609	821
121615	3609	828
121616	3609	832
121617	3609	835
121618	3609	841
121619	3609	845
121620	3609	847
121621	3609	851
121622	3609	853
121623	3609	857
121624	3609	860
121625	3609	871
121626	3609	874
121627	3610	732
121628	3610	734
121629	3610	740
121630	3610	743
121631	3610	745
121632	3610	749
121633	3610	754
121634	3610	759
121635	3610	761
121636	3610	764
121637	3610	768
121638	3610	772
121639	3610	777
121640	3610	785
121641	3610	787
121642	3610	789
121643	3610	793
121644	3610	794
121645	3610	808
121646	3610	811
121647	3610	819
121648	3610	822
121649	3610	828
121650	3610	831
121651	3610	835
121652	3610	841
121653	3610	843
121654	3610	847
121655	3610	849
121656	3610	854
121657	3610	856
121658	3610	860
121659	3610	871
121660	3610	874
121661	3611	732
121662	3611	734
121663	3611	740
121664	3611	744
121665	3611	745
121666	3611	750
121667	3611	755
121668	3611	759
121669	3611	761
121670	3611	764
121671	3611	768
121672	3611	772
121673	3611	777
121674	3611	785
121675	3611	787
121676	3611	789
121677	3611	792
121678	3611	794
121679	3611	806
121680	3611	811
121681	3611	819
121682	3611	822
121683	3611	828
121684	3611	832
121685	3611	835
121686	3611	841
121687	3611	845
121688	3611	847
121689	3611	851
121690	3611	853
121691	3611	858
121692	3611	860
121693	3611	871
121694	3611	874
121695	3612	732
121696	3612	734
121697	3612	740
121698	3612	744
121699	3612	745
121700	3612	749
121701	3612	754
121702	3612	759
121703	3612	761
121704	3612	764
121705	3612	768
121706	3612	772
121707	3612	777
121708	3612	785
121709	3612	787
121710	3612	789
121711	3612	793
121712	3612	794
121713	3612	808
121714	3612	811
121715	3612	819
121716	3612	823
121717	3612	828
121718	3612	831
121719	3612	835
121720	3612	841
121721	3612	844
121722	3612	847
121723	3612	850
121724	3612	853
121725	3612	857
121726	3612	860
121727	3612	871
121728	3612	874
121729	3613	732
121730	3613	734
121731	3613	740
121732	3613	743
121733	3613	747
121734	3613	749
121735	3613	754
121736	3613	759
121737	3613	761
121738	3613	764
121739	3613	768
121740	3613	772
121741	3613	777
121742	3613	784
121743	3613	787
121744	3613	789
121745	3613	791
121746	3613	794
121747	3613	808
121748	3613	811
121749	3613	818
121750	3613	821
121751	3613	827
121752	3613	832
121753	3613	835
121754	3613	841
121755	3613	844
121756	3613	848
121757	3613	850
121758	3613	854
121759	3613	856
121760	3613	860
121761	3613	871
121762	3613	874
121763	3614	732
121764	3614	734
121765	3614	740
121766	3614	743
121767	3614	747
121768	3614	749
121769	3614	753
121770	3614	759
121771	3614	761
121772	3614	764
121773	3614	768
121774	3614	772
121775	3614	777
121776	3614	785
121777	3614	787
121778	3614	789
121779	3614	792
121780	3614	795
121781	3614	797
121782	3614	802
121783	3614	808
121784	3614	811
121785	3614	818
121786	3614	821
121787	3614	828
121788	3614	832
121789	3614	835
121790	3614	841
121791	3614	845
121792	3614	847
121793	3614	851
121794	3614	853
121795	3614	857
121796	3614	860
121797	3614	871
121798	3614	874
121799	3615	732
121800	3615	734
121801	3615	740
121802	3615	744
121803	3615	747
121804	3615	749
121805	3615	754
121806	3615	759
121807	3615	761
121808	3615	764
121809	3615	768
121810	3615	772
121811	3615	777
121812	3615	786
121813	3615	787
121814	3615	789
121815	3615	793
121816	3615	794
121817	3615	809
121818	3615	811
121819	3615	819
121820	3615	822
121821	3615	828
121822	3615	833
121823	3615	835
121824	3615	842
121825	3615	845
121826	3615	847
121827	3615	851
121828	3615	854
121829	3615	857
121830	3615	860
121831	3615	871
121832	3615	874
121833	3616	732
121834	3616	734
121835	3616	740
121836	3616	743
121837	3616	745
121838	3616	749
121839	3616	753
121840	3616	759
121841	3616	761
121842	3616	764
121843	3616	768
121844	3616	772
121845	3616	777
121846	3616	784
121847	3616	787
121848	3616	789
121849	3616	792
121850	3616	794
121851	3616	808
121852	3616	811
121853	3616	818
121854	3616	822
121855	3616	828
121856	3616	832
121857	3616	835
121858	3616	841
121859	3616	843
121860	3616	847
121861	3616	849
121862	3616	854
121863	3616	856
121864	3616	860
121865	3616	871
121866	3616	874
121867	3617	732
121868	3617	734
121869	3617	740
121870	3617	744
121871	3617	746
121872	3617	749
121873	3617	753
121874	3617	759
121875	3617	761
121876	3617	764
121877	3617	768
121878	3617	772
121879	3617	777
121880	3617	786
121881	3617	787
121882	3617	789
121883	3617	793
121884	3617	794
121885	3617	808
121886	3617	811
121887	3617	819
121888	3617	822
121889	3617	828
121890	3617	832
121891	3617	835
121892	3617	841
121893	3617	844
121894	3617	847
121895	3617	850
121896	3617	854
121897	3617	856
121898	3617	860
121899	3617	871
121900	3617	874
121901	3618	732
121902	3618	734
121903	3618	740
121904	3618	744
121905	3618	746
121906	3618	749
121907	3618	754
121908	3618	759
121909	3618	761
121910	3618	764
121911	3618	768
121912	3618	772
121913	3618	777
121914	3618	786
121915	3618	787
121916	3618	789
121917	3618	793
121918	3618	794
121919	3618	808
121920	3618	811
121921	3618	820
121922	3618	823
121923	3618	828
121924	3618	832
121925	3618	835
121926	3618	841
121927	3618	844
121928	3618	847
121929	3618	851
121930	3618	854
121931	3618	857
121932	3618	860
121933	3618	871
121934	3618	874
121935	3619	732
121936	3619	734
121937	3619	740
121938	3619	743
121939	3619	746
121940	3619	749
121941	3619	754
121942	3619	758
121943	3619	761
121944	3619	764
121945	3619	768
121946	3619	772
121947	3619	777
121948	3619	784
121949	3619	787
121950	3619	789
121951	3619	791
121952	3619	794
121953	3619	808
121954	3619	811
121955	3619	818
121956	3619	822
121957	3619	827
121958	3619	832
121959	3619	835
121960	3619	841
121961	3619	844
121962	3619	848
121963	3619	850
121964	3619	854
121965	3619	856
121966	3619	860
121967	3619	871
121968	3619	874
121969	3620	732
121970	3620	734
121971	3620	740
121972	3620	744
121973	3620	745
121974	3620	750
121975	3620	754
121976	3620	758
121977	3620	761
121978	3620	764
121979	3620	768
121980	3620	772
121981	3620	777
121982	3620	785
121983	3620	787
121984	3620	789
121985	3620	793
121986	3620	794
121987	3620	808
121988	3620	811
121989	3620	819
121990	3620	823
121991	3620	828
121992	3620	830
121993	3620	835
121994	3620	841
121995	3620	843
121996	3620	847
121997	3620	849
121998	3620	854
121999	3620	856
122000	3620	860
122001	3620	871
122002	3620	874
122003	3621	732
122004	3621	735
122005	3621	737
122006	3621	741
122007	3621	744
122008	3621	746
122009	3621	749
122010	3621	754
122011	3621	758
122012	3621	761
122013	3621	764
122014	3621	768
122015	3621	772
122016	3621	777
122017	3621	786
122018	3621	788
122019	3621	789
122020	3621	793
122021	3621	795
122022	3621	800
122023	3621	804
122024	3621	808
122025	3621	811
122026	3621	818
122027	3621	823
122028	3621	828
122029	3621	831
122030	3621	835
122031	3621	841
122032	3621	844
122033	3621	847
122034	3621	850
122035	3621	854
122036	3621	856
122037	3621	860
122038	3621	871
122039	3621	874
122040	3622	732
122041	3622	734
122042	3622	740
122043	3622	744
122044	3622	746
122045	3622	751
122046	3622	755
122047	3622	758
122048	3622	761
122049	3622	764
122050	3622	768
122051	3622	775
122052	3622	781
122053	3622	785
122054	3622	787
122055	3622	789
122056	3622	793
122057	3622	794
122058	3622	808
122059	3622	815
122060	3622	819
122061	3622	823
122062	3622	827
122063	3622	831
122064	3622	835
122065	3622	841
122066	3622	845
122067	3622	847
122068	3622	851
122069	3622	853
122070	3622	857
122071	3622	860
122072	3622	871
122073	3622	874
122074	3623	732
122075	3623	734
122076	3623	740
122077	3623	744
122078	3623	746
122079	3623	749
122080	3623	754
122081	3623	759
122082	3623	761
122083	3623	764
122084	3623	768
122085	3623	772
122086	3623	777
122087	3623	785
122088	3623	787
122089	3623	789
122090	3623	793
122091	3623	794
122092	3623	809
122093	3623	811
122094	3623	819
122095	3623	822
122096	3623	828
122097	3623	832
122098	3623	835
122099	3623	842
122100	3623	845
122101	3623	847
122102	3623	851
122103	3623	854
122104	3623	857
122105	3623	860
122106	3623	871
122107	3623	874
122108	3624	732
122109	3624	734
122110	3624	740
122111	3624	744
122112	3624	746
122113	3624	750
122114	3624	755
122115	3624	758
122116	3624	761
122117	3624	764
122118	3624	768
122119	3624	772
122120	3624	777
122121	3624	785
122122	3624	787
122123	3624	789
122124	3624	793
122125	3624	794
122126	3624	808
122127	3624	811
122128	3624	823
122129	3624	826
122130	3624	832
122131	3624	835
122132	3624	842
122133	3624	845
122134	3624	847
122135	3624	851
122136	3624	853
122137	3624	858
122138	3624	860
122139	3624	871
122140	3624	874
122141	3625	732
122142	3625	734
122143	3625	740
122144	3625	743
122145	3625	746
122146	3625	748
122147	3625	753
122148	3625	759
122149	3625	761
122150	3625	764
122151	3625	768
122152	3625	772
122153	3625	777
122154	3625	784
122155	3625	787
122156	3625	789
122157	3625	792
122158	3625	794
122159	3625	806
122160	3625	811
122161	3625	818
122162	3625	823
122163	3625	828
122164	3625	835
122165	3625	841
122166	3625	843
122167	3625	847
122168	3625	849
122169	3625	853
122170	3625	856
122171	3625	860
122172	3625	871
122173	3625	874
122174	3626	732
122175	3626	734
122176	3626	740
122177	3626	744
122178	3626	746
122179	3626	749
122180	3626	753
122181	3626	759
122182	3626	761
122183	3626	764
122184	3626	768
122185	3626	773
122186	3626	777
122187	3626	784
122188	3626	787
122189	3626	789
122190	3626	792
122191	3626	795
122192	3626	798
122193	3626	802
122194	3626	808
122195	3626	814
122196	3626	819
122197	3626	823
122198	3626	828
122199	3626	832
122200	3626	835
122201	3626	841
122202	3626	843
122203	3626	847
122204	3626	849
122205	3626	853
122206	3626	856
122207	3626	860
122208	3626	869
122209	3626	874
122210	3627	732
122211	3627	734
122212	3627	740
122213	3627	744
122214	3627	746
122215	3627	749
122216	3627	754
122217	3627	758
122218	3627	761
122219	3627	764
122220	3627	768
122221	3627	772
122222	3627	777
122223	3627	784
122224	3627	787
122225	3627	789
122226	3627	792
122227	3627	794
122228	3627	807
122229	3627	811
122230	3627	819
122231	3627	822
122232	3627	827
122233	3627	835
122234	3627	842
122235	3627	845
122236	3627	848
122237	3627	851
122238	3627	854
122239	3627	857
122240	3627	860
122241	3627	871
122242	3627	872
122243	3627	874
122244	3628	732
122245	3628	734
122246	3628	740
122247	3628	744
122248	3628	746
122249	3628	749
122250	3628	753
122251	3628	759
122252	3628	761
122253	3628	765
122254	3628	769
122255	3628	774
122256	3628	777
122257	3628	785
122258	3628	787
122259	3628	789
122260	3628	792
122261	3628	794
122262	3628	808
122263	3628	814
122264	3628	819
122265	3628	823
122266	3628	828
122267	3628	832
122268	3628	836
122269	3628	842
122270	3628	845
122271	3628	848
122272	3628	851
122273	3628	854
122274	3628	857
122275	3628	860
122276	3628	871
122277	3628	874
122278	3629	732
122279	3629	734
122280	3629	740
122281	3629	743
122282	3629	746
122283	3629	749
122284	3629	753
122285	3629	760
122286	3629	761
122287	3629	764
122288	3629	768
122289	3629	773
122290	3629	777
122291	3629	783
122292	3629	787
122293	3629	789
122294	3629	792
122295	3629	794
122296	3629	806
122297	3629	814
122298	3629	819
122299	3629	822
122300	3629	827
122301	3629	832
122302	3629	835
122303	3629	841
122304	3629	845
122305	3629	846
122306	3629	851
122307	3629	852
122308	3629	859
122309	3629	860
122310	3629	871
122311	3629	874
122312	3630	732
122313	3630	734
122314	3630	740
122315	3630	743
122316	3630	746
122317	3630	749
122318	3630	753
122319	3630	759
122320	3630	761
122321	3630	764
122322	3630	768
122323	3630	774
122324	3630	777
122325	3630	783
122326	3630	787
122327	3630	789
122328	3630	792
122329	3630	794
122330	3630	808
122331	3630	814
122332	3630	818
122333	3630	821
122334	3630	828
122335	3630	832
122336	3630	836
122337	3630	841
122338	3630	843
122339	3630	847
122340	3630	849
122341	3630	853
122342	3630	856
122343	3630	860
122344	3630	871
122345	3630	874
122346	3631	732
122347	3631	734
122348	3631	740
122349	3631	743
122350	3631	746
122351	3631	748
122352	3631	753
122353	3631	759
122354	3631	761
122355	3631	764
122356	3631	768
122357	3631	773
122358	3631	777
122359	3631	783
122360	3631	787
122361	3631	789
122362	3631	792
122363	3631	794
122364	3631	806
122365	3631	813
122366	3631	819
122367	3631	823
122368	3631	828
122369	3631	836
122370	3631	841
122371	3631	843
122372	3631	847
122373	3631	849
122374	3631	854
122375	3631	856
122376	3631	860
122377	3631	871
122378	3631	872
122379	3631	874
122380	3632	732
122381	3632	734
122382	3632	740
122383	3632	744
122384	3632	745
122385	3632	749
122386	3632	753
122387	3632	757
122388	3632	761
122389	3632	764
122390	3632	768
122391	3632	772
122392	3632	777
122393	3632	785
122394	3632	787
122395	3632	789
122396	3632	793
122397	3632	794
122398	3632	806
122399	3632	811
122400	3632	819
122401	3632	823
122402	3632	828
122403	3632	831
122404	3632	835
122405	3632	841
122406	3632	845
122407	3632	847
122408	3632	851
122409	3632	853
122410	3632	858
122411	3632	860
122412	3632	871
122413	3632	874
122414	3633	732
122415	3633	734
122416	3633	740
122417	3633	743
122418	3633	746
122419	3633	748
122420	3633	753
122421	3633	759
122422	3633	761
122423	3633	764
122424	3633	768
122425	3633	773
122426	3633	777
122427	3633	783
122428	3633	787
122429	3633	789
122430	3633	792
122431	3633	794
122432	3633	807
122433	3633	814
122434	3633	818
122435	3633	822
122436	3633	827
122437	3633	832
122438	3633	835
122439	3633	841
122440	3633	843
122441	3633	847
122442	3633	849
122443	3633	854
122444	3633	856
122445	3633	860
122446	3633	871
122447	3633	874
122448	3634	731
122449	3634	734
122450	3634	740
122451	3634	743
122452	3634	745
122453	3634	748
122454	3634	753
122455	3634	760
122456	3634	764
122457	3634	768
122458	3634	775
122459	3634	782
122460	3634	787
122461	3634	789
122462	3634	792
122463	3634	794
122464	3634	806
122465	3634	815
122466	3634	819
122467	3634	823
122468	3634	824
122469	3634	833
122470	3634	835
122471	3634	841
122472	3634	845
122473	3634	846
122474	3634	851
122475	3634	852
122476	3634	859
122477	3634	860
122478	3635	732
122479	3635	734
122480	3635	740
122481	3635	744
122482	3635	746
122483	3635	749
122484	3635	754
122485	3635	759
122486	3635	761
122487	3635	764
122488	3635	769
122489	3635	774
122490	3635	777
122491	3635	785
122492	3635	787
122493	3635	789
122494	3635	793
122495	3635	794
122496	3635	808
122497	3635	814
122498	3635	819
122499	3635	822
122500	3635	827
122501	3635	832
122502	3635	836
122503	3635	842
122504	3635	845
122505	3635	848
122506	3635	851
122507	3635	854
122508	3635	857
122509	3635	860
122510	3635	871
122511	3635	874
122512	3636	732
122513	3636	734
122514	3636	740
122515	3636	744
122516	3636	746
122517	3636	748
122518	3636	752
122519	3636	757
122520	3636	761
122521	3636	764
122522	3636	768
122523	3636	772
122524	3636	777
122525	3636	784
122526	3636	787
122527	3636	789
122528	3636	792
122529	3636	795
122530	3636	796
122531	3636	801
122532	3636	808
122533	3636	811
122534	3636	819
122535	3636	823
122536	3636	827
122537	3636	832
122538	3636	835
122539	3636	841
122540	3636	843
122541	3636	847
122542	3636	849
122543	3636	854
122544	3636	856
122545	3636	860
122546	3636	871
122547	3636	874
122548	3637	732
122549	3637	734
122550	3637	740
122551	3637	743
122552	3637	746
122553	3637	749
122554	3637	753
122555	3637	758
122556	3637	761
122557	3637	764
122558	3637	768
122559	3637	772
122560	3637	777
122561	3637	784
122562	3637	787
122563	3637	789
122564	3637	792
122565	3637	794
122566	3637	806
122567	3637	811
122568	3637	818
122569	3637	823
122570	3637	827
122571	3637	830
122572	3637	835
122573	3637	841
122574	3637	845
122575	3637	846
122576	3637	851
122577	3637	852
122578	3637	859
122579	3637	860
122580	3637	871
122581	3637	873
122582	3637	874
122583	3638	732
122584	3638	734
122585	3638	740
122586	3638	743
122587	3638	746
122588	3638	749
122589	3638	753
122590	3638	760
122591	3638	761
122592	3638	764
122593	3638	768
122594	3638	772
122595	3638	777
122596	3638	784
122597	3638	787
122598	3638	789
122599	3638	793
122600	3638	794
122601	3638	807
122602	3638	811
122603	3638	819
122604	3638	823
122605	3638	827
122606	3638	832
122607	3638	835
122608	3638	840
122609	3638	845
122610	3638	846
122611	3638	851
122612	3638	852
122613	3638	859
122614	3638	860
122615	3638	871
122616	3638	874
122617	3639	732
122618	3639	734
122619	3639	740
122620	3639	742
122621	3639	746
122622	3639	749
122623	3639	753
122624	3639	758
122625	3639	761
122626	3639	764
122627	3639	768
122628	3639	772
122629	3639	777
122630	3639	784
122631	3639	787
122632	3639	789
122633	3639	792
122634	3639	794
122635	3639	808
122636	3639	811
122637	3639	818
122638	3639	822
122639	3639	828
122640	3639	830
122641	3639	835
122642	3639	841
122643	3639	843
122644	3639	847
122645	3639	849
122646	3639	853
122647	3639	856
122648	3639	860
122649	3639	871
122650	3639	872
122651	3639	874
122652	3640	732
122653	3640	734
122654	3640	740
122655	3640	743
122656	3640	745
122657	3640	749
122658	3640	753
122659	3640	756
122660	3640	761
122661	3640	764
122662	3640	768
122663	3640	772
122664	3640	777
122665	3640	785
122666	3640	787
122667	3640	789
122668	3640	792
122669	3640	794
122670	3640	808
122671	3640	811
122672	3640	818
122673	3640	823
122674	3640	828
122675	3640	830
122676	3640	835
122677	3640	841
122678	3640	843
122679	3640	847
122680	3640	849
122681	3640	854
122682	3640	856
122683	3640	860
122684	3640	871
122685	3640	874
122686	3641	733
122687	3641	735
122688	3641	737
122689	3641	740
122690	3641	743
122691	3641	745
122692	3641	748
122693	3641	753
122694	3641	759
122695	3641	761
122696	3641	764
122697	3641	768
122698	3641	775
122699	3641	781
122700	3641	784
122701	3641	787
122702	3641	789
122703	3641	793
122704	3641	795
122705	3641	797
122706	3641	802
122707	3641	807
122708	3641	814
122709	3641	819
122710	3641	823
122711	3641	828
122712	3641	832
122713	3641	835
122714	3641	841
122715	3641	845
122716	3641	846
122717	3641	851
122718	3641	852
122719	3641	858
122720	3641	860
122721	3641	871
122722	3641	872
122723	3641	874
122724	3642	732
122725	3642	734
122726	3642	740
122727	3642	744
122728	3642	746
122729	3642	749
122730	3642	753
122731	3642	760
122732	3642	761
122733	3642	764
122734	3642	768
122735	3642	774
122736	3642	777
122737	3642	784
122738	3642	787
122739	3642	789
122740	3642	793
122741	3642	794
122742	3642	806
122743	3642	814
122744	3642	819
122745	3642	822
122746	3642	825
122747	3642	831
122748	3642	835
122749	3642	840
122750	3642	845
122751	3642	846
122752	3642	851
122753	3642	852
122754	3642	859
122755	3642	860
122756	3642	871
122757	3642	874
122758	3643	731
122759	3643	734
122760	3643	740
122761	3643	743
122762	3643	746
122763	3643	749
122764	3643	754
122765	3643	759
122766	3643	761
122767	3643	764
122768	3643	768
122769	3643	772
122770	3643	777
122771	3643	784
122772	3643	787
122773	3643	789
122774	3643	793
122775	3643	795
122776	3643	798
122777	3643	803
122778	3643	807
122779	3643	811
122780	3643	819
122781	3643	823
122782	3643	828
122783	3643	831
122784	3643	835
122785	3643	841
122786	3643	845
122787	3643	846
122788	3643	851
122789	3643	852
122790	3643	859
122791	3643	865
122792	3643	871
122793	3643	872
122794	3643	876
122795	3644	732
122796	3644	734
122797	3644	740
122798	3644	744
122799	3644	746
122800	3644	749
122801	3644	753
122802	3644	760
122803	3644	761
122804	3644	764
122805	3644	768
122806	3644	774
122807	3644	781
122808	3644	784
122809	3644	787
122810	3644	789
122811	3644	793
122812	3644	794
122813	3644	806
122814	3644	814
122815	3644	819
122816	3644	823
122817	3644	826
122818	3644	831
122819	3644	835
122820	3644	840
122821	3644	845
122822	3644	846
122823	3644	851
122824	3644	852
122825	3644	859
122826	3644	860
122827	3644	871
122828	3644	874
122829	3645	732
122830	3645	734
122831	3645	740
122832	3645	743
122833	3645	745
122834	3645	749
122835	3645	753
122836	3645	757
122837	3645	761
122838	3645	764
122839	3645	768
122840	3645	772
122841	3645	777
122842	3645	783
122843	3645	787
122844	3645	789
122845	3645	792
122846	3645	794
122847	3645	806
122848	3645	811
122849	3645	818
122850	3645	822
122851	3645	827
122852	3645	830
122853	3645	835
122854	3645	841
122855	3645	845
122856	3645	846
122857	3645	851
122858	3645	852
122859	3645	859
122860	3645	860
122861	3645	871
122862	3645	872
122863	3645	876
122864	3646	732
122865	3646	734
122866	3646	740
122867	3646	743
122868	3646	745
122869	3646	749
122870	3646	753
122871	3646	760
122872	3646	761
122873	3646	764
122874	3646	768
122875	3646	774
122876	3646	781
122877	3646	784
122878	3646	787
122879	3646	789
122880	3646	793
122881	3646	795
122882	3646	796
122883	3646	801
122884	3646	808
122885	3646	815
122886	3646	819
122887	3646	823
122888	3646	827
122889	3646	833
122890	3646	835
122891	3646	842
122892	3646	845
122893	3646	847
122894	3646	851
122895	3646	853
122896	3646	858
122897	3646	860
122898	3646	871
122899	3646	874
122900	3647	732
122901	3647	734
122902	3647	740
122903	3647	743
122904	3647	746
122905	3647	750
122906	3647	754
122907	3647	759
122908	3647	761
122909	3647	764
122910	3647	769
122911	3647	775
122912	3647	781
122913	3647	786
122914	3647	787
122915	3647	789
122916	3647	792
122917	3647	794
122918	3647	809
122919	3647	815
122920	3647	818
122921	3647	822
122922	3647	828
122923	3647	832
122924	3647	836
122925	3647	841
122926	3647	844
122927	3647	848
122928	3647	850
122929	3647	854
122930	3647	856
122931	3647	860
122932	3647	871
122933	3647	874
122934	3648	731
122935	3648	734
122936	3648	740
122937	3648	742
122938	3648	746
122939	3648	749
122940	3648	753
122941	3648	757
122942	3648	761
122943	3648	764
122944	3648	768
122945	3648	774
122946	3648	777
122947	3648	783
122948	3648	787
122949	3648	789
122950	3648	792
122951	3648	794
122952	3648	808
122953	3648	814
122954	3648	818
122955	3648	822
122956	3648	828
122957	3648	830
122958	3648	835
122959	3648	841
122960	3648	845
122961	3648	847
122962	3648	851
122963	3648	853
122964	3648	858
122965	3648	860
122966	3648	871
122967	3648	872
122968	3648	874
122969	3649	732
122970	3649	734
122971	3649	740
122972	3649	744
122973	3649	746
122974	3649	749
122975	3649	755
122976	3649	760
122977	3649	761
122978	3649	765
122979	3649	769
122980	3649	773
122981	3649	780
122982	3649	786
122983	3649	787
122984	3649	789
122985	3649	793
122986	3649	794
122987	3649	809
122988	3649	814
122989	3649	819
122990	3649	823
122991	3649	828
122992	3649	832
122993	3649	835
122994	3649	841
122995	3649	844
122996	3649	847
122997	3649	850
122998	3649	854
122999	3649	856
123000	3649	860
123001	3649	871
123002	3649	874
123003	3650	732
123004	3650	734
123005	3650	740
123006	3650	744
123007	3650	746
123008	3650	750
123009	3650	754
123010	3650	759
123011	3650	761
123012	3650	764
123013	3650	768
123014	3650	772
123015	3650	777
123016	3650	786
123017	3650	787
123018	3650	789
123019	3650	793
123020	3650	794
123021	3650	809
123022	3650	811
123023	3650	819
123024	3650	823
123025	3650	828
123026	3650	832
123027	3650	835
123028	3650	841
123029	3650	844
123030	3650	848
123031	3650	850
123032	3650	854
123033	3650	856
123034	3650	860
123035	3650	871
123036	3650	874
123037	3651	732
123038	3651	734
123039	3651	740
123040	3651	744
123041	3651	747
123042	3651	749
123043	3651	755
123044	3651	760
123045	3651	761
123046	3651	764
123047	3651	768
123048	3651	772
123049	3651	777
123050	3651	786
123051	3651	787
123052	3651	789
123053	3651	793
123054	3651	794
123055	3651	809
123056	3651	811
123057	3651	819
123058	3651	822
123059	3651	828
123060	3651	832
123061	3651	835
123062	3651	841
123063	3651	845
123064	3651	847
123065	3651	851
123066	3651	853
123067	3651	858
123068	3651	860
123069	3651	871
123070	3651	874
123071	3652	732
123072	3652	734
123073	3652	740
123074	3652	743
123075	3652	745
123076	3652	748
123077	3652	752
123078	3652	758
123079	3652	761
123080	3652	764
123081	3652	768
123082	3652	772
123083	3652	777
123084	3652	784
123085	3652	787
123086	3652	789
123087	3652	792
123088	3652	794
123089	3652	807
123090	3652	811
123091	3652	818
123092	3652	822
123093	3652	828
123094	3652	832
123095	3652	835
123096	3652	840
123097	3652	843
123098	3652	847
123099	3652	849
123100	3652	853
123101	3652	856
123102	3652	860
123103	3652	871
123104	3652	874
123105	3653	732
123106	3653	734
123107	3653	740
123108	3653	744
123109	3653	746
123110	3653	749
123111	3653	754
123112	3653	758
123113	3653	761
123114	3653	767
123115	3653	771
123116	3653	775
123117	3653	781
123118	3653	785
123119	3653	788
123120	3653	790
123121	3653	792
123122	3653	794
123123	3653	808
123124	3653	816
123125	3653	819
123126	3653	823
123127	3653	827
123128	3653	832
123129	3653	839
123130	3653	841
123131	3653	844
123132	3653	848
123133	3653	850
123134	3653	854
123135	3653	856
123136	3653	860
123137	3653	871
123138	3653	874
123139	3654	732
123140	3654	734
123141	3654	740
123142	3654	744
123143	3654	746
123144	3654	750
123145	3654	754
123146	3654	759
123147	3654	761
123148	3654	764
123149	3654	768
123150	3654	772
123151	3654	777
123152	3654	786
123153	3654	787
123154	3654	789
123155	3654	793
123156	3654	794
123157	3654	808
123158	3654	811
123159	3654	819
123160	3654	823
123161	3654	828
123162	3654	832
123163	3654	835
123164	3654	841
123165	3654	844
123166	3654	847
123167	3654	850
123168	3654	854
123169	3654	857
123170	3654	860
123171	3654	871
123172	3654	874
123173	3655	732
123174	3655	734
123175	3655	740
123176	3655	744
123177	3655	746
123178	3655	750
123179	3655	755
123180	3655	758
123181	3655	761
123182	3655	764
123183	3655	768
123184	3655	772
123185	3655	777
123186	3655	785
123187	3655	787
123188	3655	789
123189	3655	793
123190	3655	794
123191	3655	807
123192	3655	811
123193	3655	819
123194	3655	822
123195	3655	828
123196	3655	831
123197	3655	835
123198	3655	841
123199	3655	845
123200	3655	847
123201	3655	851
123202	3655	853
123203	3655	858
123204	3655	860
123205	3655	871
123206	3655	874
123207	3656	732
123208	3656	734
123209	3656	740
123210	3656	743
123211	3656	746
123212	3656	748
123213	3656	754
123214	3656	759
123215	3656	761
123216	3656	764
123217	3656	768
123218	3656	772
123219	3656	777
123220	3656	783
123221	3656	787
123222	3656	789
123223	3656	792
123224	3656	794
123225	3656	807
123226	3656	811
123227	3656	819
123228	3656	823
123229	3656	828
123230	3656	831
123231	3656	835
123232	3656	841
123233	3656	844
123234	3656	847
123235	3656	850
123236	3656	853
123237	3656	857
123238	3656	860
123239	3656	871
123240	3656	874
123241	3657	732
123242	3657	734
123243	3657	740
123244	3657	744
123245	3657	746
123246	3657	750
123247	3657	754
123248	3657	758
123249	3657	761
123250	3657	764
123251	3657	768
123252	3657	772
123253	3657	777
123254	3657	785
123255	3657	787
123256	3657	789
123257	3657	793
123258	3657	794
123259	3657	807
123260	3657	811
123261	3657	819
123262	3657	822
123263	3657	828
123264	3657	831
123265	3657	835
123266	3657	841
123267	3657	844
123268	3657	847
123269	3657	850
123270	3657	853
123271	3657	857
123272	3657	860
123273	3657	871
123274	3657	874
123275	3658	732
123276	3658	734
123277	3658	740
123278	3658	744
123279	3658	746
123280	3658	749
123281	3658	754
123282	3658	759
123283	3658	761
123284	3658	764
123285	3658	768
123286	3658	772
123287	3658	777
123288	3658	785
123289	3658	787
123290	3658	790
123291	3658	793
123292	3658	794
123293	3658	806
123294	3658	811
123295	3658	819
123296	3658	823
123297	3658	828
123298	3658	831
123299	3658	836
123300	3658	841
123301	3658	845
123302	3658	846
123303	3658	851
123304	3658	852
123305	3658	859
123306	3658	860
123307	3658	871
123308	3658	874
123309	3659	732
123310	3659	734
123311	3659	740
123312	3659	744
123313	3659	747
123314	3659	749
123315	3659	753
123316	3659	759
123317	3659	761
123318	3659	764
123319	3659	768
123320	3659	772
123321	3659	777
123322	3659	785
123323	3659	787
123324	3659	789
123325	3659	792
123326	3659	794
123327	3659	808
123328	3659	811
123329	3659	819
123330	3659	822
123331	3659	828
123332	3659	832
123333	3659	835
123334	3659	841
123335	3659	844
123336	3659	847
123337	3659	850
123338	3659	854
123339	3659	856
123340	3659	860
123341	3659	871
123342	3659	874
123343	3660	732
123344	3660	734
123345	3660	740
123346	3660	743
123347	3660	747
123348	3660	750
123349	3660	754
123350	3660	759
123351	3660	761
123352	3660	764
123353	3660	768
123354	3660	772
123355	3660	777
123356	3660	786
123357	3660	787
123358	3660	789
123359	3660	793
123360	3660	794
123361	3660	808
123362	3660	811
123363	3660	819
123364	3660	822
123365	3660	828
123366	3660	831
123367	3660	835
123368	3660	841
123369	3660	844
123370	3660	847
123371	3660	850
123372	3660	854
123373	3660	856
123374	3660	860
123375	3660	871
123376	3660	874
123377	3661	732
123378	3661	734
123379	3661	740
123380	3661	744
123381	3661	746
123382	3661	749
123383	3661	753
123384	3661	759
123385	3661	761
123386	3661	764
123387	3661	768
123388	3661	772
123389	3661	777
123390	3661	786
123391	3661	787
123392	3661	789
123393	3661	793
123394	3661	794
123395	3661	808
123396	3661	811
123397	3661	819
123398	3661	823
123399	3661	828
123400	3661	832
123401	3661	835
123402	3661	841
123403	3661	844
123404	3661	848
123405	3661	850
123406	3661	854
123407	3661	856
123408	3661	860
123409	3661	871
123410	3661	874
123411	3662	732
123412	3662	734
123413	3662	740
123414	3662	744
123415	3662	746
123416	3662	750
123417	3662	754
123418	3662	758
123419	3662	761
123420	3662	764
123421	3662	768
123422	3662	775
123423	3662	777
123424	3662	785
123425	3662	788
123426	3662	790
123427	3662	793
123428	3662	794
123429	3662	808
123430	3662	814
123431	3662	819
123432	3662	823
123433	3662	828
123434	3662	830
123435	3662	835
123436	3662	841
123437	3662	844
123438	3662	848
123439	3662	850
123440	3662	854
123441	3662	856
123442	3662	860
123443	3662	871
123444	3662	874
123445	3663	732
123446	3663	735
123447	3663	737
123448	3663	741
123449	3663	744
123450	3663	746
123451	3663	750
123452	3663	754
123453	3663	759
123454	3663	761
123455	3663	764
123456	3663	768
123457	3663	774
123458	3663	777
123459	3663	786
123460	3663	788
123461	3663	790
123462	3663	793
123463	3663	794
123464	3663	808
123465	3663	814
123466	3663	819
123467	3663	822
123468	3663	828
123469	3663	831
123470	3663	836
123471	3663	842
123472	3663	845
123473	3663	848
123474	3663	851
123475	3663	854
123476	3663	857
123477	3663	860
123478	3663	871
123479	3663	874
123480	3664	732
123481	3664	734
123482	3664	740
123483	3664	744
123484	3664	745
123485	3664	749
123486	3664	754
123487	3664	760
123488	3664	761
123489	3664	764
123490	3664	768
123491	3664	772
123492	3664	777
123493	3664	786
123494	3664	787
123495	3664	789
123496	3664	793
123497	3664	794
123498	3664	808
123499	3664	811
123500	3664	819
123501	3664	823
123502	3664	828
123503	3664	832
123504	3664	835
123505	3664	841
123506	3664	845
123507	3664	847
123508	3664	851
123509	3664	853
123510	3664	858
123511	3664	860
123512	3664	871
123513	3664	874
123514	3665	732
123515	3665	734
123516	3665	740
123517	3665	744
123518	3665	746
123519	3665	749
123520	3665	753
123521	3665	757
123522	3665	761
123523	3665	765
123524	3665	770
123525	3665	775
123526	3665	777
123527	3665	784
123528	3665	787
123529	3665	789
123530	3665	793
123531	3665	795
123532	3665	796
123533	3665	801
123534	3665	807
123535	3665	815
123536	3665	819
123537	3665	823
123538	3665	827
123539	3665	836
123540	3665	842
123541	3665	845
123542	3665	847
123543	3665	851
123544	3665	854
123545	3665	857
123546	3665	860
123547	3665	871
123548	3665	874
123549	3666	732
123550	3666	734
123551	3666	740
123552	3666	743
123553	3666	746
123554	3666	749
123555	3666	754
123556	3666	756
123557	3666	761
123558	3666	764
123559	3666	768
123560	3666	772
123561	3666	777
123562	3666	783
123563	3666	787
123564	3666	789
123565	3666	792
123566	3666	794
123567	3666	808
123568	3666	811
123569	3666	818
123570	3666	823
123571	3666	827
123572	3666	830
123573	3666	835
123574	3666	841
123575	3666	845
123576	3666	847
123577	3666	851
123578	3666	853
123579	3666	857
123580	3666	860
123581	3666	871
123582	3666	874
123583	3667	732
123584	3667	734
123585	3667	740
123586	3667	744
123587	3667	746
123588	3667	749
123589	3667	754
123590	3667	759
123591	3667	761
123592	3667	766
123593	3667	771
123594	3667	776
123595	3667	781
123596	3667	786
123597	3667	787
123598	3667	790
123599	3667	792
123600	3667	794
123601	3667	808
123602	3667	816
123603	3667	819
123604	3667	823
123605	3667	828
123606	3667	832
123607	3667	839
123608	3667	842
123609	3667	845
123610	3667	848
123611	3667	851
123612	3667	854
123613	3667	857
123614	3667	860
123615	3667	871
123616	3667	874
123617	3668	731
123618	3668	734
123619	3668	740
123620	3668	744
123621	3668	746
123622	3668	749
123623	3668	753
123624	3668	759
123625	3668	761
123626	3668	764
123627	3668	768
123628	3668	772
123629	3668	777
123630	3668	786
123631	3668	787
123632	3668	789
123633	3668	793
123634	3668	795
123635	3668	800
123636	3668	805
123637	3668	808
123638	3668	811
123639	3668	819
123640	3668	822
123641	3668	828
123642	3668	832
123643	3668	835
123644	3668	840
123645	3668	843
123646	3668	847
123647	3668	849
123648	3668	853
123649	3668	856
123650	3668	860
123651	3668	871
123652	3668	874
123653	3669	732
123654	3669	734
123655	3669	740
123656	3669	744
123657	3669	746
123658	3669	749
123659	3669	754
123660	3669	759
123661	3669	761
123662	3669	764
123663	3669	769
123664	3669	775
123665	3669	777
123666	3669	786
123667	3669	787
123668	3669	789
123669	3669	792
123670	3669	794
123671	3669	808
123672	3669	814
123673	3669	818
123674	3669	822
123675	3669	828
123676	3669	832
123677	3669	835
123678	3669	841
123679	3669	845
123680	3669	847
123681	3669	851
123682	3669	853
123683	3669	857
123684	3669	860
123685	3669	871
123686	3669	874
123687	3670	732
123688	3670	734
123689	3670	740
123690	3670	744
123691	3670	746
123692	3670	750
123693	3670	754
123694	3670	759
123695	3670	761
123696	3670	764
123697	3670	768
123698	3670	772
123699	3670	777
123700	3670	786
123701	3670	787
123702	3670	789
123703	3670	793
123704	3670	794
123705	3670	808
123706	3670	811
123707	3670	819
123708	3670	822
123709	3670	828
123710	3670	832
123711	3670	835
123712	3670	841
123713	3670	844
123714	3670	848
123715	3670	850
123716	3670	854
123717	3670	856
123718	3670	860
123719	3670	871
123720	3670	874
123721	3671	732
123722	3671	734
123723	3671	740
123724	3671	744
123725	3671	746
123726	3671	750
123727	3671	754
123728	3671	756
123729	3671	761
123730	3671	764
123731	3671	768
123732	3671	772
123733	3671	777
123734	3671	786
123735	3671	787
123736	3671	789
123737	3671	793
123738	3671	794
123739	3671	809
123740	3671	811
123741	3671	819
123742	3671	822
123743	3671	828
123744	3671	831
123745	3671	835
123746	3671	842
123747	3671	845
123748	3671	848
123749	3671	851
123750	3671	854
123751	3671	857
123752	3671	860
123753	3671	871
123754	3671	874
123755	3672	732
123756	3672	734
123757	3672	740
123758	3672	743
123759	3672	746
123760	3672	749
123761	3672	754
123762	3672	756
123763	3672	761
123764	3672	764
123765	3672	768
123766	3672	772
123767	3672	777
123768	3672	784
123769	3672	787
123770	3672	789
123771	3672	791
123772	3672	794
123773	3672	807
123774	3672	811
123775	3672	818
123776	3672	822
123777	3672	827
123778	3672	830
123779	3672	835
123780	3672	841
123781	3672	844
123782	3672	848
123783	3672	850
123784	3672	854
123785	3672	856
123786	3672	860
123787	3672	871
123788	3672	874
123789	3673	732
123790	3673	734
123791	3673	740
123792	3673	743
123793	3673	746
123794	3673	749
123795	3673	754
123796	3673	756
123797	3673	761
123798	3673	764
123799	3673	768
123800	3673	772
123801	3673	777
123802	3673	784
123803	3673	787
123804	3673	789
123805	3673	792
123806	3673	794
123807	3673	808
123808	3673	811
123809	3673	818
123810	3673	822
123811	3673	827
123812	3673	831
123813	3673	835
123814	3673	860
123815	3673	871
123816	3673	874
123817	3674	732
123818	3674	734
123819	3674	740
123820	3674	743
123821	3674	746
123822	3674	749
123823	3674	755
123824	3674	757
123825	3674	761
123826	3674	764
123827	3674	768
123828	3674	772
123829	3674	777
123830	3674	784
123831	3674	787
123832	3674	789
123833	3674	792
123834	3674	794
123835	3674	808
123836	3674	811
123837	3674	818
123838	3674	822
123839	3674	828
123840	3674	830
123841	3674	835
123842	3674	841
123843	3674	845
123844	3674	847
123845	3674	851
123846	3674	853
123847	3674	858
123848	3674	860
123849	3674	871
123850	3674	874
123851	3675	732
123852	3675	734
123853	3675	740
123854	3675	744
123855	3675	746
123856	3675	749
123857	3675	753
123858	3675	759
123859	3675	761
123860	3675	764
123861	3675	768
123862	3675	772
123863	3675	777
123864	3675	786
123865	3675	788
123866	3675	789
123867	3675	793
123868	3675	794
123869	3675	808
123870	3675	811
123871	3675	819
123872	3675	823
123873	3675	828
123874	3675	831
123875	3675	835
123876	3675	841
123877	3675	844
123878	3675	847
123879	3675	850
123880	3675	854
123881	3675	856
123882	3675	860
123883	3675	871
123884	3675	874
123885	3676	732
123886	3676	734
123887	3676	740
123888	3676	743
123889	3676	746
123890	3676	749
123891	3676	754
123892	3676	759
123893	3676	761
123894	3676	764
123895	3676	768
123896	3676	773
123897	3676	777
123898	3676	783
123899	3676	787
123900	3676	789
123901	3676	792
123902	3676	794
123903	3676	809
123904	3676	813
123905	3676	819
123906	3676	822
123907	3676	827
123908	3676	836
123909	3676	841
123910	3676	844
123911	3676	847
123912	3676	850
123913	3676	854
123914	3676	856
123915	3676	860
123916	3676	871
123917	3676	873
123918	3676	874
123919	3677	732
123920	3677	734
123921	3677	740
123922	3677	743
123923	3677	746
123924	3677	748
123925	3677	752
123926	3677	758
123927	3677	761
123928	3677	764
123929	3677	768
123930	3677	775
123931	3677	781
123932	3677	785
123933	3677	787
123934	3677	789
123935	3677	793
123936	3677	795
123937	3677	797
123938	3677	801
123939	3677	806
123940	3677	814
123941	3677	819
123942	3677	823
123943	3677	827
123944	3677	830
123945	3677	835
123946	3677	841
123947	3677	845
123948	3677	846
123949	3677	851
123950	3677	852
123951	3677	858
123952	3677	860
123953	3677	871
123954	3677	874
123955	3678	732
123956	3678	734
123957	3678	740
123958	3678	744
123959	3678	746
123960	3678	749
123961	3678	754
123962	3678	759
123963	3678	761
123964	3678	766
123965	3678	771
123966	3678	776
123967	3678	781
123968	3678	785
123969	3678	787
123970	3678	790
123971	3678	792
123972	3678	794
123973	3678	808
123974	3678	816
123975	3678	819
123976	3678	823
123977	3678	828
123978	3678	832
123979	3678	839
123980	3678	842
123981	3678	845
123982	3678	848
123983	3678	851
123984	3678	854
123985	3678	857
123986	3678	860
123987	3678	871
123988	3678	874
123989	3679	732
123990	3679	734
123991	3679	740
123992	3679	744
123993	3679	745
123994	3679	749
123995	3679	754
123996	3679	759
123997	3679	761
123998	3679	764
123999	3679	768
124000	3679	772
124001	3679	777
124002	3679	786
124003	3679	787
124004	3679	789
124005	3679	793
124006	3679	794
124007	3679	808
124008	3679	811
124009	3679	819
124010	3679	822
124011	3679	828
124012	3679	831
124013	3679	835
124014	3679	841
124015	3679	844
124016	3679	847
124017	3679	850
124018	3679	853
124019	3679	857
124020	3679	860
124021	3679	871
124022	3679	874
124023	3680	732
124024	3680	734
124025	3680	740
124026	3680	744
124027	3680	747
124028	3680	750
124029	3680	755
124030	3680	756
124031	3680	761
124032	3680	764
124033	3680	768
124034	3680	772
124035	3680	777
124036	3680	783
124037	3680	787
124038	3680	789
124039	3680	792
124040	3680	794
124041	3680	806
124042	3680	811
124043	3680	819
124044	3680	823
124045	3680	827
124046	3680	830
124047	3680	835
124048	3680	841
124049	3680	845
124050	3680	847
124051	3680	851
124052	3680	853
124053	3680	858
124054	3680	860
124055	3680	871
124056	3680	874
124057	3681	732
124058	3681	734
124059	3681	740
124060	3681	744
124061	3681	746
124062	3681	749
124063	3681	754
124064	3681	759
124065	3681	761
124066	3681	766
124067	3681	771
124068	3681	776
124069	3681	781
124070	3681	786
124071	3681	787
124072	3681	790
124073	3681	792
124074	3681	794
124075	3681	809
124076	3681	816
124077	3681	818
124078	3681	821
124079	3681	828
124080	3681	832
124081	3681	839
124082	3681	841
124083	3681	844
124084	3681	847
124085	3681	850
124086	3681	854
124087	3681	856
124088	3681	860
124089	3681	871
124090	3681	874
124091	3682	732
124092	3682	734
124093	3682	740
124094	3682	744
124095	3682	746
124096	3682	750
124097	3682	754
124098	3682	760
124099	3682	761
124100	3682	767
124101	3682	771
124102	3682	776
124103	3682	781
124104	3682	786
124105	3682	787
124106	3682	790
124107	3682	792
124108	3682	794
124109	3682	809
124110	3682	816
124111	3682	819
124112	3682	822
124113	3682	828
124114	3682	832
124115	3682	839
124116	3682	842
124117	3682	845
124118	3682	848
124119	3682	851
124120	3682	854
124121	3682	857
124122	3682	860
124123	3682	871
124124	3682	874
124125	3683	732
124126	3683	734
124127	3683	740
124128	3683	743
124129	3683	746
124130	3683	749
124131	3683	754
124132	3683	758
124133	3683	761
124134	3683	764
124135	3683	768
124136	3683	772
124137	3683	777
124138	3683	783
124139	3683	787
124140	3683	789
124141	3683	792
124142	3683	794
124143	3683	808
124144	3683	811
124145	3683	819
124146	3683	822
124147	3683	827
124148	3683	830
124149	3683	835
124150	3683	842
124151	3683	845
124152	3683	848
124153	3683	851
124154	3683	854
124155	3683	857
124156	3683	860
124157	3683	871
124158	3683	872
124159	3683	874
124160	3684	732
124161	3684	734
124162	3684	740
124163	3684	744
124164	3684	746
124165	3684	749
124166	3684	755
124167	3684	758
124168	3684	761
124169	3684	764
124170	3684	768
124171	3684	772
124172	3684	777
124173	3684	785
124174	3684	787
124175	3684	789
124176	3684	792
124177	3684	794
124178	3684	810
124179	3684	811
124180	3684	819
124181	3684	822
124182	3684	828
124183	3684	831
124184	3684	835
124185	3684	841
124186	3684	844
124187	3684	847
124188	3684	850
124189	3684	854
124190	3684	856
124191	3684	860
124192	3684	871
124193	3684	874
124194	3685	732
124195	3685	734
124196	3685	740
124197	3685	744
124198	3685	746
124199	3685	750
124200	3685	755
124201	3685	758
124202	3685	761
124203	3685	764
124204	3685	768
124205	3685	772
124206	3685	777
124207	3685	786
124208	3685	787
124209	3685	789
124210	3685	793
124211	3685	794
124212	3685	808
124213	3685	811
124214	3685	819
124215	3685	823
124216	3685	828
124217	3685	832
124218	3685	835
124219	3685	841
124220	3685	844
124221	3685	847
124222	3685	851
124223	3685	854
124224	3685	857
124225	3685	860
124226	3685	871
124227	3685	874
124228	3686	732
124229	3686	734
124230	3686	740
124231	3686	744
124232	3686	746
124233	3686	749
124234	3686	755
124235	3686	758
124236	3686	761
124237	3686	764
124238	3686	768
124239	3686	772
124240	3686	777
124241	3686	786
124242	3686	787
124243	3686	789
124244	3686	793
124245	3686	794
124246	3686	808
124247	3686	811
124248	3686	819
124249	3686	823
124250	3686	828
124251	3686	831
124252	3686	835
124253	3686	842
124254	3686	844
124255	3686	848
124256	3686	850
124257	3686	854
124258	3686	856
124259	3686	860
124260	3686	871
124261	3686	874
124262	3687	732
124263	3687	734
124264	3687	740
124265	3687	744
124266	3687	746
124267	3687	748
124268	3687	753
124269	3687	760
124270	3687	761
124271	3687	764
124272	3687	768
124273	3687	772
124274	3687	777
124275	3687	785
124276	3687	787
124277	3687	789
124278	3687	793
124279	3687	794
124280	3687	806
124281	3687	811
124282	3687	819
124283	3687	823
124284	3687	828
124285	3687	832
124286	3687	835
124287	3687	840
124288	3687	844
124289	3687	847
124290	3687	850
124291	3687	853
124292	3687	857
124293	3687	860
124294	3687	871
124295	3687	874
124296	3688	732
124297	3688	734
124298	3688	740
124299	3688	744
124300	3688	746
124301	3688	749
124302	3688	753
124303	3688	760
124304	3688	761
124305	3688	764
124306	3688	768
124307	3688	772
124308	3688	777
124309	3688	786
124310	3688	787
124311	3688	789
124312	3688	792
124313	3688	794
124314	3688	808
124315	3688	811
124316	3688	818
124317	3688	822
124318	3688	828
124319	3688	832
124320	3688	835
124321	3688	841
124322	3688	844
124323	3688	847
124324	3688	850
124325	3688	853
124326	3688	857
124327	3688	860
124328	3688	871
124329	3688	874
124330	3689	732
124331	3689	734
124332	3689	740
124333	3689	744
124334	3689	745
124335	3689	749
124336	3689	755
124337	3689	756
124338	3689	761
124339	3689	764
124340	3689	768
124341	3689	772
124342	3689	777
124343	3689	784
124344	3689	787
124345	3689	789
124346	3689	792
124347	3689	794
124348	3689	807
124349	3689	811
124350	3689	819
124351	3689	822
124352	3689	827
124353	3689	829
124354	3689	835
124355	3689	860
124356	3689	871
124357	3689	874
124358	3690	732
124359	3690	734
124360	3690	740
124361	3690	743
124362	3690	746
124363	3690	748
124364	3690	753
124365	3690	760
124366	3690	761
124367	3690	765
124368	3690	770
124369	3690	776
124370	3690	781
124371	3690	785
124372	3690	787
124373	3690	789
124374	3690	792
124375	3690	795
124376	3690	796
124377	3690	802
124378	3690	807
124379	3690	815
124380	3690	818
124381	3690	822
124382	3690	828
124383	3690	832
124384	3690	836
124385	3690	840
124386	3690	844
124387	3690	847
124388	3690	850
124389	3690	853
124390	3690	856
124391	3690	860
124392	3690	871
124393	3690	874
124394	3691	732
124395	3691	734
124396	3691	740
124397	3691	744
124398	3691	746
124399	3691	750
124400	3691	753
124401	3691	758
124402	3691	761
124403	3691	764
124404	3691	768
124405	3691	772
124406	3691	777
124407	3691	786
124408	3691	787
124409	3691	789
124410	3691	792
124411	3691	794
124412	3691	809
124413	3691	811
124414	3691	819
124415	3691	823
124416	3691	828
124417	3691	832
124418	3691	835
124419	3691	841
124420	3691	844
124421	3691	847
124422	3691	850
124423	3691	854
124424	3691	856
124425	3691	860
124426	3691	871
124427	3691	874
124428	3692	733
124429	3692	734
124430	3692	740
124431	3692	743
124432	3692	746
124433	3692	749
124434	3692	754
124435	3692	757
124436	3692	761
124437	3692	764
124438	3692	768
124439	3692	772
124440	3692	777
124441	3692	783
124442	3692	787
124443	3692	789
124444	3692	792
124445	3692	794
124446	3692	806
124447	3692	811
124448	3692	818
124449	3692	823
124450	3692	827
124451	3692	831
124452	3692	835
124453	3692	841
124454	3692	843
124455	3692	847
124456	3692	849
124457	3692	853
124458	3692	856
124459	3692	860
124460	3692	871
124461	3692	874
124462	3693	732
124463	3693	734
124464	3693	740
124465	3693	744
124466	3693	746
124467	3693	750
124468	3693	755
124469	3693	759
124470	3693	761
124471	3693	764
124472	3693	769
124473	3693	774
124474	3693	777
124475	3693	786
124476	3693	788
124477	3693	789
124478	3693	793
124479	3693	795
124480	3693	796
124481	3693	801
124482	3693	808
124483	3693	814
124484	3693	819
124485	3693	823
124486	3693	828
124487	3693	832
124488	3693	836
124489	3693	841
124490	3693	844
124491	3693	848
124492	3693	850
124493	3693	854
124494	3693	856
124495	3693	860
124496	3693	871
124497	3693	874
124498	3694	732
124499	3694	734
124500	3694	740
124501	3694	744
124502	3694	747
124503	3694	749
124504	3694	753
124505	3694	759
124506	3694	761
124507	3694	764
124508	3694	768
124509	3694	772
124510	3694	777
124511	3694	785
124512	3694	787
124513	3694	789
124514	3694	792
124515	3694	794
124516	3694	809
124517	3694	811
124518	3694	819
124519	3694	822
124520	3694	826
124521	3694	833
124522	3694	835
124523	3694	841
124524	3694	844
124525	3694	847
124526	3694	850
124527	3694	853
124528	3694	857
124529	3694	860
124530	3694	871
124531	3694	874
124532	3695	732
124533	3695	734
124534	3695	740
124535	3695	742
124536	3695	746
124537	3695	750
124538	3695	754
124539	3695	757
124540	3695	761
124541	3695	764
124542	3695	768
124543	3695	774
124544	3695	777
124545	3695	782
124546	3695	787
124547	3695	789
124548	3695	792
124549	3695	794
124550	3695	807
124551	3695	814
124552	3695	819
124553	3695	822
124554	3695	828
124555	3695	835
124556	3695	842
124557	3695	845
124558	3695	848
124559	3695	851
124560	3695	854
124561	3695	857
124562	3695	860
124563	3695	871
124564	3695	872
124565	3695	874
124566	3696	732
124567	3696	734
124568	3696	740
124569	3696	744
124570	3696	746
124571	3696	749
124572	3696	754
124573	3696	759
124574	3696	761
124575	3696	765
124576	3696	770
124577	3696	775
124578	3696	777
124579	3696	785
124580	3696	787
124581	3696	790
124582	3696	792
124583	3696	794
124584	3696	808
124585	3696	814
124586	3696	818
124587	3696	822
124588	3696	828
124589	3696	831
124590	3696	836
124591	3696	841
124592	3696	844
124593	3696	847
124594	3696	850
124595	3696	853
124596	3696	856
124597	3696	860
124598	3696	871
124599	3696	874
124600	3697	732
124601	3697	734
124602	3697	740
124603	3697	743
124604	3697	746
124605	3697	749
124606	3697	754
124607	3697	758
124608	3697	761
124609	3697	764
124610	3697	768
124611	3697	774
124612	3697	777
124613	3697	785
124614	3697	787
124615	3697	789
124616	3697	793
124617	3697	794
124618	3697	808
124619	3697	814
124620	3697	819
124621	3697	823
124622	3697	827
124623	3697	831
124624	3697	835
124625	3697	841
124626	3697	843
124627	3697	848
124628	3697	849
124629	3697	854
124630	3697	856
124631	3697	860
124632	3697	871
124633	3697	874
124634	3698	732
124635	3698	734
124636	3698	740
124637	3698	744
124638	3698	746
124639	3698	750
124640	3698	754
124641	3698	760
124642	3698	761
124643	3698	764
124644	3698	768
124645	3698	772
124646	3698	777
124647	3698	785
124648	3698	787
124649	3698	789
124650	3698	793
124651	3698	794
124652	3698	808
124653	3698	811
124654	3698	819
124655	3698	822
124656	3698	828
124657	3698	832
124658	3698	835
124659	3698	842
124660	3698	845
124661	3698	848
124662	3698	851
124663	3698	854
124664	3698	857
124665	3698	860
124666	3698	871
124667	3698	874
124668	3699	732
124669	3699	734
124670	3699	740
124671	3699	743
124672	3699	746
124673	3699	750
124674	3699	754
124675	3699	760
124676	3699	761
124677	3699	764
124678	3699	769
124679	3699	774
124680	3699	777
124681	3699	785
124682	3699	787
124683	3699	790
124684	3699	792
124685	3699	795
124686	3699	797
124687	3699	802
124688	3699	809
124689	3699	814
124690	3699	819
124691	3699	822
124692	3699	828
124693	3699	832
124694	3699	836
124695	3699	841
124696	3699	845
124697	3699	847
124698	3699	851
124699	3699	854
124700	3699	857
124701	3699	860
124702	3699	871
124703	3699	874
124704	3700	732
124705	3700	734
124706	3700	740
124707	3700	743
124708	3700	746
124709	3700	749
124710	3700	755
124711	3700	756
124712	3700	761
124713	3700	764
124714	3700	768
124715	3700	772
124716	3700	777
124717	3700	784
124718	3700	787
124719	3700	789
124720	3700	792
124721	3700	794
124722	3700	807
124723	3700	811
124724	3700	818
124725	3700	823
124726	3700	827
124727	3700	830
124728	3700	835
124729	3700	860
124730	3700	871
124731	3700	874
124732	3701	732
124733	3701	734
124734	3701	740
124735	3701	744
124736	3701	746
124737	3701	749
124738	3701	754
124739	3701	760
124740	3701	761
124741	3701	764
124742	3701	768
124743	3701	772
124744	3701	777
124745	3701	785
124746	3701	787
124747	3701	789
124748	3701	792
124749	3701	795
124750	3701	800
124751	3701	802
124752	3701	810
124753	3701	811
124754	3701	819
124755	3701	822
124756	3701	828
124757	3701	832
124758	3701	835
124759	3701	841
124760	3701	845
124761	3701	848
124762	3701	851
124763	3701	854
124764	3701	857
124765	3701	860
124766	3701	871
124767	3701	874
124768	3702	732
124769	3702	734
124770	3702	740
124771	3702	743
124772	3702	746
124773	3702	750
124774	3702	754
124775	3702	759
124776	3702	761
124777	3702	764
124778	3702	768
124779	3702	772
124780	3702	777
124781	3702	785
124782	3702	787
124783	3702	789
124784	3702	792
124785	3702	794
124786	3702	808
124787	3702	811
124788	3702	819
124789	3702	822
124790	3702	828
124791	3702	831
124792	3702	835
124793	3702	841
124794	3702	845
124795	3702	847
124796	3702	851
124797	3702	853
124798	3702	857
124799	3702	860
124800	3702	871
124801	3702	874
124802	3703	732
124803	3703	734
124804	3703	740
124805	3703	744
124806	3703	746
124807	3703	748
124808	3703	754
124809	3703	759
124810	3703	761
124811	3703	764
124812	3703	768
124813	3703	772
124814	3703	777
124815	3703	785
124816	3703	787
124817	3703	789
124818	3703	792
124819	3703	794
124820	3703	808
124821	3703	811
124822	3703	819
124823	3703	822
124824	3703	828
124825	3703	832
124826	3703	835
124827	3703	841
124828	3703	845
124829	3703	847
124830	3703	851
124831	3703	853
124832	3703	857
124833	3703	860
124834	3703	871
124835	3703	874
124836	3704	732
124837	3704	734
124838	3704	740
124839	3704	744
124840	3704	746
124841	3704	749
124842	3704	754
124843	3704	759
124844	3704	761
124845	3704	764
124846	3704	768
124847	3704	772
124848	3704	777
124849	3704	786
124850	3704	787
124851	3704	789
124852	3704	792
124853	3704	794
124854	3704	809
124855	3704	811
124856	3704	819
124857	3704	823
124858	3704	828
124859	3704	832
124860	3704	835
124861	3704	841
124862	3704	844
124863	3704	847
124864	3704	850
124865	3704	854
124866	3704	856
124867	3704	860
124868	3704	871
124869	3704	874
124870	3705	732
124871	3705	734
124872	3705	740
124873	3705	744
124874	3705	746
124875	3705	749
124876	3705	754
124877	3705	759
124878	3705	761
124879	3705	764
124880	3705	768
124881	3705	774
124882	3705	777
124883	3705	785
124884	3705	787
124885	3705	789
124886	3705	792
124887	3705	794
124888	3705	808
124889	3705	814
124890	3705	818
124891	3705	823
124892	3705	828
124893	3705	831
124894	3705	836
124895	3705	841
124896	3705	844
124897	3705	847
124898	3705	850
124899	3705	853
124900	3705	857
124901	3705	860
124902	3705	871
124903	3705	874
124904	3706	732
124905	3706	734
124906	3706	740
124907	3706	743
124908	3706	747
124909	3706	749
124910	3706	753
124911	3706	759
124912	3706	761
124913	3706	764
124914	3706	769
124915	3706	774
124916	3706	777
124917	3706	784
124918	3706	787
124919	3706	790
124920	3706	791
124921	3706	794
124922	3706	809
124923	3706	814
124924	3706	818
124925	3706	821
124926	3706	825
124927	3706	832
124928	3706	836
124929	3706	841
124930	3706	844
124931	3706	847
124932	3706	850
124933	3706	854
124934	3706	856
124935	3706	860
124936	3706	871
124937	3706	874
124938	3707	732
124939	3707	734
124940	3707	740
124941	3707	743
124942	3707	746
124943	3707	749
124944	3707	753
124945	3707	759
124946	3707	761
124947	3707	764
124948	3707	768
124949	3707	772
124950	3707	777
124951	3707	784
124952	3707	787
124953	3707	789
124954	3707	792
124955	3707	794
124956	3707	809
124957	3707	811
124958	3707	818
124959	3707	821
124960	3707	828
124961	3707	832
124962	3707	835
124963	3707	841
124964	3707	844
124965	3707	847
124966	3707	849
124967	3707	854
124968	3707	856
124969	3707	860
124970	3707	871
124971	3707	874
124972	3708	732
124973	3708	734
124974	3708	740
124975	3708	744
124976	3708	746
124977	3708	750
124978	3708	754
124979	3708	758
124980	3708	761
124981	3708	764
124982	3708	768
124983	3708	775
124984	3708	777
124985	3708	785
124986	3708	787
124987	3708	789
124988	3708	793
124989	3708	794
124990	3708	808
124991	3708	814
124992	3708	819
124993	3708	823
124994	3708	827
124995	3708	831
124996	3708	835
124997	3708	842
124998	3708	845
124999	3708	848
125000	3708	851
125001	3708	854
125002	3708	857
125003	3708	860
125004	3708	871
125005	3708	874
125006	3709	732
125007	3709	734
125008	3709	740
125009	3709	744
125010	3709	746
125011	3709	750
125012	3709	754
125013	3709	759
125014	3709	761
125015	3709	764
125016	3709	768
125017	3709	772
125018	3709	777
125019	3709	785
125020	3709	787
125021	3709	789
125022	3709	792
125023	3709	794
125024	3709	808
125025	3709	811
125026	3709	819
125027	3709	823
125028	3709	828
125029	3709	831
125030	3709	835
125031	3709	842
125032	3709	845
125033	3709	847
125034	3709	851
125035	3709	853
125036	3709	858
125037	3709	860
125038	3709	871
125039	3709	874
125040	3710	732
125041	3710	734
125042	3710	740
125043	3710	743
125044	3710	746
125045	3710	749
125046	3710	754
125047	3710	758
125048	3710	761
125049	3710	764
125050	3710	768
125051	3710	772
125052	3710	777
125053	3710	784
125054	3710	787
125055	3710	789
125056	3710	791
125057	3710	794
125058	3710	809
125059	3710	811
125060	3710	818
125061	3710	822
125062	3710	828
125063	3710	831
125064	3710	835
125065	3710	841
125066	3710	844
125067	3710	847
125068	3710	850
125069	3710	853
125070	3710	856
125071	3710	860
125072	3710	871
125073	3710	874
125074	3711	732
125075	3711	734
125076	3711	740
125077	3711	743
125078	3711	746
125079	3711	750
125080	3711	755
125081	3711	758
125082	3711	761
125083	3711	764
125084	3711	768
125085	3711	773
125086	3711	777
125087	3711	784
125088	3711	787
125089	3711	789
125090	3711	793
125091	3711	794
125092	3711	807
125093	3711	816
125094	3711	819
125095	3711	822
125096	3711	828
125097	3711	831
125098	3711	835
125099	3711	841
125100	3711	845
125101	3711	847
125102	3711	851
125103	3711	853
125104	3711	858
125105	3711	860
125106	3711	871
125107	3711	874
125108	3712	732
125109	3712	734
125110	3712	740
125111	3712	743
125112	3712	746
125113	3712	749
125114	3712	754
125115	3712	759
125116	3712	761
125117	3712	765
125118	3712	770
125119	3712	776
125120	3712	781
125121	3712	785
125122	3712	787
125123	3712	790
125124	3712	792
125125	3712	794
125126	3712	808
125127	3712	816
125128	3712	819
125129	3712	823
125130	3712	827
125131	3712	832
125132	3712	839
125133	3712	841
125134	3712	844
125135	3712	848
125136	3712	850
125137	3712	854
125138	3712	856
125139	3712	860
125140	3712	871
125141	3712	874
125142	3713	733
125143	3713	734
125144	3713	740
125145	3713	742
125146	3713	746
125147	3713	749
125148	3713	753
125149	3713	758
125150	3713	761
125151	3713	764
125152	3713	768
125153	3713	772
125154	3713	777
125155	3713	782
125156	3713	787
125157	3713	789
125158	3713	791
125159	3713	794
125160	3713	808
125161	3713	811
125162	3713	817
125163	3713	821
125164	3713	827
125165	3713	831
125166	3713	835
125167	3713	841
125168	3713	845
125169	3713	847
125170	3713	851
125171	3713	853
125172	3713	857
125173	3713	860
125174	3713	871
125175	3713	872
125176	3713	874
125177	3714	732
125178	3714	734
125179	3714	740
125180	3714	743
125181	3714	747
125182	3714	749
125183	3714	753
125184	3714	759
125185	3714	761
125186	3714	764
125187	3714	768
125188	3714	772
125189	3714	777
125190	3714	785
125191	3714	787
125192	3714	789
125193	3714	792
125194	3714	795
125195	3714	798
125196	3714	802
125197	3714	808
125198	3714	811
125199	3714	818
125200	3714	822
125201	3714	828
125202	3714	832
125203	3714	835
125204	3714	841
125205	3714	845
125206	3714	847
125207	3714	851
125208	3714	853
125209	3714	857
125210	3714	860
125211	3714	871
125212	3714	874
125213	3715	732
125214	3715	734
125215	3715	740
125216	3715	743
125217	3715	746
125218	3715	749
125219	3715	753
125220	3715	760
125221	3715	761
125222	3715	764
125223	3715	768
125224	3715	772
125225	3715	777
125226	3715	786
125227	3715	787
125228	3715	789
125229	3715	792
125230	3715	794
125231	3715	809
125232	3715	811
125233	3715	818
125234	3715	822
125235	3715	828
125236	3715	831
125237	3715	835
125238	3715	841
125239	3715	845
125240	3715	847
125241	3715	851
125242	3715	853
125243	3715	857
125244	3715	860
125245	3715	871
125246	3715	874
125247	3716	732
125248	3716	734
125249	3716	740
125250	3716	743
125251	3716	746
125252	3716	748
125253	3716	752
125254	3716	758
125255	3716	761
125256	3716	764
125257	3716	768
125258	3716	772
125259	3716	777
125260	3716	783
125261	3716	787
125262	3716	789
125263	3716	792
125264	3716	794
125265	3716	806
125266	3716	811
125267	3716	819
125268	3716	822
125269	3716	827
125270	3716	831
125271	3716	835
125272	3716	842
125273	3716	845
125274	3716	847
125275	3716	851
125276	3716	853
125277	3716	858
125278	3716	860
125279	3716	871
125280	3716	872
125281	3716	874
125282	3717	732
125283	3717	734
125284	3717	740
125285	3717	743
125286	3717	746
125287	3717	749
125288	3717	754
125289	3717	756
125290	3717	761
125291	3717	764
125292	3717	768
125293	3717	775
125294	3717	777
125295	3717	783
125296	3717	787
125297	3717	789
125298	3717	792
125299	3717	794
125300	3717	808
125301	3717	814
125302	3717	819
125303	3717	822
125304	3717	827
125305	3717	829
125306	3717	835
125307	3717	841
125308	3717	845
125309	3717	847
125310	3717	850
125311	3717	853
125312	3717	857
125313	3717	860
125314	3717	871
125315	3717	872
125316	3717	874
125317	3718	733
125318	3718	735
125319	3718	737
125320	3718	741
125321	3718	744
125322	3718	746
125323	3718	749
125324	3718	754
125325	3718	759
125326	3718	761
125327	3718	767
125328	3718	771
125329	3718	776
125330	3718	781
125331	3718	786
125332	3718	788
125333	3718	790
125334	3718	793
125335	3718	794
125336	3718	808
125337	3718	815
125338	3718	819
125339	3718	823
125340	3718	828
125341	3718	832
125342	3718	838
125343	3718	841
125344	3718	844
125345	3718	847
125346	3718	850
125347	3718	854
125348	3718	856
125349	3718	860
125350	3718	871
125351	3718	872
125352	3718	874
125353	3719	732
125354	3719	734
125355	3719	740
125356	3719	743
125357	3719	746
125358	3719	749
125359	3719	753
125360	3719	759
125361	3719	761
125362	3719	764
125363	3719	768
125364	3719	772
125365	3719	777
125366	3719	784
125367	3719	787
125368	3719	789
125369	3719	792
125370	3719	794
125371	3719	808
125372	3719	811
125373	3719	818
125374	3719	822
125375	3719	828
125376	3719	832
125377	3719	835
125378	3719	841
125379	3719	845
125380	3719	847
125381	3719	851
125382	3719	853
125383	3719	857
125384	3719	860
125385	3719	871
125386	3719	874
125387	3720	732
125388	3720	734
125389	3720	740
125390	3720	743
125391	3720	746
125392	3720	748
125393	3720	752
125394	3720	758
125395	3720	761
125396	3720	764
125397	3720	768
125398	3720	772
125399	3720	777
125400	3720	783
125401	3720	787
125402	3720	789
125403	3720	794
125404	3720	808
125405	3720	811
125406	3720	818
125407	3720	821
125408	3720	828
125409	3720	831
125410	3720	835
125411	3720	840
125412	3720	844
125413	3720	847
125414	3720	851
125415	3720	853
125416	3720	857
125417	3720	860
125418	3720	871
125419	3720	872
125420	3720	874
125421	3721	732
125422	3721	735
125423	3721	737
125424	3721	740
125425	3721	743
125426	3721	746
125427	3721	749
125428	3721	753
125429	3721	759
125430	3721	761
125431	3721	764
125432	3721	768
125433	3721	775
125434	3721	781
125435	3721	784
125436	3721	788
125437	3721	790
125438	3721	792
125439	3721	794
125440	3721	806
125441	3721	815
125442	3721	819
125443	3721	823
125444	3721	827
125445	3721	830
125446	3721	835
125447	3721	841
125448	3721	844
125449	3721	847
125450	3721	850
125451	3721	853
125452	3721	857
125453	3721	860
125454	3721	871
125455	3721	874
125456	3722	732
125457	3722	734
125458	3722	740
125459	3722	743
125460	3722	745
125461	3722	749
125462	3722	753
125463	3722	758
125464	3722	761
125465	3722	764
125466	3722	768
125467	3722	776
125468	3722	781
125469	3722	783
125470	3722	787
125471	3722	789
125472	3722	792
125473	3722	794
125474	3722	806
125475	3722	815
125476	3722	819
125477	3722	822
125478	3722	827
125479	3722	830
125480	3722	835
125481	3722	841
125482	3722	845
125483	3722	846
125484	3722	851
125485	3722	852
125486	3722	859
125487	3722	860
125488	3722	871
125489	3722	872
125490	3722	874
125491	3723	732
125492	3723	734
125493	3723	740
125494	3723	744
125495	3723	747
125496	3723	748
125497	3723	752
125498	3723	760
125499	3723	761
125500	3723	764
125501	3723	768
125502	3723	774
125503	3723	777
125504	3723	782
125505	3723	787
125506	3723	789
125507	3723	793
125508	3723	794
125509	3723	806
125510	3723	814
125511	3723	819
125512	3723	822
125513	3723	825
125514	3723	833
125515	3723	835
125516	3723	840
125517	3723	844
125518	3723	846
125519	3723	851
125520	3723	852
125521	3723	858
125522	3723	860
125523	3724	732
125524	3724	734
125525	3724	740
125526	3724	743
125527	3724	745
125528	3724	748
125529	3724	752
125530	3724	760
125531	3724	761
125532	3724	764
125533	3724	768
125534	3724	772
125535	3724	777
125536	3724	784
125537	3724	787
125538	3724	789
125539	3724	792
125540	3724	794
125541	3724	807
125542	3724	811
125543	3724	819
125544	3724	822
125545	3724	828
125546	3724	833
125547	3724	835
125548	3724	841
125549	3724	843
125550	3724	847
125551	3724	849
125552	3724	853
125553	3724	856
125554	3724	860
125555	3725	732
125556	3725	735
125557	3725	739
125558	3725	741
125559	3725	744
125560	3725	746
125561	3725	749
125562	3725	754
125563	3725	760
125564	3725	761
125565	3725	765
125566	3725	770
125567	3725	775
125568	3725	781
125569	3725	786
125570	3725	788
125571	3725	790
125572	3725	793
125573	3725	794
125574	3725	808
125575	3725	813
125576	3725	819
125577	3725	822
125578	3725	827
125579	3725	833
125580	3725	836
125581	3725	842
125582	3725	845
125583	3725	847
125584	3725	851
125585	3725	853
125586	3725	857
125587	3725	860
125588	3726	732
125589	3726	734
125590	3726	740
125591	3726	744
125592	3726	746
125593	3726	748
125594	3726	753
125595	3726	757
125596	3726	761
125597	3726	764
125598	3726	768
125599	3726	772
125600	3726	777
125601	3726	783
125602	3726	787
125603	3726	789
125604	3726	792
125605	3726	794
125606	3726	808
125607	3726	811
125608	3726	819
125609	3726	822
125610	3726	828
125611	3726	831
125612	3726	835
125613	3726	842
125614	3726	845
125615	3726	848
125616	3726	851
125617	3726	854
125618	3726	857
125619	3726	860
125620	3727	732
125621	3727	734
125622	3727	740
125623	3727	744
125624	3727	746
125625	3727	749
125626	3727	753
125627	3727	759
125628	3727	761
125629	3727	764
125630	3727	769
125631	3727	775
125632	3727	777
125633	3727	783
125634	3727	787
125635	3727	789
125636	3727	793
125637	3727	794
125638	3727	808
125639	3727	814
125640	3727	819
125641	3727	823
125642	3727	828
125643	3727	832
125644	3727	836
125645	3727	842
125646	3727	845
125647	3727	847
125648	3727	851
125649	3727	854
125650	3727	857
125651	3727	860
125652	3728	732
125653	3728	734
125654	3728	740
125655	3728	743
125656	3728	746
125657	3728	749
125658	3728	753
125659	3728	757
125660	3728	761
125661	3728	764
125662	3728	768
125663	3728	772
125664	3728	777
125665	3728	783
125666	3728	787
125667	3728	789
125668	3728	793
125669	3728	795
125670	3728	798
125671	3728	802
125672	3728	808
125673	3728	811
125674	3728	819
125675	3728	822
125676	3728	828
125677	3728	831
125678	3728	835
125679	3728	841
125680	3728	843
125681	3728	847
125682	3728	849
125683	3728	853
125684	3728	856
125685	3728	860
125686	3728	874
125687	3729	732
125688	3729	734
125689	3729	740
125690	3729	744
125691	3729	747
125692	3729	750
125693	3729	754
125694	3729	760
125695	3729	761
125696	3729	764
125697	3729	768
125698	3729	772
125699	3729	777
125700	3729	784
125701	3729	787
125702	3729	789
125703	3729	793
125704	3729	794
125705	3729	808
125706	3729	811
125707	3729	819
125708	3729	822
125709	3729	828
125710	3729	832
125711	3729	835
125712	3729	841
125713	3729	845
125714	3729	847
125715	3729	851
125716	3729	853
125717	3729	858
125718	3729	860
125719	3730	732
125720	3730	734
125721	3730	740
125722	3730	743
125723	3730	746
125724	3730	749
125725	3730	753
125726	3730	760
125727	3730	761
125728	3730	764
125729	3730	768
125730	3730	775
125731	3730	777
125732	3730	784
125733	3730	787
125734	3730	789
125735	3730	793
125736	3730	794
125737	3730	806
125738	3730	815
125739	3730	819
125740	3730	822
125741	3730	828
125742	3730	832
125743	3730	835
125744	3730	840
125745	3730	845
125746	3730	846
125747	3730	851
125748	3730	852
125749	3730	859
125750	3730	860
125751	3731	732
125752	3731	734
125753	3731	740
125754	3731	744
125755	3731	746
125756	3731	750
125757	3731	754
125758	3731	759
125759	3731	761
125760	3731	764
125761	3731	768
125762	3731	772
125763	3731	777
125764	3731	783
125765	3731	787
125766	3731	789
125767	3731	792
125768	3731	794
125769	3731	807
125770	3731	813
125771	3731	819
125772	3731	823
125773	3731	828
125774	3731	831
125775	3731	836
125776	3731	841
125777	3731	845
125778	3731	847
125779	3731	851
125780	3731	853
125781	3731	858
125782	3731	860
125783	3732	732
125784	3732	734
125785	3732	740
125786	3732	744
125787	3732	745
125788	3732	750
125789	3732	755
125790	3732	759
125791	3732	761
125792	3732	764
125793	3732	768
125794	3732	772
125795	3732	777
125796	3732	785
125797	3732	787
125798	3732	789
125799	3732	793
125800	3732	794
125801	3732	807
125802	3732	811
125803	3732	819
125804	3732	823
125805	3732	828
125806	3732	832
125807	3732	835
125808	3732	841
125809	3732	845
125810	3732	846
125811	3732	851
125812	3732	852
125813	3732	859
125814	3732	860
125815	3733	732
125816	3733	734
125817	3733	740
125818	3733	744
125819	3733	746
125820	3733	750
125821	3733	755
125822	3733	756
125823	3733	761
125824	3733	764
125825	3733	768
125826	3733	772
125827	3733	777
125828	3733	784
125829	3733	787
125830	3733	789
125831	3733	793
125832	3733	794
125833	3733	808
125834	3733	811
125835	3733	819
125836	3733	822
125837	3733	828
125838	3733	830
125839	3733	835
125840	3733	841
125841	3733	845
125842	3733	847
125843	3733	851
125844	3733	853
125845	3733	858
125846	3733	860
125847	3734	732
125848	3734	734
125849	3734	740
125850	3734	743
125851	3734	746
125852	3734	748
125853	3734	752
125854	3734	760
125855	3734	761
125856	3734	764
125857	3734	768
125858	3734	772
125859	3734	777
125860	3734	787
125861	3734	789
125862	3734	795
125863	3734	798
125864	3734	804
125865	3734	806
125866	3734	811
125867	3734	819
125868	3734	823
125869	3734	826
125870	3734	835
125871	3734	841
125872	3734	845
125873	3734	846
125874	3734	851
125875	3734	852
125876	3734	859
125877	3734	860
125878	3735	732
125879	3735	734
125880	3735	740
125881	3735	744
125882	3735	746
125883	3735	750
125884	3735	754
125885	3735	756
125886	3735	761
125887	3735	764
125888	3735	768
125889	3735	772
125890	3735	777
125891	3735	783
125892	3735	787
125893	3735	789
125894	3735	793
125895	3735	794
125896	3735	807
125897	3735	811
125898	3735	819
125899	3735	823
125900	3735	828
125901	3735	829
125902	3735	835
125903	3735	841
125904	3735	845
125905	3735	847
125906	3735	851
125907	3735	853
125908	3735	858
125909	3735	860
125910	3736	732
125911	3736	734
125912	3736	740
125913	3736	743
125914	3736	747
125915	3736	749
125916	3736	753
125917	3736	760
125918	3736	761
125919	3736	764
125920	3736	768
125921	3736	775
125922	3736	777
125923	3736	784
125924	3736	787
125925	3736	789
125926	3736	793
125927	3736	794
125928	3736	806
125929	3736	815
125930	3736	819
125931	3736	822
125932	3736	827
125933	3736	832
125934	3736	835
125935	3736	841
125936	3736	845
125937	3736	846
125938	3736	851
125939	3736	852
125940	3736	859
125941	3736	860
125942	3737	732
125943	3737	734
125944	3737	740
125945	3737	743
125946	3737	746
125947	3737	750
125948	3737	754
125949	3737	758
125950	3737	761
125951	3737	764
125952	3737	768
125953	3737	772
125954	3737	777
125955	3737	784
125956	3737	787
125957	3737	789
125958	3737	793
125959	3737	794
125960	3737	807
125961	3737	811
125962	3737	819
125963	3737	822
125964	3737	828
125965	3737	831
125966	3737	835
125967	3737	841
125968	3737	845
125969	3737	847
125970	3737	851
125971	3737	853
125972	3737	858
125973	3737	860
125974	3738	732
125975	3738	734
125976	3738	740
125977	3738	743
125978	3738	746
125979	3738	748
125980	3738	753
125981	3738	757
125982	3738	761
125983	3738	764
125984	3738	768
125985	3738	772
125986	3738	777
125987	3738	783
125988	3738	787
125989	3738	789
125990	3738	792
125991	3738	795
125992	3738	797
125993	3738	802
125994	3738	806
125995	3738	811
125996	3738	819
125997	3738	823
125998	3738	828
125999	3738	831
126000	3738	835
126001	3738	842
126002	3738	844
126003	3738	848
126004	3738	850
126005	3738	854
126006	3738	856
126007	3738	860
126008	3738	871
126009	3738	872
126010	3738	874
126011	3739	731
126012	3739	734
126013	3739	740
126014	3739	744
126015	3739	746
126016	3739	749
126017	3739	755
126018	3739	756
126019	3739	761
126020	3739	764
126021	3739	768
126022	3739	772
126023	3739	777
126024	3739	784
126025	3739	787
126026	3739	789
126027	3739	793
126028	3739	794
126029	3739	807
126030	3739	811
126031	3739	819
126032	3739	823
126033	3739	828
126034	3739	829
126035	3739	835
126036	3739	841
126037	3739	845
126038	3739	847
126039	3739	851
126040	3739	853
126041	3739	858
126042	3739	860
126043	3740	731
126044	3740	734
126045	3740	740
126046	3740	744
126047	3740	746
126048	3740	750
126049	3740	755
126050	3740	759
126051	3740	761
126052	3740	764
126053	3740	768
126054	3740	772
126055	3740	777
126056	3740	784
126057	3740	787
126058	3740	789
126059	3740	793
126060	3740	794
126061	3740	807
126062	3740	811
126063	3740	819
126064	3740	822
126065	3740	828
126066	3740	831
126067	3740	835
126068	3740	841
126069	3740	844
126070	3740	847
126071	3740	850
126072	3740	853
126073	3740	857
126074	3740	860
126075	3741	732
126076	3741	734
126077	3741	740
126078	3741	743
126079	3741	746
126080	3741	749
126081	3741	753
126082	3741	761
126083	3741	764
126084	3741	768
126085	3741	772
126086	3741	777
126087	3741	783
126088	3741	787
126089	3741	789
126090	3741	793
126091	3741	794
126092	3741	806
126093	3741	811
126094	3741	819
126095	3741	822
126096	3741	827
126097	3741	831
126098	3741	835
126099	3741	840
126100	3741	844
126101	3741	846
126102	3741	851
126103	3741	852
126104	3741	858
126105	3741	865
126106	3741	871
126107	3741	872
126108	3741	874
126109	3742	732
126110	3742	734
126111	3742	740
126112	3742	743
126113	3742	746
126114	3742	749
126115	3742	753
126116	3742	759
126117	3742	761
126118	3742	764
126119	3742	768
126120	3742	772
126121	3742	777
126122	3742	783
126123	3742	787
126124	3742	789
126125	3742	792
126126	3742	795
126127	3742	797
126128	3742	802
126129	3742	808
126130	3742	811
126131	3742	819
126132	3742	822
126133	3742	828
126134	3742	832
126135	3742	835
126136	3742	842
126137	3742	845
126138	3742	848
126139	3742	851
126140	3742	854
126141	3742	857
126142	3742	860
126143	3742	871
126144	3742	872
126145	3742	874
126146	3743	732
126147	3743	734
126148	3743	740
126149	3743	742
126150	3743	746
126151	3743	748
126152	3743	752
126153	3743	759
126154	3743	761
126155	3743	764
126156	3743	768
126157	3743	772
126158	3743	777
126159	3743	782
126160	3743	787
126161	3743	789
126162	3743	792
126163	3743	794
126164	3743	806
126165	3743	811
126166	3743	817
126167	3743	821
126168	3743	825
126169	3743	835
126170	3743	841
126171	3743	845
126172	3743	847
126173	3743	851
126174	3743	853
126175	3743	857
126176	3743	860
126177	3743	871
126178	3743	872
126179	3743	874
126180	3744	733
126181	3744	735
126182	3744	737
126183	3744	740
126184	3744	742
126185	3744	746
126186	3744	749
126187	3744	754
126188	3744	758
126189	3744	761
126190	3744	764
126191	3744	768
126192	3744	775
126193	3744	781
126194	3744	783
126195	3744	787
126196	3744	789
126197	3744	792
126198	3744	794
126199	3744	808
126200	3744	815
126201	3744	819
126202	3744	822
126203	3744	828
126204	3744	835
126205	3744	841
126206	3744	844
126207	3744	847
126208	3744	850
126209	3744	853
126210	3744	857
126211	3744	860
126212	3744	871
126213	3744	873
126214	3744	874
126215	3745	732
126216	3745	734
126217	3745	740
126218	3745	743
126219	3745	747
126220	3745	749
126221	3745	754
126222	3745	758
126223	3745	761
126224	3745	764
126225	3745	769
126226	3745	774
126227	3745	777
126228	3745	783
126229	3745	787
126230	3745	789
126231	3745	792
126232	3745	794
126233	3745	808
126234	3745	814
126235	3745	819
126236	3745	822
126237	3745	828
126238	3745	837
126239	3745	842
126240	3745	845
126241	3745	847
126242	3745	851
126243	3745	854
126244	3745	857
126245	3745	860
126246	3745	871
126247	3745	873
126248	3745	874
126249	3746	732
126250	3746	734
126251	3746	740
126252	3746	742
126253	3746	746
126254	3746	749
126255	3746	753
126256	3746	760
126257	3746	761
126258	3746	764
126259	3746	768
126260	3746	772
126261	3746	777
126262	3746	784
126263	3746	787
126264	3746	789
126265	3746	792
126266	3746	794
126267	3746	806
126268	3746	811
126269	3746	819
126270	3746	822
126271	3746	828
126272	3746	832
126273	3746	835
126274	3746	842
126275	3746	845
126276	3746	848
126277	3746	851
126278	3746	854
126279	3746	856
126280	3746	860
126281	3746	871
126282	3746	872
126283	3746	874
126284	3747	732
126285	3747	734
126286	3747	740
126287	3747	743
126288	3747	746
126289	3747	749
126290	3747	753
126291	3747	758
126292	3747	761
126293	3747	764
126294	3747	768
126295	3747	772
126296	3747	777
126297	3747	783
126298	3747	787
126299	3747	789
126300	3747	792
126301	3747	794
126302	3747	808
126303	3747	811
126304	3747	819
126305	3747	822
126306	3747	828
126307	3747	831
126308	3747	835
126309	3747	841
126310	3747	843
126311	3747	848
126312	3747	849
126313	3747	854
126314	3747	856
126315	3747	860
126316	3747	871
126317	3747	872
126318	3747	874
126319	3748	732
126320	3748	734
126321	3748	740
126322	3748	742
126323	3748	746
126324	3748	749
126325	3748	753
126326	3748	756
126327	3748	761
126328	3748	764
126329	3748	768
126330	3748	772
126331	3748	777
126332	3748	782
126333	3748	787
126334	3748	789
126335	3748	792
126336	3748	794
126337	3748	808
126338	3748	811
126339	3748	818
126340	3748	822
126341	3748	828
126342	3748	830
126343	3748	835
126344	3748	841
126345	3748	843
126346	3748	847
126347	3748	849
126348	3748	853
126349	3748	856
126350	3748	860
126351	3748	871
126352	3748	872
126353	3748	874
126354	3749	732
126355	3749	734
126356	3749	740
126357	3749	743
126358	3749	745
126359	3749	748
126360	3749	753
126361	3749	757
126362	3749	761
126363	3749	764
126364	3749	768
126365	3749	772
126366	3749	777
126367	3749	783
126368	3749	787
126369	3749	789
126370	3749	792
126371	3749	794
126372	3749	807
126373	3749	811
126374	3749	819
126375	3749	822
126376	3749	828
126377	3749	830
126378	3749	835
126379	3749	840
126380	3749	845
126381	3749	846
126382	3749	851
126383	3749	852
126384	3749	859
126385	3749	860
126386	3749	871
126387	3749	873
126388	3749	874
126389	3750	732
126390	3750	734
126391	3750	740
126392	3750	743
126393	3750	746
126394	3750	748
126395	3750	753
126396	3750	758
126397	3750	761
126398	3750	764
126399	3750	768
126400	3750	772
126401	3750	777
126402	3750	783
126403	3750	787
126404	3750	789
126405	3750	792
126406	3750	794
126407	3750	808
126408	3750	811
126409	3750	819
126410	3750	822
126411	3750	828
126412	3750	830
126413	3750	835
126414	3750	842
126415	3750	845
126416	3750	848
126417	3750	851
126418	3750	854
126419	3750	857
126420	3750	860
126421	3750	871
126422	3750	872
126423	3750	874
126424	3751	732
126425	3751	734
126426	3751	740
126427	3751	743
126428	3751	746
126429	3751	749
126430	3751	753
126431	3751	758
126432	3751	761
126433	3751	764
126434	3751	768
126435	3751	775
126436	3751	781
126437	3751	784
126438	3751	787
126439	3751	789
126440	3751	792
126441	3751	795
126442	3751	799
126443	3751	802
126444	3751	808
126445	3751	814
126446	3751	819
126447	3751	822
126448	3751	827
126449	3751	831
126450	3751	835
126451	3751	841
126452	3751	845
126453	3751	847
126454	3751	851
126455	3751	853
126456	3751	858
126457	3751	865
126458	3751	871
126459	3751	873
126460	3751	874
126461	3752	732
126462	3752	734
126463	3752	740
126464	3752	743
126465	3752	746
126466	3752	749
126467	3752	753
126468	3752	759
126469	3752	761
126470	3752	764
126471	3752	768
126472	3752	773
126473	3752	777
126474	3752	783
126475	3752	787
126476	3752	789
126477	3752	792
126478	3752	795
126479	3752	799
126480	3752	804
126481	3752	808
126482	3752	814
126483	3752	819
126484	3752	823
126485	3752	828
126486	3752	831
126487	3752	835
126488	3752	840
126489	3752	843
126490	3752	847
126491	3752	849
126492	3752	853
126493	3752	856
126494	3752	860
126495	3752	871
126496	3752	873
126497	3752	874
126498	3753	733
126499	3753	735
126500	3753	737
126501	3753	740
126502	3753	743
126503	3753	745
126504	3753	748
126505	3753	752
126506	3753	759
126507	3753	761
126508	3753	764
126509	3753	768
126510	3753	775
126511	3753	781
126512	3753	783
126513	3753	787
126514	3753	789
126515	3753	793
126516	3753	795
126517	3753	797
126518	3753	802
126519	3753	806
126520	3753	815
126521	3753	819
126522	3753	823
126523	3753	828
126524	3753	830
126525	3753	835
126526	3753	841
126527	3753	845
126528	3753	846
126529	3753	851
126530	3753	852
126531	3753	859
126532	3753	860
126533	3753	871
126534	3753	873
126535	3753	874
126536	3754	733
126537	3754	735
126538	3754	737
126539	3754	741
126540	3754	743
126541	3754	745
126542	3754	748
126543	3754	752
126544	3754	757
126545	3754	761
126546	3754	764
126547	3754	768
126548	3754	775
126549	3754	781
126550	3754	783
126551	3754	787
126552	3754	789
126553	3754	793
126554	3754	794
126555	3754	807
126556	3754	815
126557	3754	819
126558	3754	823
126559	3754	827
126560	3754	830
126561	3754	835
126562	3754	841
126563	3754	845
126564	3754	846
126565	3754	851
126566	3754	852
126567	3754	859
126568	3754	860
126569	3754	871
126570	3754	873
126571	3754	874
126572	3755	732
126573	3755	734
126574	3755	740
126575	3755	743
126576	3755	746
126577	3755	749
126578	3755	753
126579	3755	759
126580	3755	761
126581	3755	764
126582	3755	768
126583	3755	772
126584	3755	777
126585	3755	783
126586	3755	787
126587	3755	789
126588	3755	792
126589	3755	794
126590	3755	808
126591	3755	811
126592	3755	819
126593	3755	822
126594	3755	828
126595	3755	831
126596	3755	835
126597	3755	842
126598	3755	845
126599	3755	848
126600	3755	851
126601	3755	854
126602	3755	857
126603	3755	860
126604	3755	871
126605	3755	872
126606	3755	874
126607	3756	733
126608	3756	735
126609	3756	737
126610	3756	741
126611	3756	744
126612	3756	746
126613	3756	748
126614	3756	752
126615	3756	759
126616	3756	761
126617	3756	764
126618	3756	768
126619	3756	775
126620	3756	781
126621	3756	783
126622	3756	787
126623	3756	789
126624	3756	792
126625	3756	795
126626	3756	797
126627	3756	802
126628	3756	806
126629	3756	814
126630	3756	819
126631	3756	822
126632	3756	825
126633	3756	833
126634	3756	835
126635	3756	858
126636	3756	860
126637	3756	870
126638	3756	872
126639	3756	874
126640	3757	732
126641	3757	735
126642	3757	737
126643	3757	740
126644	3757	742
126645	3757	745
126646	3757	748
126647	3757	752
126648	3757	759
126649	3757	763
126650	3757	764
126651	3757	768
126652	3757	775
126653	3757	781
126654	3757	782
126655	3757	787
126656	3757	789
126657	3757	792
126658	3757	794
126659	3757	807
126660	3757	814
126661	3757	835
126662	3757	858
126663	3757	860
126664	3757	871
126665	3757	873
126666	3757	874
126667	3758	733
126668	3758	735
126669	3758	737
126670	3758	741
126671	3758	744
126672	3758	746
126673	3758	748
126674	3758	753
126675	3758	760
126676	3758	761
126677	3758	764
126678	3758	768
126679	3758	774
126680	3758	781
126681	3758	783
126682	3758	787
126683	3758	789
126684	3758	792
126685	3758	794
126686	3758	806
126687	3758	815
126688	3758	819
126689	3758	822
126690	3758	824
126691	3758	833
126692	3758	835
126693	3758	859
126694	3758	860
126695	3758	871
126696	3758	872
126697	3758	874
126698	3759	732
126699	3759	734
126700	3759	740
126701	3759	742
126702	3759	746
126703	3759	748
126704	3759	753
126705	3759	759
126706	3759	761
126707	3759	764
126708	3759	768
126709	3759	772
126710	3759	777
126711	3759	782
126712	3759	787
126713	3759	789
126714	3759	792
126715	3759	795
126716	3759	797
126717	3759	802
126718	3759	808
126719	3759	811
126720	3759	819
126721	3759	822
126722	3759	826
126723	3759	835
126724	3759	841
126725	3759	845
126726	3759	847
126727	3759	851
126728	3759	853
126729	3759	857
126730	3759	860
126731	3759	871
126732	3759	872
126733	3759	874
126734	3760	732
126735	3760	734
126736	3760	740
126737	3760	742
126738	3760	745
126739	3760	749
126740	3760	753
126741	3760	758
126742	3760	761
126743	3760	764
126744	3760	768
126745	3760	774
126746	3760	777
126747	3760	782
126748	3760	787
126749	3760	789
126750	3760	792
126751	3760	794
126752	3760	807
126753	3760	814
126754	3760	818
126755	3760	822
126756	3760	828
126757	3760	831
126758	3760	835
126759	3760	841
126760	3760	843
126761	3760	847
126762	3760	849
126763	3760	854
126764	3760	856
126765	3760	860
126766	3760	871
126767	3760	872
126768	3760	874
126769	3761	731
126770	3761	734
126771	3761	740
126772	3761	744
126773	3761	746
126774	3761	749
126775	3761	754
126776	3761	761
126777	3761	764
126778	3761	768
126779	3761	772
126780	3761	777
126781	3761	787
126782	3761	789
126783	3761	794
126784	3761	806
126785	3761	811
126786	3761	819
126787	3761	822
126788	3761	827
126789	3761	835
126790	3761	842
126791	3761	844
126792	3761	848
126793	3761	854
126794	3761	856
126795	3761	860
126796	3761	871
126797	3761	872
126798	3761	874
126799	3762	733
126800	3762	734
126801	3762	740
126802	3762	743
126803	3762	746
126804	3762	748
126805	3762	753
126806	3762	759
126807	3762	761
126808	3762	764
126809	3762	768
126810	3762	774
126811	3762	777
126812	3762	783
126813	3762	787
126814	3762	789
126815	3762	793
126816	3762	794
126817	3762	806
126818	3762	815
126819	3762	819
126820	3762	822
126821	3762	827
126822	3762	831
126823	3762	835
126824	3762	840
126825	3762	845
126826	3762	846
126827	3762	851
126828	3762	852
126829	3762	859
126830	3762	860
126831	3762	871
126832	3762	873
126833	3762	874
126834	3763	732
126835	3763	734
126836	3763	740
126837	3763	743
126838	3763	746
126839	3763	748
126840	3763	752
126841	3763	758
126842	3763	761
126843	3763	764
126844	3763	768
126845	3763	772
126846	3763	777
126847	3763	784
126848	3763	787
126849	3763	789
126850	3763	792
126851	3763	794
126852	3763	808
126853	3763	811
126854	3763	840
126855	3763	845
126856	3763	846
126857	3763	851
126858	3763	852
126859	3763	859
126860	3763	860
126861	3764	732
126862	3764	734
126863	3764	740
126864	3764	743
126865	3764	746
126866	3764	749
126867	3764	753
126868	3764	758
126869	3764	761
126870	3764	764
126871	3764	768
126872	3764	772
126873	3764	777
126874	3764	783
126875	3764	787
126876	3764	789
126877	3764	791
126878	3764	794
126879	3764	808
126880	3764	811
126881	3764	818
126882	3764	822
126883	3764	826
126884	3764	831
126885	3764	840
126886	3764	845
126887	3764	846
126888	3764	851
126889	3764	852
126890	3764	859
126891	3764	865
126892	3765	732
126893	3765	734
126894	3765	740
126895	3765	743
126896	3765	745
126897	3765	749
126898	3765	753
126899	3765	758
126900	3765	761
126901	3765	764
126902	3765	768
126903	3765	774
126904	3765	777
126905	3765	783
126906	3765	787
126907	3765	789
126908	3765	792
126909	3765	794
126910	3765	806
126911	3765	815
126912	3765	819
126913	3765	822
126914	3765	826
126915	3765	831
126916	3765	835
126917	3765	840
126918	3765	845
126919	3765	846
126920	3765	851
126921	3765	852
126922	3765	859
126923	3765	860
126924	3766	732
126925	3766	734
126926	3766	740
126927	3766	744
126928	3766	746
126929	3766	749
126930	3766	753
126931	3766	758
126932	3766	761
126933	3766	764
126934	3766	768
126935	3766	772
126936	3766	777
126937	3766	785
126938	3766	787
126939	3766	789
126940	3766	792
126941	3766	794
126942	3766	809
126943	3766	811
126944	3766	819
126945	3766	822
126946	3766	828
126947	3766	832
126948	3766	835
126949	3766	842
126950	3766	845
126951	3766	847
126952	3766	851
126953	3766	854
126954	3766	857
126955	3766	860
126956	3767	732
126957	3767	734
126958	3767	740
126959	3767	742
126960	3767	746
126961	3767	749
126962	3767	753
126963	3767	758
126964	3767	761
126965	3767	764
126966	3767	768
126967	3767	772
126968	3767	777
126969	3767	784
126970	3767	787
126971	3767	789
126972	3767	792
126973	3767	794
126974	3767	808
126975	3767	811
126976	3767	819
126977	3767	822
126978	3767	828
126979	3767	833
126980	3767	835
126981	3767	841
126982	3767	845
126983	3767	847
126984	3767	851
126985	3767	853
126986	3767	857
126987	3767	860
126988	3768	732
126989	3768	734
126990	3768	740
126991	3768	744
126992	3768	747
126993	3768	749
126994	3768	753
126995	3768	757
126996	3768	764
126997	3768	768
126998	3768	772
126999	3768	777
127000	3768	784
127001	3768	787
127002	3768	789
127003	3768	792
127004	3768	794
127005	3768	808
127006	3768	811
127007	3768	819
127008	3768	822
127009	3768	827
127010	3768	830
127011	3768	835
127012	3768	841
127013	3768	844
127014	3768	847
127015	3768	851
127016	3768	853
127017	3768	857
127018	3768	860
127019	3769	732
127020	3769	734
127021	3769	740
127022	3769	744
127023	3769	745
127024	3769	749
127025	3769	753
127026	3769	758
127027	3769	761
127028	3769	764
127029	3769	768
127030	3769	772
127031	3769	777
127032	3769	786
127033	3769	787
127034	3769	789
127035	3769	793
127036	3769	795
127037	3769	800
127038	3769	803
127039	3769	808
127040	3769	811
127041	3769	819
127042	3769	823
127043	3769	828
127044	3769	832
127045	3769	835
127046	3769	841
127047	3769	843
127048	3769	847
127049	3769	849
127050	3769	854
127051	3769	856
127052	3769	860
127053	3770	732
127054	3770	734
127055	3770	740
127056	3770	744
127057	3770	746
127058	3770	750
127059	3770	755
127060	3770	756
127061	3770	761
127062	3770	764
127063	3770	768
127064	3770	772
127065	3770	777
127066	3770	784
127067	3770	787
127068	3770	789
127069	3770	793
127070	3770	794
127071	3770	809
127072	3770	811
127073	3770	819
127074	3770	822
127075	3770	828
127076	3770	830
127077	3770	835
127078	3770	841
127079	3770	844
127080	3770	847
127081	3770	850
127082	3770	854
127083	3770	856
127084	3770	860
127085	3771	732
127086	3771	734
127087	3771	740
127088	3771	743
127089	3771	747
127090	3771	749
127091	3771	753
127092	3771	758
127093	3771	761
127094	3771	764
127095	3771	768
127096	3771	772
127097	3771	777
127098	3771	784
127099	3771	787
127100	3771	789
127101	3771	791
127102	3771	794
127103	3771	808
127104	3771	811
127105	3771	818
127106	3771	821
127107	3771	828
127108	3771	832
127109	3771	835
127110	3771	841
127111	3771	844
127112	3771	847
127113	3771	851
127114	3771	853
127115	3771	857
127116	3771	860
127117	3772	732
127118	3772	734
127119	3772	740
127120	3772	743
127121	3772	746
127122	3772	748
127123	3772	759
127124	3772	761
127125	3772	764
127126	3772	768
127127	3772	772
127128	3772	777
127129	3772	841
127130	3772	843
127131	3772	847
127132	3772	849
127133	3772	854
127134	3772	856
127135	3772	860
127136	3773	732
127137	3773	734
127138	3773	740
127139	3773	743
127140	3773	747
127141	3773	749
127142	3773	753
127143	3773	758
127144	3773	761
127145	3773	764
127146	3773	768
127147	3773	772
127148	3773	777
127149	3773	784
127150	3773	787
127151	3773	789
127152	3773	792
127153	3773	794
127154	3773	809
127155	3773	811
127156	3773	819
127157	3773	821
127158	3773	827
127159	3773	832
127160	3773	835
127161	3773	841
127162	3773	843
127163	3773	847
127164	3773	850
127165	3773	854
127166	3773	856
127167	3773	860
127168	3774	732
127169	3774	734
127170	3774	740
127171	3774	743
127172	3774	747
127173	3774	749
127174	3774	753
127175	3774	758
127176	3774	761
127177	3774	764
127178	3774	768
127179	3774	772
127180	3774	777
127181	3774	784
127182	3774	787
127183	3774	789
127184	3774	792
127185	3774	794
127186	3774	809
127187	3774	811
127188	3774	819
127189	3774	821
127190	3774	828
127191	3774	832
127192	3774	835
127193	3774	841
127194	3774	843
127195	3774	847
127196	3774	849
127197	3774	854
127198	3774	856
127199	3774	860
127200	3775	732
127201	3775	734
127202	3775	740
127203	3775	744
127204	3775	746
127205	3775	749
127206	3775	753
127207	3775	757
127208	3775	761
127209	3775	764
127210	3775	768
127211	3775	772
127212	3775	777
127213	3775	785
127214	3775	787
127215	3775	789
127216	3775	791
127217	3775	794
127218	3775	809
127219	3775	811
127220	3775	818
127221	3775	821
127222	3775	828
127223	3775	832
127224	3775	835
127225	3775	841
127226	3775	844
127227	3775	847
127228	3775	850
127229	3775	854
127230	3775	856
127231	3775	860
127232	3776	732
127233	3776	734
127234	3776	740
127235	3776	743
127236	3776	746
127237	3776	749
127238	3776	753
127239	3776	759
127240	3776	761
127241	3776	764
127242	3776	768
127243	3776	772
127244	3776	777
127245	3776	784
127246	3776	787
127247	3776	789
127248	3776	792
127249	3776	794
127250	3776	808
127251	3776	811
127252	3776	818
127253	3776	822
127254	3776	828
127255	3776	829
127256	3776	835
127257	3776	842
127258	3776	845
127259	3776	847
127260	3776	851
127261	3776	853
127262	3776	858
127263	3776	860
127264	3776	871
127265	3776	874
127266	3777	732
127267	3777	734
127268	3777	740
127269	3777	742
127270	3777	746
127271	3777	749
127272	3777	753
127273	3777	758
127274	3777	761
127275	3777	764
127276	3777	768
127277	3777	772
127278	3777	777
127279	3777	783
127280	3777	787
127281	3777	789
127282	3777	792
127283	3777	794
127284	3777	809
127285	3777	811
127286	3777	819
127287	3777	821
127288	3777	828
127289	3777	833
127290	3777	835
127291	3777	841
127292	3777	843
127293	3777	847
127294	3777	849
127295	3777	854
127296	3777	856
127297	3777	860
127298	3778	732
127299	3778	734
127300	3778	740
127301	3778	742
127302	3778	746
127303	3778	748
127304	3778	753
127305	3778	758
127306	3778	761
127307	3778	764
127308	3778	768
127309	3778	772
127310	3778	777
127311	3778	783
127312	3778	787
127313	3778	789
127314	3778	791
127315	3778	794
127316	3778	806
127317	3778	811
127318	3778	817
127319	3778	821
127320	3778	825
127321	3778	830
127322	3778	835
127323	3778	841
127324	3778	845
127325	3778	847
127326	3778	851
127327	3778	853
127328	3778	857
127329	3778	860
127330	3778	871
127331	3778	872
127332	3778	874
127333	3779	732
127334	3779	734
127335	3779	740
127336	3779	742
127337	3779	746
127338	3779	749
127339	3779	753
127340	3779	758
127341	3779	761
127342	3779	764
127343	3779	768
127344	3779	772
127345	3779	777
127346	3779	783
127347	3779	787
127348	3779	789
127349	3779	792
127350	3779	794
127351	3779	806
127352	3779	811
127353	3779	818
127354	3779	822
127355	3779	827
127356	3779	832
127357	3779	835
127358	3779	841
127359	3779	844
127360	3779	847
127361	3779	850
127362	3779	853
127363	3779	857
127364	3779	860
127365	3779	871
127366	3779	872
127367	3779	874
127368	3780	732
127369	3780	734
127370	3780	740
127371	3780	742
127372	3780	746
127373	3780	749
127374	3780	754
127375	3780	758
127376	3780	761
127377	3780	764
127378	3780	768
127379	3780	772
127380	3780	777
127381	3780	783
127382	3780	787
127383	3780	789
127384	3780	792
127385	3780	794
127386	3780	809
127387	3780	811
127388	3780	819
127389	3780	822
127390	3780	827
127391	3780	835
127392	3780	842
127393	3780	845
127394	3780	848
127395	3780	851
127396	3780	854
127397	3780	857
127398	3780	860
127399	3780	871
127400	3780	872
127401	3780	874
127402	3781	732
127403	3781	734
127404	3781	740
127405	3781	744
127406	3781	746
127407	3781	749
127408	3781	754
127409	3781	758
127410	3781	761
127411	3781	764
127412	3781	768
127413	3781	772
127414	3781	777
127415	3781	783
127416	3781	787
127417	3781	789
127418	3781	793
127419	3781	795
127420	3781	798
127421	3781	804
127422	3781	808
127423	3781	811
127424	3781	819
127425	3781	822
127426	3781	828
127427	3781	831
127428	3781	835
127429	3781	841
127430	3781	845
127431	3781	847
127432	3781	851
127433	3781	853
127434	3781	857
127435	3781	860
127436	3781	871
127437	3781	872
127438	3781	874
127439	3782	732
127440	3782	734
127441	3782	740
127442	3782	744
127443	3782	746
127444	3782	749
127445	3782	753
127446	3782	759
127447	3782	761
127448	3782	767
127449	3782	771
127450	3782	776
127451	3782	781
127452	3782	784
127453	3782	787
127454	3782	790
127455	3782	792
127456	3782	795
127457	3782	800
127458	3782	805
127459	3782	808
127460	3782	816
127461	3782	819
127462	3782	823
127463	3782	827
127464	3782	832
127465	3782	839
127466	3782	842
127467	3782	845
127468	3782	847
127469	3782	851
127470	3782	854
127471	3782	857
127472	3782	860
127473	3782	871
127474	3782	873
127475	3782	874
127476	3783	732
127477	3783	734
127478	3783	740
127479	3783	743
127480	3783	746
127481	3783	748
127482	3783	753
127483	3783	758
127484	3783	761
127485	3783	764
127486	3783	768
127487	3783	772
127488	3783	777
127489	3783	783
127490	3783	787
127491	3783	789
127492	3783	792
127493	3783	794
127494	3783	808
127495	3783	811
127496	3783	819
127497	3783	822
127498	3783	827
127499	3783	835
127500	3783	842
127501	3783	845
127502	3783	847
127503	3783	851
127504	3783	854
127505	3783	857
127506	3783	860
127507	3783	871
127508	3783	872
127509	3783	874
127510	3784	732
127511	3784	734
127512	3784	740
127513	3784	744
127514	3784	746
127515	3784	749
127516	3784	753
127517	3784	759
127518	3784	761
127519	3784	764
127520	3784	768
127521	3784	774
127522	3784	777
127523	3784	783
127524	3784	787
127525	3784	789
127526	3784	792
127527	3784	794
127528	3784	806
127529	3784	815
127530	3784	819
127531	3784	822
127532	3784	827
127533	3784	832
127534	3784	835
127535	3784	840
127536	3784	845
127537	3784	846
127538	3784	851
127539	3784	852
127540	3784	859
127541	3784	860
127542	3784	871
127543	3784	873
127544	3784	874
127545	3785	732
127546	3785	734
127547	3785	740
127548	3785	744
127549	3785	746
127550	3785	749
127551	3785	753
127552	3785	760
127553	3785	761
127554	3785	764
127555	3785	768
127556	3785	774
127557	3785	777
127558	3785	783
127559	3785	787
127560	3785	789
127561	3785	792
127562	3785	794
127563	3785	806
127564	3785	815
127565	3785	819
127566	3785	822
127567	3785	826
127568	3785	832
127569	3785	835
127570	3785	840
127571	3785	844
127572	3785	847
127573	3785	850
127574	3785	853
127575	3785	857
127576	3785	860
127577	3785	871
127578	3785	872
127579	3785	874
127580	3786	733
127581	3786	735
127582	3786	737
127583	3786	741
127584	3786	743
127585	3786	746
127586	3786	749
127587	3786	754
127588	3786	758
127589	3786	761
127590	3786	764
127591	3786	768
127592	3786	775
127593	3786	781
127594	3786	783
127595	3786	787
127596	3786	789
127597	3786	792
127598	3786	795
127599	3786	800
127600	3786	804
127601	3786	807
127602	3786	815
127603	3786	819
127604	3786	822
127605	3786	828
127606	3786	831
127607	3786	835
127608	3786	841
127609	3786	845
127610	3786	847
127611	3786	851
127612	3786	853
127613	3786	858
127614	3786	860
127615	3786	871
127616	3786	872
127617	3786	874
127618	3787	732
127619	3787	734
127620	3787	740
127621	3787	743
127622	3787	746
127623	3787	749
127624	3787	753
127625	3787	758
127626	3787	761
127627	3787	766
127628	3787	770
127629	3787	775
127630	3787	777
127631	3787	783
127632	3787	787
127633	3787	789
127634	3787	792
127635	3787	794
127636	3787	807
127637	3787	814
127638	3787	819
127639	3787	822
127640	3787	827
127641	3787	832
127642	3787	837
127643	3787	842
127644	3787	845
127645	3787	848
127646	3787	851
127647	3787	854
127648	3787	857
127649	3787	860
127650	3787	871
127651	3787	872
127652	3787	874
127653	3788	732
127654	3788	735
127655	3788	737
127656	3788	741
127657	3788	744
127658	3788	746
127659	3788	749
127660	3788	754
127661	3788	760
127662	3788	761
127663	3788	764
127664	3788	768
127665	3788	774
127666	3788	777
127667	3788	785
127668	3788	787
127669	3788	790
127670	3788	793
127671	3788	794
127672	3788	806
127673	3788	814
127674	3788	819
127675	3788	823
127676	3788	828
127677	3788	832
127678	3788	837
127679	3788	841
127680	3788	845
127681	3788	847
127682	3788	851
127683	3788	853
127684	3788	857
127685	3788	863
127686	3788	871
127687	3788	872
127688	3788	874
127689	3789	733
127690	3789	735
127691	3789	739
127692	3789	741
127693	3789	744
127694	3789	746
127695	3789	749
127696	3789	754
127697	3789	759
127698	3789	761
127699	3789	767
127700	3789	771
127701	3789	776
127702	3789	781
127703	3789	785
127704	3789	788
127705	3789	790
127706	3789	792
127707	3789	794
127708	3789	808
127709	3789	816
127710	3789	819
127711	3789	822
127712	3789	828
127713	3789	832
127714	3789	839
127715	3789	841
127716	3789	843
127717	3789	848
127718	3789	849
127719	3789	854
127720	3789	856
127721	3789	868
127722	3789	871
127723	3789	873
127724	3789	876
127725	3790	732
127726	3790	735
127727	3790	737
127728	3790	741
127729	3790	744
127730	3790	746
127731	3790	749
127732	3790	753
127733	3790	759
127734	3790	761
127735	3790	767
127736	3790	771
127737	3790	776
127738	3790	781
127739	3790	786
127740	3790	787
127741	3790	790
127742	3790	793
127743	3790	794
127744	3790	809
127745	3790	816
127746	3790	819
127747	3790	823
127748	3790	828
127749	3790	833
127750	3790	836
127751	3790	841
127752	3790	845
127753	3790	847
127754	3790	851
127755	3790	853
127756	3790	857
127757	3790	868
127758	3790	871
127759	3790	873
127760	3790	876
127761	3791	732
127762	3791	734
127763	3791	740
127764	3791	744
127765	3791	745
127766	3791	748
127767	3791	753
127768	3791	759
127769	3791	761
127770	3791	764
127771	3791	768
127772	3791	775
127773	3791	780
127774	3791	783
127775	3791	787
127776	3791	789
127777	3791	792
127778	3791	794
127779	3791	806
127780	3791	815
127781	3791	819
127782	3791	822
127783	3791	827
127784	3791	832
127785	3791	835
127786	3791	841
127787	3791	845
127788	3791	846
127789	3791	851
127790	3791	852
127791	3791	859
127792	3791	860
127793	3791	871
127794	3791	872
127795	3791	874
127796	3792	732
127797	3792	734
127798	3792	740
127799	3792	743
127800	3792	745
127801	3792	748
127802	3792	752
127803	3792	760
127804	3792	761
127805	3792	764
127806	3792	768
127807	3792	774
127808	3792	781
127809	3792	783
127810	3792	787
127811	3792	789
127812	3792	792
127813	3792	794
127814	3792	806
127815	3792	815
127816	3792	819
127817	3792	823
127818	3792	824
127819	3792	840
127820	3792	844
127821	3792	846
127822	3792	851
127823	3792	852
127824	3792	859
127825	3792	860
127826	3793	733
127827	3793	735
127828	3793	738
127829	3793	741
127830	3793	744
127831	3793	746
127832	3793	749
127833	3793	753
127834	3793	758
127835	3793	761
127836	3793	765
127837	3793	771
127838	3793	776
127839	3793	781
127840	3793	783
127841	3793	787
127842	3793	790
127843	3793	793
127844	3793	794
127845	3793	808
127846	3793	816
127847	3793	819
127848	3793	823
127849	3793	827
127850	3793	831
127851	3793	838
127852	3793	842
127853	3793	845
127854	3793	847
127855	3793	851
127856	3793	853
127857	3793	857
127858	3793	868
127859	3793	871
127860	3793	872
127861	3793	876
127862	3794	731
127863	3794	734
127864	3794	740
127865	3794	744
127866	3794	745
127867	3794	748
127868	3794	752
127869	3794	758
127870	3794	761
127871	3794	764
127872	3794	768
127873	3794	772
127874	3794	777
127875	3794	783
127876	3794	787
127877	3794	789
127878	3794	792
127879	3794	794
127880	3794	807
127881	3794	811
127882	3794	818
127883	3794	823
127884	3794	827
127885	3794	832
127886	3794	835
127887	3794	841
127888	3794	843
127889	3794	847
127890	3794	849
127891	3794	853
127892	3794	856
127893	3794	860
127894	3794	871
127895	3794	872
127896	3794	874
127897	3795	732
127898	3795	734
127899	3795	740
127900	3795	743
127901	3795	746
127902	3795	748
127903	3795	753
127904	3795	758
127905	3795	761
127906	3795	764
127907	3795	768
127908	3795	773
127909	3795	777
127910	3795	783
127911	3795	787
127912	3795	789
127913	3795	792
127914	3795	794
127915	3795	809
127916	3795	814
127917	3795	819
127918	3795	822
127919	3795	826
127920	3795	832
127921	3795	835
127922	3795	841
127923	3795	843
127924	3795	847
127925	3795	849
127926	3795	853
127927	3795	856
127928	3795	860
127929	3795	871
127930	3795	872
127931	3795	874
127932	3796	732
127933	3796	734
127934	3796	740
127935	3796	743
127936	3796	746
127937	3796	749
127938	3796	753
127939	3796	758
127940	3796	761
127941	3796	764
127942	3796	768
127943	3796	773
127944	3796	777
127945	3796	783
127946	3796	787
127947	3796	789
127948	3796	792
127949	3796	794
127950	3796	806
127951	3796	814
127952	3796	819
127953	3796	822
127954	3796	827
127955	3796	831
127956	3796	835
127957	3796	841
127958	3796	845
127959	3796	847
127960	3796	851
127961	3796	853
127962	3796	858
127963	3796	860
127964	3796	871
127965	3796	873
127966	3796	874
127967	3797	732
127968	3797	734
127969	3797	740
127970	3797	743
127971	3797	745
127972	3797	749
127973	3797	754
127974	3797	758
127975	3797	761
127976	3797	764
127977	3797	768
127978	3797	774
127979	3797	781
127980	3797	783
127981	3797	787
127982	3797	789
127983	3797	792
127984	3797	794
127985	3797	806
127986	3797	815
127987	3797	819
127988	3797	822
127989	3797	827
127990	3797	830
127991	3797	834
127992	3797	841
127993	3797	845
127994	3797	846
127995	3797	851
127996	3797	852
127997	3797	859
127998	3797	860
127999	3797	871
128000	3797	873
128001	3797	874
128002	3798	733
128003	3798	735
128004	3798	737
128005	3798	741
128006	3798	743
128007	3798	745
128008	3798	748
128009	3798	752
128010	3798	758
128011	3798	761
128012	3798	764
128013	3798	768
128014	3798	775
128015	3798	781
128016	3798	782
128017	3798	787
128018	3798	789
128019	3798	792
128020	3798	794
128021	3798	808
128022	3798	815
128023	3798	819
128024	3798	822
128025	3798	827
128026	3798	835
128027	3798	841
128028	3798	844
128029	3798	847
128030	3798	850
128031	3798	853
128032	3798	856
128033	3798	860
128034	3798	871
128035	3798	873
128036	3798	874
128037	3799	732
128038	3799	734
128039	3799	740
128040	3799	744
128041	3799	746
128042	3799	749
128043	3799	753
128044	3799	758
128045	3799	761
128046	3799	764
128047	3799	768
128048	3799	772
128049	3799	777
128050	3799	783
128051	3799	787
128052	3799	789
128053	3799	792
128054	3799	794
128055	3799	809
128056	3799	811
128057	3799	819
128058	3799	822
128059	3799	827
128060	3799	835
128061	3799	842
128062	3799	845
128063	3799	848
128064	3799	851
128065	3799	854
128066	3799	857
128067	3799	860
128068	3799	871
128069	3799	872
128070	3799	874
128071	3800	732
128072	3800	734
128073	3800	740
128074	3800	744
128075	3800	746
128076	3800	749
128077	3800	753
128078	3800	758
128079	3800	761
128080	3800	764
128081	3800	768
128082	3800	772
128083	3800	777
128084	3800	783
128085	3800	787
128086	3800	789
128087	3800	792
128088	3800	794
128089	3800	809
128090	3800	811
128091	3800	819
128092	3800	822
128093	3800	827
128094	3800	835
128095	3800	842
128096	3800	845
128097	3800	848
128098	3800	851
128099	3800	854
128100	3800	857
128101	3800	860
128102	3800	871
128103	3800	872
128104	3800	874
128105	3801	732
128106	3801	734
128107	3801	740
128108	3801	743
128109	3801	746
128110	3801	748
128111	3801	753
128112	3801	758
128113	3801	761
128114	3801	764
128115	3801	768
128116	3801	772
128117	3801	777
128118	3801	783
128119	3801	787
128120	3801	789
128121	3801	792
128122	3801	795
128123	3801	798
128124	3801	802
128125	3801	806
128126	3801	811
128127	3801	819
128128	3801	822
128129	3801	828
128130	3801	831
128131	3801	835
128132	3801	841
128133	3801	845
128134	3801	847
128135	3801	851
128136	3801	853
128137	3801	857
128138	3801	860
128139	3801	871
128140	3801	872
128141	3801	874
128142	3802	732
128143	3802	734
128144	3802	740
128145	3802	743
128146	3802	746
128147	3802	749
128148	3802	754
128149	3802	758
128150	3802	761
128151	3802	764
128152	3802	768
128153	3802	776
128154	3802	781
128155	3802	783
128156	3802	787
128157	3802	789
128158	3802	792
128159	3802	795
128160	3802	798
128161	3802	802
128162	3802	808
128163	3802	815
128164	3802	819
128165	3802	822
128166	3802	827
128167	3802	835
128168	3802	841
128169	3802	845
128170	3802	847
128171	3802	851
128172	3802	853
128173	3802	858
128174	3802	865
128175	3802	871
128176	3802	873
128177	3802	874
128178	3803	732
128179	3803	734
128180	3803	740
128181	3803	743
128182	3803	746
128183	3803	749
128184	3803	753
128185	3803	758
128186	3803	761
128187	3803	764
128188	3803	768
128189	3803	772
128190	3803	777
128191	3803	783
128192	3803	787
128193	3803	789
128194	3803	791
128195	3803	794
128196	3803	806
128197	3803	811
128198	3803	818
128199	3803	822
128200	3803	827
128201	3803	831
128202	3803	835
128203	3803	841
128204	3803	845
128205	3803	847
128206	3803	851
128207	3803	853
128208	3803	858
128209	3803	860
128210	3803	871
128211	3803	872
128212	3803	874
128213	3804	732
128214	3804	734
128215	3804	740
128216	3804	743
128217	3804	746
128218	3804	749
128219	3804	753
128220	3804	759
128221	3804	761
128222	3804	764
128223	3804	768
128224	3804	775
128225	3804	780
128226	3804	783
128227	3804	787
128228	3804	789
128229	3804	792
128230	3804	795
128231	3804	796
128232	3804	801
128233	3804	806
128234	3804	815
128235	3804	818
128236	3804	822
128237	3804	826
128238	3804	832
128239	3804	835
128240	3804	842
128241	3804	845
128242	3804	847
128243	3804	851
128244	3804	854
128245	3804	857
128246	3804	860
128247	3804	871
128248	3804	872
128249	3804	874
128250	3805	732
128251	3805	734
128252	3805	740
128253	3805	743
128254	3805	746
128255	3805	748
128256	3805	753
128257	3805	757
128258	3805	761
128259	3805	764
128260	3805	768
128261	3805	772
128262	3805	777
128263	3805	785
128264	3805	787
128265	3805	789
128266	3805	792
128267	3805	794
128268	3805	803
128269	3805	807
128270	3805	811
128271	3805	818
128272	3805	821
128273	3805	827
128274	3805	830
128275	3805	835
128276	3805	841
128277	3805	844
128278	3805	847
128279	3805	850
128280	3805	853
128281	3805	857
128282	3805	860
128283	3805	871
128284	3805	872
128285	3805	874
128286	3806	733
128287	3806	735
128288	3806	737
128289	3806	741
128290	3806	744
128291	3806	746
128292	3806	749
128293	3806	753
128294	3806	758
128295	3806	761
128296	3806	764
128297	3806	768
128298	3806	775
128299	3806	781
128300	3806	783
128301	3806	787
128302	3806	789
128303	3806	793
128304	3806	794
128305	3806	806
128306	3806	815
128307	3806	819
128308	3806	823
128309	3806	828
128310	3806	832
128311	3806	835
128312	3806	841
128313	3806	845
128314	3806	846
128315	3806	851
128316	3806	852
128317	3806	859
128318	3806	865
128319	3806	871
128320	3806	873
128321	3806	876
128322	3807	732
128323	3807	734
128324	3807	740
128325	3807	743
128326	3807	746
128327	3807	749
128328	3807	754
128329	3807	758
128330	3807	761
128331	3807	764
128332	3807	768
128333	3807	772
128334	3807	777
128335	3807	784
128336	3807	787
128337	3807	789
128338	3807	792
128339	3807	794
128340	3807	807
128341	3807	811
128342	3807	819
128343	3807	822
128344	3807	828
128345	3807	831
128346	3807	835
128347	3807	841
128348	3807	844
128349	3807	847
128350	3807	850
128351	3807	853
128352	3807	856
128353	3807	865
128354	3807	871
128355	3807	872
128356	3807	874
128357	3808	732
128358	3808	734
128359	3808	740
128360	3808	744
128361	3808	746
128362	3808	748
128363	3808	752
128364	3808	758
128365	3808	761
128366	3808	764
128367	3808	768
128368	3808	772
128369	3808	777
128370	3808	783
128371	3808	787
128372	3808	789
128373	3808	792
128374	3808	794
128375	3808	806
128376	3808	811
128377	3808	819
128378	3808	822
128379	3808	827
128380	3808	832
128381	3808	835
128382	3808	842
128383	3808	845
128384	3808	848
128385	3808	851
128386	3808	854
128387	3808	857
128388	3808	860
128389	3808	871
128390	3808	872
128391	3808	874
128392	3809	732
128393	3809	734
128394	3809	740
128395	3809	744
128396	3809	746
128397	3809	749
128398	3809	754
128399	3809	759
128400	3809	761
128401	3809	764
128402	3809	770
128403	3809	776
128404	3809	781
128405	3809	786
128406	3809	787
128407	3809	789
128408	3809	793
128409	3809	794
128410	3809	809
128411	3809	815
128412	3809	819
128413	3809	823
128414	3809	828
128415	3809	831
128416	3809	837
128417	3809	842
128418	3809	845
128419	3809	848
128420	3809	851
128421	3809	854
128422	3809	857
128423	3809	860
128424	3809	871
128425	3809	873
128426	3809	874
128427	3810	732
128428	3810	734
128429	3810	740
128430	3810	742
128431	3810	746
128432	3810	749
128433	3810	753
128434	3810	758
128435	3810	761
128436	3810	764
128437	3810	768
128438	3810	772
128439	3810	777
128440	3810	783
128441	3810	787
128442	3810	789
128443	3810	792
128444	3810	794
128445	3810	808
128446	3810	811
128447	3810	818
128448	3810	822
128449	3810	828
128450	3810	831
128451	3810	835
128452	3810	841
128453	3810	843
128454	3810	847
128455	3810	849
128456	3810	853
128457	3810	856
128458	3810	860
128459	3810	871
128460	3810	872
128461	3810	874
128462	3811	732
128463	3811	734
128464	3811	740
128465	3811	743
128466	3811	745
128467	3811	750
128468	3811	754
128469	3811	758
128470	3811	761
128471	3811	764
128472	3811	768
128473	3811	775
128474	3811	781
128475	3811	783
128476	3811	787
128477	3811	789
128478	3811	792
128479	3811	794
128480	3811	806
128481	3811	816
128482	3811	819
128483	3811	822
128484	3811	828
128485	3811	830
128486	3811	835
128487	3811	840
128488	3811	845
128489	3811	846
128490	3811	851
128491	3811	852
128492	3811	859
128493	3811	860
128494	3811	871
128495	3811	873
128496	3811	876
128497	3812	731
128498	3812	734
128499	3812	740
128500	3812	743
128501	3812	746
128502	3812	749
128503	3812	754
128504	3812	759
128505	3812	761
128506	3812	764
128507	3812	768
128508	3812	772
128509	3812	777
128510	3812	784
128511	3812	787
128512	3812	789
128513	3812	792
128514	3812	795
128515	3812	798
128516	3812	801
128517	3812	808
128518	3812	811
128519	3812	819
128520	3812	823
128521	3812	827
128522	3812	832
128523	3812	835
128524	3812	842
128525	3812	845
128526	3812	848
128527	3812	851
128528	3812	854
128529	3812	856
128530	3812	860
128531	3812	871
128532	3812	872
128533	3812	874
128534	3813	733
128535	3813	735
128536	3813	737
128537	3813	741
128538	3813	744
128539	3813	746
128540	3813	750
128541	3813	755
128542	3813	758
128543	3813	761
128544	3813	764
128545	3813	768
128546	3813	775
128547	3813	781
128548	3813	785
128549	3813	788
128550	3813	790
128551	3813	793
128552	3813	794
128553	3813	810
128554	3813	815
128555	3813	819
128556	3813	822
128557	3813	828
128558	3813	831
128559	3813	836
128560	3813	841
128561	3813	844
128562	3813	847
128563	3813	850
128564	3813	853
128565	3813	857
128566	3813	865
128567	3813	871
128568	3813	872
128569	3813	874
128570	3814	732
128571	3814	734
128572	3814	740
128573	3814	742
128574	3814	746
128575	3814	749
128576	3814	754
128577	3814	757
128578	3814	761
128579	3814	764
128580	3814	768
128581	3814	772
128582	3814	777
128583	3814	783
128584	3814	787
128585	3814	789
128586	3814	791
128587	3814	794
128588	3814	808
128589	3814	811
128590	3814	818
128591	3814	822
128592	3814	826
128593	3814	832
128594	3814	835
128595	3814	841
128596	3814	844
128597	3814	847
128598	3814	850
128599	3814	853
128600	3814	857
128601	3814	865
128602	3814	871
128603	3814	872
128604	3814	874
128605	3815	732
128606	3815	734
128607	3815	740
128608	3815	743
128609	3815	746
128610	3815	750
128611	3815	754
128612	3815	760
128613	3815	761
128614	3815	764
128615	3815	768
128616	3815	774
128617	3815	781
128618	3815	783
128619	3815	787
128620	3815	789
128621	3815	793
128622	3815	794
128623	3815	806
128624	3815	815
128625	3815	819
128626	3815	822
128627	3815	827
128628	3815	832
128629	3815	835
128630	3815	841
128631	3815	845
128632	3815	846
128633	3815	851
128634	3815	852
128635	3815	859
128636	3815	860
128637	3815	871
128638	3815	874
128639	3816	731
128640	3816	734
128641	3816	740
128642	3816	743
128643	3816	745
128644	3816	749
128645	3816	754
128646	3816	760
128647	3816	761
128648	3816	764
128649	3816	768
128650	3816	772
128651	3816	777
128652	3816	783
128653	3816	787
128654	3816	789
128655	3816	793
128656	3816	795
128657	3816	798
128658	3816	803
128659	3816	808
128660	3816	811
128661	3816	819
128662	3816	823
128663	3816	826
128664	3816	832
128665	3816	835
128666	3816	841
128667	3816	845
128668	3816	846
128669	3816	851
128670	3816	852
128671	3816	859
128672	3816	860
128673	3816	871
128674	3816	874
128675	3817	731
128676	3817	734
128677	3817	740
128678	3817	744
128679	3817	745
128680	3817	750
128681	3817	755
128682	3817	760
128683	3817	761
128684	3817	764
128685	3817	768
128686	3817	772
128687	3817	777
128688	3817	784
128689	3817	787
128690	3817	789
128691	3817	793
128692	3817	794
128693	3817	808
128694	3817	811
128695	3817	819
128696	3817	823
128697	3817	828
128698	3817	831
128699	3817	835
128700	3817	841
128701	3817	845
128702	3817	846
128703	3817	851
128704	3817	852
128705	3817	859
128706	3817	860
128707	3817	871
128708	3817	874
128709	3818	732
128710	3818	734
128711	3818	740
128712	3818	743
128713	3818	746
128714	3818	749
128715	3818	753
128716	3818	758
128717	3818	761
128718	3818	764
128719	3818	768
128720	3818	772
128721	3818	777
128722	3818	785
128723	3818	787
128724	3818	789
128725	3818	793
128726	3818	794
128727	3818	806
128728	3818	811
128729	3818	819
128730	3818	822
128731	3818	828
128732	3818	830
128733	3818	836
128734	3818	841
128735	3818	845
128736	3818	847
128737	3818	851
128738	3818	853
128739	3818	857
128740	3818	865
128741	3818	871
128742	3818	872
128743	3818	876
128744	3819	733
128745	3819	735
128746	3819	739
128747	3819	741
128748	3819	744
128749	3819	746
128750	3819	749
128751	3819	753
128752	3819	759
128753	3819	761
128754	3819	767
128755	3819	771
128756	3819	776
128757	3819	781
128758	3819	785
128759	3819	787
128760	3819	790
128761	3819	793
128762	3819	794
128763	3819	808
128764	3819	815
128765	3819	819
128766	3819	823
128767	3819	828
128768	3819	833
128769	3819	839
128770	3819	841
128771	3819	844
128772	3819	847
128773	3819	850
128774	3819	853
128775	3819	857
128776	3819	868
128777	3819	871
128778	3819	873
128779	3819	876
128780	3820	732
128781	3820	734
128782	3820	740
128783	3820	743
128784	3820	747
128785	3820	749
128786	3820	753
128787	3820	758
128788	3820	761
128789	3820	764
128790	3820	768
128791	3820	772
128792	3820	777
128793	3820	784
128794	3820	787
128795	3820	789
128796	3820	791
128797	3820	794
128798	3820	808
128799	3820	811
128800	3820	818
128801	3820	822
128802	3820	828
128803	3820	835
128804	3820	841
128805	3820	845
128806	3820	847
128807	3820	851
128808	3820	854
128809	3820	857
128810	3820	860
128811	3820	874
128812	3821	732
128813	3821	735
128814	3821	737
128815	3821	740
128816	3821	744
128817	3821	745
128818	3821	749
128819	3821	753
128820	3821	758
128821	3821	761
128822	3821	764
128823	3821	768
128824	3821	775
128825	3821	781
128826	3821	784
128827	3821	787
128828	3821	789
128829	3821	793
128830	3821	794
128831	3821	806
128832	3821	815
128833	3821	819
128834	3821	823
128835	3821	825
128836	3821	831
128837	3821	835
128838	3821	841
128839	3821	845
128840	3821	846
128841	3821	851
128842	3821	852
128843	3821	859
128844	3821	860
128845	3821	874
128846	3822	731
128847	3822	734
128848	3822	740
128849	3822	744
128850	3822	745
128851	3822	749
128852	3822	753
128853	3822	759
128854	3822	761
128855	3822	764
128856	3822	768
128857	3822	772
128858	3822	777
128859	3822	784
128860	3822	787
128861	3822	789
128862	3822	793
128863	3822	794
128864	3822	807
128865	3822	811
128866	3822	819
128867	3822	823
128868	3822	826
128869	3822	833
128870	3822	835
128871	3822	841
128872	3822	845
128873	3822	846
128874	3822	851
128875	3822	852
128876	3822	859
128877	3822	860
128878	3822	874
128879	3823	731
128880	3823	734
128881	3823	740
128882	3823	743
128883	3823	746
128884	3823	749
128885	3823	754
128886	3823	758
128887	3823	761
128888	3823	764
128889	3823	768
128890	3823	772
128891	3823	777
128892	3823	784
128893	3823	787
128894	3823	789
128895	3823	794
128896	3823	808
128897	3823	811
128898	3823	819
128899	3823	823
128900	3823	828
128901	3823	835
128902	3823	841
128903	3823	845
128904	3823	847
128905	3823	851
128906	3823	852
128907	3823	859
128908	3823	860
128909	3823	874
128910	3824	732
128911	3824	734
128912	3824	740
128913	3824	743
128914	3824	746
128915	3824	748
128916	3824	754
128917	3824	757
128918	3824	761
128919	3824	764
128920	3824	768
128921	3824	772
128922	3824	777
128923	3824	784
128924	3824	787
128925	3824	789
128926	3824	793
128927	3824	794
128928	3824	808
128929	3824	811
128930	3824	819
128931	3824	823
128932	3824	828
128933	3824	835
128934	3824	842
128935	3824	845
128936	3824	848
128937	3824	851
128938	3824	854
128939	3824	857
128940	3824	860
128941	3824	874
128942	3825	732
128943	3825	735
128944	3825	737
128945	3825	741
128946	3825	744
128947	3825	746
128948	3825	750
128949	3825	755
128950	3825	758
128951	3825	761
128952	3825	764
128953	3825	768
128954	3825	772
128955	3825	777
128956	3825	788
128957	3825	789
128958	3825	794
128959	3825	810
128960	3825	811
128961	3825	819
128962	3825	821
128963	3825	828
128964	3825	835
128965	3825	842
128966	3825	844
128967	3825	847
128968	3825	850
128969	3825	854
128970	3825	856
128971	3825	860
128972	3825	874
128973	3826	732
128974	3826	734
128975	3826	740
128976	3826	743
128977	3826	746
128978	3826	748
128979	3826	753
128980	3826	757
128981	3826	761
128982	3826	764
128983	3826	768
128984	3826	772
128985	3826	777
128986	3826	782
128987	3826	787
128988	3826	789
128989	3826	791
128990	3826	794
128991	3826	809
128992	3826	811
128993	3826	818
128994	3826	822
128995	3826	827
128996	3826	832
128997	3826	835
128998	3826	842
128999	3826	844
129000	3826	848
129001	3826	850
129002	3826	854
129003	3826	856
129004	3826	860
129005	3826	874
129006	3827	732
129007	3827	734
129008	3827	740
129009	3827	743
129010	3827	747
129011	3827	749
129012	3827	753
129013	3827	757
129014	3827	761
129015	3827	764
129016	3827	768
129017	3827	772
129018	3827	777
129019	3827	787
129020	3827	789
129021	3827	794
129022	3827	808
129023	3827	811
129024	3827	819
129025	3827	823
129026	3827	828
129027	3827	835
129028	3827	841
129029	3827	844
129030	3827	847
129031	3827	850
129032	3827	854
129033	3827	856
129034	3827	860
129035	3827	874
129036	3828	732
129037	3828	734
129038	3828	740
129039	3828	743
129040	3828	746
129041	3828	748
129042	3828	753
129043	3828	758
129044	3828	761
129045	3828	764
129046	3828	768
129047	3828	772
129048	3828	777
129049	3828	783
129050	3828	787
129051	3828	789
129052	3828	791
129053	3828	794
129054	3828	810
129055	3828	811
129056	3828	818
129057	3828	822
129058	3828	827
129059	3828	835
129060	3828	842
129061	3828	844
129062	3828	848
129063	3828	850
129064	3828	854
129065	3828	856
129066	3828	860
129067	3828	874
129068	3829	732
129069	3829	734
129070	3829	740
129071	3829	744
129072	3829	746
129073	3829	748
129074	3829	752
129075	3829	759
129076	3829	761
129077	3829	764
129078	3829	768
129079	3829	772
129080	3829	777
129081	3829	784
129082	3829	787
129083	3829	789
129084	3829	793
129085	3829	794
129086	3829	808
129087	3829	811
129088	3829	818
129089	3829	822
129090	3829	827
129091	3829	838
129092	3829	841
129093	3829	844
129094	3829	847
129095	3829	850
129096	3829	853
129097	3829	857
129098	3829	868
129099	3829	871
129100	3829	872
129101	3829	876
129102	3830	740
129103	3830	757
129104	3830	785
129105	3830	794
129106	3830	819
129107	3830	849
129108	3830	856
129109	3830	860
129110	3831	733
129111	3831	735
129112	3831	738
129113	3831	741
129114	3831	743
129115	3831	746
129116	3831	749
129117	3831	753
129118	3831	760
129119	3831	761
129120	3831	766
129121	3831	771
129122	3831	776
129123	3831	781
129124	3831	783
129125	3831	787
129126	3831	790
129127	3831	793
129128	3831	794
129129	3831	807
129130	3831	815
129131	3831	819
129132	3831	823
129133	3831	827
129134	3831	832
129135	3831	840
129136	3831	845
129137	3831	846
129138	3831	851
129139	3831	852
129140	3831	859
129141	3831	868
129142	3832	731
129143	3832	734
129144	3832	740
129145	3832	744
129146	3832	745
129147	3832	748
129148	3832	754
129149	3832	759
129150	3832	761
129151	3832	764
129152	3832	768
129153	3832	772
129154	3832	777
129155	3832	787
129156	3832	789
129157	3832	792
129158	3832	794
129159	3832	807
129160	3832	811
129161	3832	819
129162	3832	823
129163	3832	827
129164	3832	832
129165	3832	835
129166	3832	841
129167	3832	845
129168	3832	846
129169	3832	851
129170	3832	852
129171	3832	859
129172	3832	865
129173	3832	871
129174	3833	732
129175	3833	734
129176	3833	740
129177	3833	743
129178	3833	746
129179	3833	749
129180	3833	753
129181	3833	760
129182	3833	761
129183	3833	764
129184	3833	768
129185	3833	772
129186	3833	777
129187	3833	782
129188	3833	787
129189	3833	789
129190	3833	792
129191	3833	794
129192	3833	806
129193	3833	811
129194	3833	818
129195	3833	822
129196	3833	828
129197	3833	832
129198	3833	835
129199	3833	842
129200	3833	845
129201	3833	847
129202	3833	851
129203	3833	853
129204	3833	857
129205	3833	860
129206	3833	871
129207	3833	874
129208	3834	732
129209	3834	734
129210	3834	740
129211	3834	742
129212	3834	746
129213	3834	748
129214	3834	753
129215	3834	759
129216	3834	761
129217	3834	764
129218	3834	768
129219	3834	772
129220	3834	777
129221	3834	782
129222	3834	787
129223	3834	789
129224	3834	792
129225	3834	794
129226	3834	806
129227	3834	811
129228	3834	818
129229	3834	822
129230	3834	828
129231	3834	831
129232	3834	835
129233	3834	840
129234	3834	843
129235	3834	847
129236	3834	849
129237	3834	853
129238	3834	857
129239	3834	860
129240	3835	732
129241	3835	734
129242	3835	740
129243	3835	743
129244	3835	747
129245	3835	749
129246	3835	753
129247	3835	759
129248	3835	761
129249	3835	764
129250	3835	768
129251	3835	772
129252	3835	777
129253	3835	782
129254	3835	787
129255	3835	789
129256	3835	791
129257	3835	794
129258	3835	807
129259	3835	811
129260	3835	818
129261	3835	821
129262	3835	827
129263	3835	832
129264	3835	835
129265	3835	841
129266	3835	844
129267	3835	847
129268	3835	850
129269	3835	853
129270	3835	856
129271	3835	860
129272	3836	732
129273	3836	734
129274	3836	740
129275	3836	743
129276	3836	746
129277	3836	749
129278	3836	753
129279	3836	760
129280	3836	761
129281	3836	764
129282	3836	768
129283	3836	772
129284	3836	777
129285	3836	782
129286	3836	787
129287	3836	789
129288	3836	792
129289	3836	794
129290	3836	808
129291	3836	811
129292	3836	818
129293	3836	821
129294	3836	828
129295	3836	832
129296	3836	835
129297	3836	841
129298	3836	844
129299	3836	847
129300	3836	850
129301	3836	853
129302	3836	856
129303	3836	860
129304	3837	732
129305	3837	734
129306	3837	740
129307	3837	744
129308	3837	746
129309	3837	750
129310	3837	754
129311	3837	760
129312	3837	761
129313	3837	764
129314	3837	768
129315	3837	775
129316	3837	781
129317	3837	783
129318	3837	787
129319	3837	789
129320	3837	793
129321	3837	794
129322	3837	807
129323	3837	815
129324	3837	819
129325	3837	822
129326	3837	828
129327	3837	832
129328	3837	835
129329	3837	841
129330	3837	845
129331	3837	846
129332	3837	851
129333	3837	852
129334	3837	859
129335	3837	860
129336	3837	874
129337	3838	732
129338	3838	734
129339	3838	740
129340	3838	743
129341	3838	745
129342	3838	749
129343	3838	753
129344	3838	760
129345	3838	761
129346	3838	764
129347	3838	768
129348	3838	774
129349	3838	781
129350	3838	783
129351	3838	787
129352	3838	789
129353	3838	792
129354	3838	794
129355	3838	806
129356	3838	816
129357	3838	819
129358	3838	822
129359	3838	827
129360	3838	833
129361	3838	841
129362	3838	845
129363	3838	846
129364	3838	851
129365	3838	852
129366	3838	859
129367	3838	860
129368	3839	732
129369	3839	734
129370	3839	740
129371	3839	743
129372	3839	746
129373	3839	749
129374	3839	753
129375	3839	760
129376	3839	761
129377	3839	764
129378	3839	768
129379	3839	772
129380	3839	777
129381	3839	783
129382	3839	787
129383	3839	789
129384	3839	792
129385	3839	794
129386	3839	808
129387	3839	811
129388	3839	819
129389	3839	822
129390	3839	828
129391	3839	832
129392	3839	835
129393	3839	841
129394	3839	845
129395	3839	847
129396	3839	851
129397	3839	853
129398	3839	858
129399	3839	860
129400	3840	732
129401	3840	734
129402	3840	740
129403	3840	744
129404	3840	746
129405	3840	749
129406	3840	754
129407	3840	760
129408	3840	761
129409	3840	764
129410	3840	768
129411	3840	772
129412	3840	777
129413	3840	784
129414	3840	787
129415	3840	789
129416	3840	792
129417	3840	794
129418	3840	806
129419	3840	811
129420	3840	818
129421	3840	822
129422	3840	827
129423	3840	832
129424	3840	835
129425	3840	841
129426	3840	845
129427	3840	847
129428	3840	851
129429	3840	853
129430	3840	858
129431	3840	860
129432	3840	871
129433	3840	874
129434	3841	732
129435	3841	734
129436	3841	740
129437	3841	743
129438	3841	745
129439	3841	748
129440	3841	752
129441	3841	760
129442	3841	761
129443	3841	764
129444	3841	768
129445	3841	772
129446	3841	777
129447	3841	783
129448	3841	787
129449	3841	789
129450	3841	792
129451	3841	794
129452	3841	808
129453	3841	811
129454	3841	819
129455	3841	822
129456	3841	827
129457	3841	833
129458	3841	835
129459	3841	841
129460	3841	843
129461	3841	847
129462	3841	849
129463	3841	853
129464	3841	856
129465	3841	860
129466	3841	874
129467	3842	732
129468	3842	734
129469	3842	740
129470	3842	744
129471	3842	746
129472	3842	748
129473	3842	754
129474	3842	760
129475	3842	761
129476	3842	764
129477	3842	768
129478	3842	772
129479	3842	777
129480	3842	783
129481	3842	787
129482	3842	789
129483	3842	793
129484	3842	794
129485	3842	807
129486	3842	811
129487	3842	819
129488	3842	822
129489	3842	827
129490	3842	832
129491	3842	835
129492	3842	841
129493	3842	844
129494	3842	847
129495	3842	850
129496	3842	853
129497	3842	857
129498	3842	860
129499	3842	871
129500	3842	874
129501	3843	732
129502	3843	734
129503	3843	740
129504	3843	744
129505	3843	746
129506	3843	749
129507	3843	753
129508	3843	758
129509	3843	761
129510	3843	764
129511	3843	768
129512	3843	772
129513	3843	777
129514	3843	783
129515	3843	787
129516	3843	789
129517	3843	792
129518	3843	794
129519	3843	807
129520	3843	811
129521	3843	818
129522	3843	823
129523	3843	828
129524	3843	830
129525	3843	835
129526	3843	841
129527	3843	843
129528	3843	847
129529	3843	849
129530	3843	853
129531	3843	856
129532	3843	860
129533	3843	874
129534	3844	733
129535	3844	734
129536	3844	740
129537	3844	743
129538	3844	746
129539	3844	749
129540	3844	754
129541	3844	760
129542	3844	761
129543	3844	764
129544	3844	768
129545	3844	772
129546	3844	777
129547	3844	782
129548	3844	787
129549	3844	789
129550	3844	792
129551	3844	794
129552	3844	808
129553	3844	811
129554	3844	818
129555	3844	821
129556	3844	827
129557	3844	833
129558	3844	835
129559	3844	840
129560	3844	844
129561	3844	846
129562	3844	850
129563	3844	852
129564	3844	858
129565	3844	860
129566	3844	874
129567	3845	732
129568	3845	734
129569	3845	740
129570	3845	744
129571	3845	746
129572	3845	749
129573	3845	754
129574	3845	760
129575	3845	761
129576	3845	764
129577	3845	768
129578	3845	775
129579	3845	777
129580	3845	784
129581	3845	787
129582	3845	790
129583	3845	792
129584	3845	794
129585	3845	808
129586	3845	815
129587	3845	818
129588	3845	822
129589	3845	827
129590	3845	832
129591	3845	835
129592	3845	840
129593	3845	845
129594	3845	846
129595	3845	851
129596	3845	852
129597	3845	859
129598	3845	860
129599	3845	871
129600	3845	874
129601	3846	732
129602	3846	734
129603	3846	740
129604	3846	743
129605	3846	746
129606	3846	748
129607	3846	753
129608	3846	760
129609	3846	761
129610	3846	764
129611	3846	768
129612	3846	775
129613	3846	781
129614	3846	782
129615	3846	787
129616	3846	789
129617	3846	792
129618	3846	794
129619	3846	808
129620	3846	815
129621	3846	818
129622	3846	823
129623	3846	827
129624	3846	832
129625	3846	835
129626	3846	840
129627	3846	845
129628	3846	846
129629	3846	851
129630	3846	852
129631	3846	858
129632	3846	860
129633	3846	874
129634	3847	732
129635	3847	734
129636	3847	740
129637	3847	743
129638	3847	746
129639	3847	749
129640	3847	753
129641	3847	759
129642	3847	761
129643	3847	764
129644	3847	768
129645	3847	772
129646	3847	777
129647	3847	783
129648	3847	787
129649	3847	789
129650	3847	792
129651	3847	794
129652	3847	809
129653	3847	811
129654	3847	818
129655	3847	822
129656	3847	828
129657	3847	832
129658	3847	835
129659	3847	841
129660	3847	844
129661	3847	848
129662	3847	850
129663	3847	854
129664	3847	856
129665	3847	860
129666	3847	874
129667	3848	732
129668	3848	734
129669	3848	740
129670	3848	743
129671	3848	746
129672	3848	749
129673	3848	754
129674	3848	759
129675	3848	761
129676	3848	764
129677	3848	768
129678	3848	772
129679	3848	777
129680	3848	782
129681	3848	787
129682	3848	789
129683	3848	792
129684	3848	794
129685	3848	809
129686	3848	811
129687	3848	818
129688	3848	822
129689	3848	828
129690	3848	831
129691	3848	835
129692	3848	841
129693	3848	845
129694	3848	846
129695	3848	851
129696	3848	852
129697	3848	859
129698	3848	860
129699	3848	874
129700	3849	732
129701	3849	734
129702	3849	740
129703	3849	742
129704	3849	746
129705	3849	749
129706	3849	754
129707	3849	758
129708	3849	761
129709	3849	764
129710	3849	768
129711	3849	772
129712	3849	777
129713	3849	782
129714	3849	787
129715	3849	789
129716	3849	792
129717	3849	794
129718	3849	808
129719	3849	811
129720	3849	818
129721	3849	822
129722	3849	827
129723	3849	831
129724	3849	835
129725	3849	840
129726	3849	844
129727	3849	847
129728	3849	850
129729	3849	853
129730	3849	857
129731	3849	860
129732	3849	874
129733	3850	732
129734	3850	734
129735	3850	740
129736	3850	743
129737	3850	746
129738	3850	748
129739	3850	753
129740	3850	759
129741	3850	761
129742	3850	764
129743	3850	768
129744	3850	772
129745	3850	777
129746	3850	782
129747	3850	787
129748	3850	789
129749	3850	791
129750	3850	794
129751	3850	809
129752	3850	811
129753	3850	818
129754	3850	822
129755	3850	828
129756	3850	831
129757	3850	835
129758	3850	841
129759	3850	844
129760	3850	847
129761	3850	850
129762	3850	853
129763	3850	856
129764	3850	860
129765	3850	874
129766	3851	732
129767	3851	734
129768	3851	740
129769	3851	743
129770	3851	746
129771	3851	749
129772	3851	754
129773	3851	759
129774	3851	761
129775	3851	764
129776	3851	768
129777	3851	772
129778	3851	777
129779	3851	783
129780	3851	787
129781	3851	789
129782	3851	792
129783	3851	794
129784	3851	808
129785	3851	811
129786	3851	819
129787	3851	822
129788	3851	827
129789	3851	831
129790	3851	835
129791	3851	841
129792	3851	845
129793	3851	846
129794	3851	851
129795	3851	852
129796	3851	859
129797	3851	860
129798	3852	732
129799	3852	734
129800	3852	740
129801	3852	742
129802	3852	746
129803	3852	749
129804	3852	754
129805	3852	759
129806	3852	761
129807	3852	764
129808	3852	768
129809	3852	772
129810	3852	777
129811	3852	783
129812	3852	787
129813	3852	789
129814	3852	792
129815	3852	794
129816	3852	807
129817	3852	811
129818	3852	819
129819	3852	822
129820	3852	827
129821	3852	831
129822	3852	835
129823	3852	842
129824	3852	845
129825	3852	847
129826	3852	851
129827	3852	853
129828	3852	858
129829	3852	860
129830	3852	871
129831	3852	874
129832	3853	732
129833	3853	734
129834	3853	740
129835	3853	743
129836	3853	746
129837	3853	749
129838	3853	754
129839	3853	758
129840	3853	761
129841	3853	764
129842	3853	768
129843	3853	772
129844	3853	777
129845	3853	783
129846	3853	787
129847	3853	789
129848	3853	792
129849	3853	794
129850	3853	808
129851	3853	811
129852	3853	819
129853	3853	822
129854	3853	827
129855	3853	831
129856	3853	835
129857	3853	841
129858	3853	845
129859	3853	847
129860	3853	851
129861	3853	853
129862	3853	858
129863	3853	860
129864	3853	871
129865	3853	872
129866	3853	874
129867	3854	732
129868	3854	734
129869	3854	740
129870	3854	743
129871	3854	746
129872	3854	749
129873	3854	754
129874	3854	759
129875	3854	761
129876	3854	764
129877	3854	768
129878	3854	772
129879	3854	777
129880	3854	783
129881	3854	787
129882	3854	789
129883	3854	792
129884	3854	794
129885	3854	808
129886	3854	811
129887	3854	819
129888	3854	822
129889	3854	828
129890	3854	832
129891	3854	835
129892	3854	842
129893	3854	845
129894	3854	848
129895	3854	851
129896	3854	854
129897	3854	857
129898	3854	860
129899	3854	871
129900	3854	872
129901	3854	874
129902	3855	732
129903	3855	734
129904	3855	740
129905	3855	743
129906	3855	746
129907	3855	749
129908	3855	753
129909	3855	758
129910	3855	761
129911	3855	764
129912	3855	768
129913	3855	772
129914	3855	777
129915	3855	783
129916	3855	787
129917	3855	789
129918	3855	792
129919	3855	794
129920	3855	806
129921	3855	811
129922	3855	819
129923	3855	822
129924	3855	828
129925	3855	830
129926	3855	835
129927	3855	841
129928	3855	845
129929	3855	847
129930	3855	851
129931	3855	853
129932	3855	857
129933	3855	860
129934	3855	871
129935	3855	873
129936	3855	874
129937	3856	732
129938	3856	734
129939	3856	740
129940	3856	744
129941	3856	745
129942	3856	749
129943	3856	754
129944	3856	759
129945	3856	761
129946	3856	764
129947	3856	768
129948	3856	772
129949	3856	777
129950	3856	783
129951	3856	787
129952	3856	789
129953	3856	792
129954	3856	794
129955	3856	806
129956	3856	813
129957	3856	819
129958	3856	823
129959	3856	828
129960	3856	831
129961	3856	836
129962	3856	840
129963	3856	845
129964	3856	846
129965	3856	851
129966	3856	852
129967	3856	859
129968	3856	863
129969	3856	871
129970	3856	873
129971	3856	874
129972	3857	731
129973	3857	734
129974	3857	740
129975	3857	744
129976	3857	746
129977	3857	748
129978	3857	752
129979	3857	760
129980	3857	761
129981	3857	764
129982	3857	768
129983	3857	772
129984	3857	777
129985	3857	783
129986	3857	787
129987	3857	789
129988	3857	793
129989	3857	795
129990	3857	798
129991	3857	803
129992	3857	808
129993	3857	811
129994	3857	819
129995	3857	823
129996	3857	826
129997	3857	832
129998	3857	834
129999	3857	841
130000	3857	845
130001	3857	846
130002	3857	851
130003	3857	852
130004	3857	859
130005	3857	860
130006	3857	871
130007	3857	873
130008	3857	874
130009	3858	732
130010	3858	734
130011	3858	740
130012	3858	742
130013	3858	746
130014	3858	748
130015	3858	753
130016	3858	758
130017	3858	761
130018	3858	764
130019	3858	768
130020	3858	772
130021	3858	777
130022	3858	782
130023	3858	787
130024	3858	789
130025	3858	792
130026	3858	794
130027	3858	808
130028	3858	811
130029	3858	819
130030	3858	823
130031	3858	828
130032	3858	831
130033	3858	836
130034	3858	841
130035	3858	845
130036	3858	847
130037	3858	851
130038	3858	853
130039	3858	857
130040	3858	868
130041	3858	870
130042	3858	872
130043	3858	876
130044	3859	732
130045	3859	734
130046	3859	740
130047	3859	744
130048	3859	746
130049	3859	749
130050	3859	753
130051	3859	758
130052	3859	761
130053	3859	764
130054	3859	768
130055	3859	775
130056	3859	777
130057	3859	783
130058	3859	787
130059	3859	789
130060	3859	793
130061	3859	795
130062	3859	800
130063	3859	804
130064	3859	808
130065	3859	814
130066	3859	819
130067	3859	823
130068	3859	827
130069	3859	831
130070	3859	836
130071	3859	842
130072	3859	845
130073	3859	848
130074	3859	851
130075	3859	854
130076	3859	857
130077	3859	860
130078	3859	871
130079	3859	873
130080	3859	874
130081	3860	732
130082	3860	734
130083	3860	740
130084	3860	743
130085	3860	747
130086	3860	748
130087	3860	752
130088	3860	759
130089	3860	761
130090	3860	764
130091	3860	768
130092	3860	772
130093	3860	777
130094	3860	783
130095	3860	787
130096	3860	789
130097	3860	794
130098	3860	808
130099	3860	811
130100	3860	819
130101	3860	822
130102	3860	828
130103	3860	832
130104	3860	835
130105	3860	841
130106	3860	844
130107	3860	847
130108	3860	850
130109	3860	853
130110	3860	857
130111	3860	860
130112	3860	871
130113	3860	873
130114	3860	874
130115	3861	731
130116	3861	734
130117	3861	740
130118	3861	743
130119	3861	746
130120	3861	748
130121	3861	752
130122	3861	760
130123	3861	761
130124	3861	764
130125	3861	768
130126	3861	772
130127	3861	777
130128	3861	783
130129	3861	787
130130	3861	789
130131	3861	792
130132	3861	795
130133	3861	798
130134	3861	803
130135	3861	807
130136	3861	811
130137	3861	819
130138	3861	823
130139	3861	826
130140	3861	832
130141	3861	835
130142	3861	840
130143	3861	845
130144	3861	846
130145	3861	851
130146	3861	852
130147	3861	859
130148	3861	860
130149	3861	871
130150	3861	873
130151	3861	874
130152	3862	732
130153	3862	734
130154	3862	740
130155	3862	743
130156	3862	746
130157	3862	748
130158	3862	752
130159	3862	760
130160	3862	761
130161	3862	764
130162	3862	768
130163	3862	772
130164	3862	777
130165	3862	783
130166	3862	787
130167	3862	789
130168	3862	792
130169	3862	795
130170	3862	797
130171	3862	802
130172	3862	806
130173	3862	811
130174	3862	819
130175	3862	822
130176	3862	825
130177	3862	832
130178	3862	835
130179	3862	841
130180	3862	845
130181	3862	846
130182	3862	851
130183	3862	852
130184	3862	859
130185	3862	860
130186	3862	871
130187	3862	873
130188	3862	874
130189	3863	732
130190	3863	734
130191	3863	740
130192	3863	743
130193	3863	746
130194	3863	748
130195	3863	752
130196	3863	760
130197	3863	763
130198	3863	764
130199	3863	768
130200	3863	772
130201	3863	777
130202	3863	783
130203	3863	787
130204	3863	789
130205	3863	795
130206	3863	797
130207	3863	802
130208	3863	807
130209	3863	811
130210	3863	871
130211	3863	873
130212	3863	874
130213	3864	733
130214	3864	735
130215	3864	737
130216	3864	741
130217	3864	743
130218	3864	746
130219	3864	749
130220	3864	753
130221	3864	758
130222	3864	761
130223	3864	764
130224	3864	768
130225	3864	776
130226	3864	781
130227	3864	783
130228	3864	787
130229	3864	789
130230	3864	792
130231	3864	794
130232	3864	806
130233	3864	814
130234	3864	819
130235	3864	822
130236	3864	828
130237	3864	830
130238	3864	835
130239	3864	842
130240	3864	845
130241	3864	847
130242	3864	851
130243	3864	853
130244	3864	857
130245	3864	860
130246	3864	871
130247	3864	872
130248	3864	874
130249	3865	733
130250	3865	735
130251	3865	737
130252	3865	741
130253	3865	742
130254	3865	746
130255	3865	750
130256	3865	755
130257	3865	758
130258	3865	761
130259	3865	764
130260	3865	768
130261	3865	776
130262	3865	781
130263	3865	787
130264	3865	789
130265	3865	792
130266	3865	794
130267	3865	806
130268	3865	815
130269	3865	819
130270	3865	822
130271	3865	826
130272	3865	831
130273	3865	835
130274	3865	841
130275	3865	845
130276	3865	847
130277	3865	851
130278	3865	853
130279	3865	857
130280	3865	860
130281	3865	871
130282	3865	872
130283	3865	874
130284	3866	733
130285	3866	735
130286	3866	737
130287	3866	741
130288	3866	743
130289	3866	746
130290	3866	749
130291	3866	754
130292	3866	758
130293	3866	761
130294	3866	764
130295	3866	768
130296	3866	775
130297	3866	781
130298	3866	783
130299	3866	788
130300	3866	790
130301	3866	793
130302	3866	795
130303	3866	798
130304	3866	801
130305	3866	808
130306	3866	815
130307	3866	819
130308	3866	822
130309	3866	828
130310	3866	831
130311	3866	835
130312	3866	842
130313	3866	845
130314	3866	847
130315	3866	851
130316	3866	853
130317	3866	858
130318	3866	860
130319	3866	871
130320	3866	872
130321	3866	874
130322	3867	732
130323	3867	734
130324	3867	740
130325	3867	743
130326	3867	746
130327	3867	749
130328	3867	753
130329	3867	758
130330	3867	761
130331	3867	764
130332	3867	768
130333	3867	773
130334	3867	777
130335	3867	783
130336	3867	787
130337	3867	789
130338	3867	792
130339	3867	794
130340	3867	807
130341	3867	814
130342	3867	819
130343	3867	822
130344	3867	827
130345	3867	830
130346	3867	835
130347	3867	842
130348	3867	845
130349	3867	847
130350	3867	851
130351	3867	853
130352	3867	858
130353	3867	860
130354	3867	871
130355	3867	872
130356	3867	874
130357	3868	732
130358	3868	734
130359	3868	740
130360	3868	744
130361	3868	746
130362	3868	748
130363	3868	753
130364	3868	760
130365	3868	761
130366	3868	764
130367	3868	768
130368	3868	775
130369	3868	777
130370	3868	783
130371	3868	787
130372	3868	789
130373	3868	792
130374	3868	794
130375	3868	806
130376	3868	816
130377	3868	819
130378	3868	823
130379	3868	826
130380	3868	832
130381	3868	835
130382	3868	840
130383	3868	845
130384	3868	846
130385	3868	851
130386	3868	852
130387	3868	859
130388	3868	860
130389	3868	871
130390	3868	873
130391	3868	874
130392	3869	732
130393	3869	734
130394	3869	740
130395	3869	744
130396	3869	746
130397	3869	749
130398	3869	753
130399	3869	758
130400	3869	761
130401	3869	764
130402	3869	768
130403	3869	772
130404	3869	777
130405	3869	783
130406	3869	787
130407	3869	789
130408	3869	792
130409	3869	794
130410	3869	808
130411	3869	811
130412	3869	819
130413	3869	822
130414	3869	827
130415	3869	831
130416	3869	834
130417	3869	842
130418	3869	845
130419	3869	848
130420	3869	851
130421	3869	854
130422	3869	857
130423	3869	860
130424	3869	871
130425	3869	872
130426	3869	874
130427	3870	733
130428	3870	734
130429	3870	740
130430	3870	743
130431	3870	746
130432	3870	748
130433	3870	753
130434	3870	758
130435	3870	761
130436	3870	764
130437	3870	768
130438	3870	775
130439	3870	780
130440	3870	782
130441	3870	787
130442	3870	789
130443	3870	792
130444	3870	794
130445	3870	806
130446	3870	815
130447	3870	819
130448	3870	822
130449	3870	827
130450	3870	831
130451	3870	835
130452	3870	842
130453	3870	845
130454	3870	847
130455	3870	851
130456	3870	853
130457	3870	857
130458	3870	860
130459	3870	871
130460	3870	873
130461	3870	874
130462	3871	732
130463	3871	734
130464	3871	740
130465	3871	743
130466	3871	745
130467	3871	749
130468	3871	754
130469	3871	759
130470	3871	761
130471	3871	764
130472	3871	768
130473	3871	774
130474	3871	781
130475	3871	783
130476	3871	787
130477	3871	789
130478	3871	792
130479	3871	794
130480	3871	806
130481	3871	815
130482	3871	819
130483	3871	822
130484	3871	827
130485	3871	832
130486	3871	835
130487	3871	845
130488	3871	846
130489	3871	851
130490	3871	852
130491	3871	859
130492	3871	860
130493	3871	871
130494	3871	873
130495	3871	874
130496	3872	733
130497	3872	735
130498	3872	737
130499	3872	741
130500	3872	744
130501	3872	746
130502	3872	750
130503	3872	755
130504	3872	758
130505	3872	761
130506	3872	764
130507	3872	771
130508	3872	776
130509	3872	781
130510	3872	784
130511	3872	787
130512	3872	789
130513	3872	793
130514	3872	794
130515	3872	807
130516	3872	815
130517	3872	819
130518	3872	823
130519	3872	828
130520	3872	832
130521	3872	839
130522	3872	841
130523	3872	845
130524	3872	846
130525	3872	851
130526	3872	852
130527	3872	859
130528	3872	868
130529	3872	871
130530	3872	872
130531	3872	876
130532	3873	732
130533	3873	734
130534	3873	740
130535	3873	743
130536	3873	746
130537	3873	749
130538	3873	753
130539	3873	759
130540	3873	761
130541	3873	764
130542	3873	768
130543	3873	774
130544	3873	777
130545	3873	783
130546	3873	787
130547	3873	789
130548	3873	792
130549	3873	794
130550	3873	808
130551	3873	814
130552	3873	819
130553	3873	822
130554	3873	827
130555	3873	832
130556	3873	835
130557	3873	842
130558	3873	845
130559	3873	848
130560	3873	851
130561	3873	854
130562	3873	857
130563	3873	860
130564	3873	871
130565	3873	873
130566	3873	874
130567	3874	732
130568	3874	734
130569	3874	740
130570	3874	743
130571	3874	746
130572	3874	749
130573	3874	753
130574	3874	759
130575	3874	761
130576	3874	764
130577	3874	768
130578	3874	774
130579	3874	777
130580	3874	783
130581	3874	787
130582	3874	789
130583	3874	792
130584	3874	794
130585	3874	808
130586	3874	814
130587	3874	819
130588	3874	822
130589	3874	827
130590	3874	832
130591	3874	835
130592	3874	842
130593	3874	845
130594	3874	848
130595	3874	851
130596	3874	854
130597	3874	857
130598	3874	860
130599	3874	871
130600	3874	873
130601	3874	874
130602	3875	733
130603	3875	735
130604	3875	737
130605	3875	741
130606	3875	743
130607	3875	746
130608	3875	748
130609	3875	753
130610	3875	758
130611	3875	761
130612	3875	764
130613	3875	770
130614	3875	776
130615	3875	781
130616	3875	784
130617	3875	787
130618	3875	789
130619	3875	793
130620	3875	794
130621	3875	807
130622	3875	816
130623	3875	819
130624	3875	823
130625	3875	828
130626	3875	832
130627	3875	836
130628	3875	841
130629	3875	845
130630	3875	846
130631	3875	851
130632	3875	852
130633	3875	859
130634	3875	865
130635	3875	871
130636	3875	873
130637	3875	876
130638	3876	732
130639	3876	734
130640	3876	740
130641	3876	743
130642	3876	746
130643	3876	749
130644	3876	753
130645	3876	758
130646	3876	761
130647	3876	764
130648	3876	768
130649	3876	772
130650	3876	777
130651	3876	783
130652	3876	787
130653	3876	789
130654	3876	792
130655	3876	794
130656	3876	806
130657	3876	811
130658	3876	819
130659	3876	822
130660	3876	827
130661	3876	831
130662	3876	835
130663	3876	841
130664	3876	845
130665	3876	847
130666	3876	851
130667	3876	853
130668	3876	858
130669	3876	860
130670	3876	871
130671	3876	872
130672	3876	874
130673	3877	732
130674	3877	734
130675	3877	740
130676	3877	743
130677	3877	746
130678	3877	749
130679	3877	754
130680	3877	759
130681	3877	761
130682	3877	764
130683	3877	768
130684	3877	774
130685	3877	781
130686	3877	783
130687	3877	787
130688	3877	789
130689	3877	792
130690	3877	794
130691	3877	806
130692	3877	815
130693	3877	819
130694	3877	822
130695	3877	827
130696	3877	831
130697	3877	835
130698	3877	841
130699	3877	845
130700	3877	847
130701	3877	851
130702	3877	853
130703	3877	858
130704	3877	860
130705	3877	871
130706	3877	872
130707	3877	874
130708	3878	732
130709	3878	735
130710	3878	737
130711	3878	741
130712	3878	743
130713	3878	746
130714	3878	748
130715	3878	752
130716	3878	760
130717	3878	761
130718	3878	764
130719	3878	768
130720	3878	775
130721	3878	781
130722	3878	783
130723	3878	787
130724	3878	789
130725	3878	793
130726	3878	794
130727	3878	806
130728	3878	815
130729	3878	819
130730	3878	823
130731	3878	825
130732	3878	832
130733	3878	835
130734	3878	845
130735	3878	846
130736	3878	851
130737	3878	852
130738	3878	859
130739	3878	860
130740	3878	871
130741	3878	873
130742	3878	874
130743	3879	731
130744	3879	734
130745	3879	740
130746	3879	744
130747	3879	747
130748	3879	748
130749	3879	752
130750	3879	760
130751	3879	761
130752	3879	764
130753	3879	768
130754	3879	774
130755	3879	781
130756	3879	784
130757	3879	787
130758	3879	789
130759	3879	793
130760	3879	794
130761	3879	806
130762	3879	814
130763	3879	819
130764	3879	822
130765	3879	827
130766	3879	832
130767	3879	835
130768	3879	845
130769	3879	846
130770	3879	851
130771	3879	852
130772	3879	859
130773	3879	860
130774	3879	874
130775	3880	732
130776	3880	734
130777	3880	740
130778	3880	743
130779	3880	745
130780	3880	748
130781	3880	753
130782	3880	758
130783	3880	761
130784	3880	764
130785	3880	768
130786	3880	772
130787	3880	777
130788	3880	783
130789	3880	787
130790	3880	789
130791	3880	792
130792	3880	794
130793	3880	807
130794	3880	811
130795	3880	819
130796	3880	822
130797	3880	827
130798	3880	831
130799	3880	835
130800	3880	841
130801	3880	844
130802	3880	847
130803	3880	850
130804	3880	853
130805	3880	856
130806	3880	860
130807	3880	871
130808	3880	872
130809	3880	874
130810	3881	732
130811	3881	734
130812	3881	740
130813	3881	743
130814	3881	746
130815	3881	749
130816	3881	753
130817	3881	758
130818	3881	761
130819	3881	764
130820	3881	768
130821	3881	772
130822	3881	777
130823	3881	784
130824	3881	787
130825	3881	789
130826	3881	792
130827	3881	794
130828	3881	808
130829	3881	811
130830	3881	819
130831	3881	822
130832	3881	828
130833	3881	832
130834	3881	835
130835	3881	843
130836	3881	847
130837	3881	849
130838	3881	853
130839	3881	856
130840	3881	860
130841	3881	874
130842	3882	733
130843	3882	735
130844	3882	738
130845	3882	741
130846	3882	743
130847	3882	746
130848	3882	749
130849	3882	754
130850	3882	758
130851	3882	761
130852	3882	767
130853	3882	771
130854	3882	776
130855	3882	781
130856	3882	784
130857	3882	787
130858	3882	790
130859	3882	792
130860	3882	794
130861	3882	808
130862	3882	816
130863	3882	819
130864	3882	822
130865	3882	828
130866	3882	831
130867	3882	839
130868	3882	841
130869	3882	845
130870	3882	847
130871	3882	851
130872	3882	853
130873	3882	857
130874	3882	868
130875	3882	871
130876	3882	873
130877	3882	876
130878	3883	733
130879	3883	735
130880	3883	737
130881	3883	741
130882	3883	743
130883	3883	746
130884	3883	749
130885	3883	754
130886	3883	759
130887	3883	761
130888	3883	764
130889	3883	768
130890	3883	775
130891	3883	781
130892	3883	784
130893	3883	787
130894	3883	789
130895	3883	792
130896	3883	794
130897	3883	809
130898	3883	816
130899	3883	819
130900	3883	822
130901	3883	828
130902	3883	831
130903	3883	836
130904	3883	842
130905	3883	845
130906	3883	848
130907	3883	851
130908	3883	854
130909	3883	856
130910	3883	866
130911	3883	869
130912	3883	872
130913	3883	874
130914	3884	732
130915	3884	734
130916	3884	740
130917	3884	744
130918	3884	746
130919	3884	748
130920	3884	754
130921	3884	760
130922	3884	761
130923	3884	765
130924	3884	769
130925	3884	775
130926	3884	777
130927	3884	784
130928	3884	787
130929	3884	789
130930	3884	792
130931	3884	794
130932	3884	809
130933	3884	814
130934	3884	819
130935	3884	822
130936	3884	828
130937	3884	831
130938	3884	842
130939	3884	845
130940	3884	848
130941	3884	851
130942	3884	854
130943	3884	857
130944	3884	860
130945	3884	871
130946	3884	873
130947	3884	874
130948	3885	732
130949	3885	734
130950	3885	740
130951	3885	744
130952	3885	745
130953	3885	749
130954	3885	754
130955	3885	758
130956	3885	761
130957	3885	764
130958	3885	768
130959	3885	772
130960	3885	777
130961	3885	787
130962	3885	789
130963	3885	794
130964	3885	807
130965	3885	811
130966	3885	819
130967	3885	823
130968	3885	828
130969	3885	830
130970	3885	835
130971	3885	841
130972	3885	844
130973	3885	847
130974	3885	850
130975	3885	853
130976	3885	856
130977	3885	860
130978	3885	871
130979	3885	874
130980	3886	733
130981	3886	734
130982	3886	740
130983	3886	742
130984	3886	747
130985	3886	748
130986	3886	752
130987	3886	760
130988	3886	761
130989	3886	764
130990	3886	768
130991	3886	772
130992	3886	777
130993	3886	782
130994	3886	787
130995	3886	789
130996	3886	792
130997	3886	794
130998	3886	808
130999	3886	811
131000	3886	817
131001	3886	821
131002	3886	825
131003	3886	833
131004	3886	835
131005	3886	840
131006	3886	843
131007	3886	847
131008	3886	849
131009	3886	853
131010	3886	855
131011	3886	860
131012	3886	871
131013	3886	874
131014	3888	732
131015	3888	734
131016	3888	740
131017	3888	743
131018	3888	747
131019	3888	749
131020	3888	754
131021	3888	759
131022	3888	761
131023	3888	764
131024	3888	768
131025	3888	772
131026	3888	777
131027	3888	784
131028	3888	787
131029	3888	789
131030	3888	792
131031	3888	794
131032	3888	806
131033	3888	811
131034	3888	819
131035	3888	822
131036	3888	827
131037	3888	833
131038	3888	835
131039	3888	841
131040	3888	844
131041	3888	847
131042	3888	850
131043	3888	853
131044	3888	857
131045	3888	860
131046	3888	871
131047	3889	732
131048	3889	734
131049	3889	740
131050	3889	742
131051	3889	746
131052	3889	749
131053	3889	754
131054	3889	759
131055	3889	761
131056	3889	764
131057	3889	768
131058	3889	772
131059	3889	777
131060	3889	785
131061	3889	787
131062	3889	789
131063	3889	792
131064	3889	794
131065	3889	808
131066	3889	811
131067	3889	819
131068	3889	822
131069	3889	826
131070	3889	833
131071	3889	835
131072	3889	841
131073	3889	844
131074	3889	847
131075	3889	850
131076	3889	853
131077	3889	857
131078	3889	860
131079	3889	871
131080	3890	732
131081	3890	734
131082	3890	740
131083	3890	742
131084	3890	746
131085	3890	749
131086	3890	754
131087	3890	759
131088	3890	761
131089	3890	764
131090	3890	768
131091	3890	772
131092	3890	777
131093	3890	785
131094	3890	787
131095	3890	789
131096	3890	792
131097	3890	794
131098	3890	808
131099	3890	811
131100	3890	818
131101	3890	821
131102	3890	826
131103	3890	833
131104	3890	835
131105	3890	841
131106	3890	844
131107	3890	847
131108	3890	850
131109	3890	853
131110	3890	857
131111	3890	860
131112	3890	871
131113	3892	731
131114	3892	734
131115	3892	740
131116	3892	744
131117	3892	746
131118	3892	749
131119	3892	753
131120	3892	760
131121	3892	761
131122	3892	764
131123	3892	768
131124	3892	774
131125	3892	777
131126	3892	783
131127	3892	787
131128	3892	789
131129	3892	792
131130	3892	794
131131	3892	806
131132	3892	816
131133	3892	819
131134	3892	823
131135	3892	826
131136	3892	832
131137	3892	835
131138	3892	840
131139	3892	845
131140	3892	846
131141	3892	851
131142	3892	852
131143	3892	859
131144	3892	860
131145	3892	871
131146	3892	873
131147	3892	874
131148	3893	731
131149	3893	735
131150	3893	737
131151	3893	741
131152	3893	744
131153	3893	746
131154	3893	748
131155	3893	753
131156	3893	760
131157	3893	761
131158	3893	766
131159	3893	770
131160	3893	775
131161	3893	781
131162	3893	786
131163	3893	788
131164	3893	789
131165	3893	792
131166	3893	795
131167	3893	799
131168	3893	803
131169	3893	808
131170	3893	813
131171	3893	819
131172	3893	822
131173	3893	828
131174	3893	832
131175	3893	845
131176	3893	847
131177	3893	851
131178	3893	853
131179	3893	858
131180	3893	865
131181	3894	732
131182	3894	734
131183	3894	740
131184	3894	743
131185	3894	746
131186	3894	748
131187	3894	752
131188	3894	759
131189	3894	761
131190	3894	764
131191	3894	768
131192	3894	772
131193	3894	777
131194	3894	783
131195	3894	787
131196	3894	789
131197	3894	792
131198	3894	794
131199	3894	807
131200	3894	811
131201	3894	819
131202	3894	822
131203	3894	828
131204	3894	831
131205	3894	835
131206	3894	841
131207	3894	845
131208	3894	846
131209	3894	851
131210	3894	852
131211	3894	859
131212	3894	860
131213	3894	871
131214	3894	874
131215	3895	732
131216	3895	734
131217	3895	740
131218	3895	744
131219	3895	745
131220	3895	749
131221	3895	754
131222	3895	759
131223	3895	761
131224	3895	764
131225	3895	768
131226	3895	772
131227	3895	777
131228	3895	785
131229	3895	787
131230	3895	789
131231	3895	793
131232	3895	794
131233	3895	807
131234	3895	811
131235	3895	819
131236	3895	823
131237	3895	828
131238	3895	832
131239	3895	835
131240	3895	842
131241	3895	844
131242	3895	847
131243	3895	850
131244	3895	853
131245	3895	857
131246	3895	860
131247	3895	871
131248	3895	874
131249	3896	732
131250	3896	735
131251	3896	737
131252	3896	741
131253	3896	744
131254	3896	745
131255	3896	749
131256	3896	753
131257	3896	760
131258	3896	761
131259	3896	764
131260	3896	768
131261	3896	772
131262	3896	777
131263	3896	786
131264	3896	788
131265	3896	789
131266	3896	793
131267	3896	795
131268	3896	800
131269	3896	805
131270	3896	809
131271	3896	811
131272	3896	819
131273	3896	822
131274	3896	828
131275	3896	831
131276	3896	835
131277	3896	842
131278	3896	845
131279	3896	851
131280	3896	854
131281	3896	857
131282	3896	860
131283	3896	871
131284	3896	874
131285	3897	732
131286	3897	735
131287	3897	737
131288	3897	740
131289	3897	744
131290	3897	745
131291	3897	748
131292	3897	753
131293	3897	758
131294	3897	761
131295	3897	764
131296	3897	768
131297	3897	774
131298	3897	780
131299	3897	783
131300	3897	787
131301	3897	789
131302	3897	792
131303	3897	794
131304	3897	807
131305	3897	815
131306	3897	819
131307	3897	823
131308	3897	827
131309	3897	830
131310	3897	835
131311	3897	841
131312	3897	845
131313	3897	846
131314	3897	851
131315	3897	852
131316	3897	859
131317	3897	860
131318	3897	871
131319	3897	872
131320	3897	874
131321	3898	732
131322	3898	735
131323	3898	737
131324	3898	740
131325	3898	744
131326	3898	745
131327	3898	749
131328	3898	753
131329	3898	759
131330	3898	761
131331	3898	764
131332	3898	768
131333	3898	775
131334	3898	781
131335	3898	784
131336	3898	787
131337	3898	789
131338	3898	793
131339	3898	794
131340	3898	807
131341	3898	815
131342	3898	819
131343	3898	823
131344	3898	827
131345	3898	832
131346	3898	835
131347	3898	841
131348	3898	845
131349	3898	846
131350	3898	851
131351	3898	852
131352	3898	859
131353	3898	860
131354	3898	871
131355	3898	872
131356	3898	874
131357	3899	732
131358	3899	734
131359	3899	740
131360	3899	743
131361	3899	745
131362	3899	748
131363	3899	753
131364	3899	759
131365	3899	761
131366	3899	764
131367	3899	768
131368	3899	772
131369	3899	777
131370	3899	783
131371	3899	787
131372	3899	789
131373	3899	792
131374	3899	794
131375	3899	807
131376	3899	811
131377	3899	819
131378	3899	822
131379	3899	828
131380	3899	830
131381	3899	835
131382	3899	840
131383	3899	844
131384	3899	847
131385	3899	850
131386	3899	853
131387	3899	857
131388	3899	860
131389	3899	871
131390	3899	872
131391	3899	874
131392	3900	732
131393	3900	734
131394	3900	740
131395	3900	743
131396	3900	746
131397	3900	748
131398	3900	753
131399	3900	758
131400	3900	761
131401	3900	764
131402	3900	768
131403	3900	775
131404	3900	781
131405	3900	783
131406	3900	787
131407	3900	789
131408	3900	792
131409	3900	794
131410	3900	807
131411	3900	815
131412	3900	819
131413	3900	822
131414	3900	828
131415	3900	831
131416	3900	835
131417	3900	841
131418	3900	845
131419	3900	847
131420	3900	851
131421	3900	853
131422	3900	857
131423	3900	860
131424	3900	871
131425	3900	872
131426	3900	874
131427	3901	732
131428	3901	734
131429	3901	740
131430	3901	744
131431	3901	746
131432	3901	749
131433	3901	753
131434	3901	759
131435	3901	761
131436	3901	764
131437	3901	768
131438	3901	772
131439	3901	777
131440	3901	784
131441	3901	787
131442	3901	789
131443	3901	792
131444	3901	794
131445	3901	806
131446	3901	811
131447	3901	819
131448	3901	822
131449	3901	828
131450	3901	832
131451	3901	835
131452	3901	842
131453	3901	845
131454	3901	848
131455	3901	851
131456	3901	854
131457	3901	857
131458	3901	860
131459	3901	871
131460	3901	872
131461	3901	874
131462	3902	732
131463	3902	734
131464	3902	740
131465	3902	744
131466	3902	745
131467	3902	749
131468	3902	754
131469	3902	758
131470	3902	761
131471	3902	764
131472	3902	768
131473	3902	772
131474	3902	777
131475	3902	785
131476	3902	787
131477	3902	789
131478	3902	792
131479	3902	795
131480	3902	800
131481	3902	802
131482	3902	808
131483	3902	811
131484	3902	819
131485	3902	823
131486	3902	828
131487	3902	831
131488	3902	835
131489	3902	842
131490	3902	845
131491	3902	848
131492	3902	851
131493	3902	854
131494	3902	857
131495	3902	860
131496	3902	871
131497	3902	872
131498	3902	874
131499	3903	732
131500	3903	734
131501	3903	740
131502	3903	743
131503	3903	746
131504	3903	749
131505	3903	753
131506	3903	757
131507	3903	761
131508	3903	764
131509	3903	769
131510	3903	776
131511	3903	781
131512	3903	783
131513	3903	787
131514	3903	789
131515	3903	792
131516	3903	794
131517	3903	807
131518	3903	815
131519	3903	819
131520	3903	822
131521	3903	827
131522	3903	831
131523	3903	835
131524	3903	841
131525	3903	844
131526	3903	848
131527	3903	850
131528	3903	854
131529	3903	856
131530	3903	860
131531	3903	871
131532	3903	872
131533	3903	874
131534	3904	732
131535	3904	734
131536	3904	740
131537	3904	743
131538	3904	746
131539	3904	749
131540	3904	753
131541	3904	758
131542	3904	761
131543	3904	764
131544	3904	768
131545	3904	772
131546	3904	777
131547	3904	783
131548	3904	787
131549	3904	789
131550	3904	792
131551	3904	794
131552	3904	808
131553	3904	811
131554	3904	818
131555	3904	822
131556	3904	828
131557	3904	831
131558	3904	835
131559	3904	841
131560	3904	843
131561	3904	847
131562	3904	849
131563	3904	853
131564	3904	856
131565	3904	860
131566	3904	871
131567	3904	872
131568	3904	874
131569	3905	732
131570	3905	734
131571	3905	740
131572	3905	743
131573	3905	746
131574	3905	749
131575	3905	754
131576	3905	757
131577	3905	761
131578	3905	764
131579	3905	768
131580	3905	772
131581	3905	777
131582	3905	782
131583	3905	787
131584	3905	789
131585	3905	792
131586	3905	794
131587	3905	806
131588	3905	811
131589	3905	819
131590	3905	823
131591	3905	827
131592	3905	830
131593	3905	836
131594	3905	840
131595	3905	844
131596	3905	846
131597	3905	850
131598	3905	852
131599	3905	858
131600	3905	868
131601	3905	871
131602	3905	872
131603	3905	874
131604	3906	732
131605	3906	734
131606	3906	740
131607	3906	744
131608	3906	746
131609	3906	749
131610	3906	755
131611	3906	760
131612	3906	761
131613	3906	764
131614	3906	768
131615	3906	772
131616	3906	777
131617	3906	785
131618	3906	787
131619	3906	789
131620	3906	793
131621	3906	794
131622	3906	808
131623	3906	811
131624	3906	819
131625	3906	823
131626	3906	828
131627	3906	832
131628	3906	835
131629	3906	841
131630	3906	845
131631	3906	846
131632	3906	851
131633	3906	852
131634	3906	859
131635	3906	865
131636	3907	732
131637	3907	734
131638	3907	740
131639	3907	743
131640	3907	746
131641	3907	749
131642	3907	753
131643	3907	760
131644	3907	761
131645	3907	764
131646	3907	768
131647	3907	772
131648	3907	777
131649	3907	783
131650	3907	787
131651	3907	789
131652	3907	793
131653	3907	794
131654	3907	808
131655	3907	811
131656	3907	819
131657	3907	822
131658	3907	828
131659	3907	832
131660	3907	835
131661	3907	841
131662	3907	845
131663	3907	847
131664	3907	851
131665	3907	853
131666	3907	857
131667	3907	860
131668	3907	871
131669	3907	872
131670	3907	874
131671	3908	732
131672	3908	734
131673	3908	740
131674	3908	744
131675	3908	746
131676	3908	749
131677	3908	753
131678	3908	759
131679	3908	761
131680	3908	764
131681	3908	768
131682	3908	772
131683	3908	777
131684	3908	783
131685	3908	787
131686	3908	789
131687	3908	792
131688	3908	794
131689	3908	808
131690	3908	811
131691	3908	819
131692	3908	822
131693	3908	828
131694	3908	831
131695	3908	835
131696	3908	841
131697	3908	845
131698	3908	847
131699	3908	851
131700	3908	853
131701	3908	857
131702	3908	860
131703	3908	871
131704	3908	872
131705	3908	874
131706	3909	731
131707	3909	734
131708	3909	740
131709	3909	744
131710	3909	746
131711	3909	749
131712	3909	754
131713	3909	760
131714	3909	761
131715	3909	764
131716	3909	768
131717	3909	772
131718	3909	777
131719	3909	784
131720	3909	787
131721	3909	789
131722	3909	793
131723	3909	794
131724	3909	807
131725	3909	811
131726	3909	819
131727	3909	822
131728	3909	828
131729	3909	832
131730	3909	835
131731	3909	841
131732	3909	845
131733	3909	846
131734	3909	851
131735	3909	852
131736	3909	859
131737	3909	865
131738	3909	871
131739	3909	872
131740	3909	876
131741	3910	733
131742	3910	735
131743	3910	739
131744	3910	741
131745	3910	744
131746	3910	746
131747	3910	749
131748	3910	754
131749	3910	760
131750	3910	761
131751	3910	767
131752	3910	771
131753	3910	776
131754	3910	781
131755	3910	784
131756	3910	787
131757	3910	790
131758	3910	793
131759	3910	794
131760	3910	807
131761	3910	816
131762	3910	819
131763	3910	823
131764	3910	828
131765	3910	832
131766	3910	839
131767	3910	840
131768	3910	844
131769	3910	847
131770	3910	850
131771	3910	853
131772	3910	857
131773	3910	868
131774	3910	871
131775	3910	872
131776	3910	876
131777	3911	732
131778	3911	734
131779	3911	740
131780	3911	744
131781	3911	745
131782	3911	749
131783	3911	754
131784	3911	760
131785	3911	761
131786	3911	764
131787	3911	768
131788	3911	772
131789	3911	777
131790	3911	783
131791	3911	787
131792	3911	789
131793	3911	792
131794	3911	795
131795	3911	797
131796	3911	803
131797	3911	808
131798	3911	811
131799	3911	819
131800	3911	822
131801	3911	828
131802	3911	831
131803	3911	836
131804	3911	841
131805	3911	845
131806	3911	847
131807	3911	851
131808	3911	853
131809	3911	857
131810	3911	868
131811	3911	871
131812	3911	872
131813	3911	876
131814	3912	732
131815	3912	734
131816	3912	740
131817	3912	744
131818	3912	747
131819	3912	749
131820	3912	753
131821	3912	759
131822	3912	761
131823	3912	764
131824	3912	768
131825	3912	773
131826	3912	777
131827	3912	783
131828	3912	787
131829	3912	789
131830	3912	792
131831	3912	794
131832	3912	806
131833	3912	814
131834	3912	819
131835	3912	823
131836	3912	827
131837	3912	831
131838	3912	836
131839	3912	841
131840	3912	845
131841	3912	846
131842	3912	851
131843	3912	852
131844	3912	859
131845	3912	868
131846	3913	732
131847	3913	734
131848	3913	740
131849	3913	744
131850	3913	746
131851	3913	749
131852	3913	753
131853	3913	759
131854	3913	761
131855	3913	764
131856	3913	768
131857	3913	772
131858	3913	777
131859	3913	783
131860	3913	787
131861	3913	789
131862	3913	792
131863	3913	794
131864	3913	806
131865	3913	811
131866	3913	819
131867	3913	822
131868	3913	828
131869	3913	832
131870	3913	835
131871	3913	842
131872	3913	845
131873	3913	847
131874	3913	851
131875	3913	854
131876	3913	857
131877	3913	860
131878	3913	871
131879	3913	874
131880	3914	732
131881	3914	734
131882	3914	740
131883	3914	744
131884	3914	746
131885	3914	749
131886	3914	753
131887	3914	759
131888	3914	761
131889	3914	764
131890	3914	768
131891	3914	772
131892	3914	777
131893	3914	783
131894	3914	787
131895	3914	789
131896	3914	792
131897	3914	794
131898	3914	806
131899	3914	811
131900	3914	818
131901	3914	822
131902	3914	828
131903	3914	831
131904	3914	835
131905	3914	841
131906	3914	845
131907	3914	847
131908	3914	851
131909	3914	853
131910	3914	857
131911	3914	860
131912	3914	871
131913	3914	874
131914	3915	732
131915	3915	734
131916	3915	740
131917	3915	744
131918	3915	746
131919	3915	749
131920	3915	753
131921	3915	760
131922	3915	761
131923	3915	764
131924	3915	768
131925	3915	776
131926	3915	781
131927	3915	786
131928	3915	787
131929	3915	789
131930	3915	793
131931	3915	794
131932	3915	808
131933	3915	816
131934	3915	819
131935	3915	822
131936	3915	828
131937	3915	832
131938	3915	835
131939	3915	841
131940	3915	843
131941	3915	848
131942	3915	849
131943	3915	854
131944	3915	856
131945	3915	860
131946	3915	871
131947	3915	874
131948	3916	732
131949	3916	734
131950	3916	740
131951	3916	743
131952	3916	745
131953	3916	749
131954	3916	754
131955	3916	760
131956	3916	761
131957	3916	764
131958	3916	768
131959	3916	774
131960	3916	781
131961	3916	783
131962	3916	787
131963	3916	789
131964	3916	792
131965	3916	794
131966	3916	806
131967	3916	815
131968	3916	819
131969	3916	823
131970	3916	826
131971	3916	832
131972	3916	835
131973	3916	841
131974	3916	845
131975	3916	846
131976	3916	851
131977	3916	852
131978	3916	859
131979	3916	860
131980	3916	871
131981	3916	874
131982	3918	732
131983	3918	734
131984	3918	740
131985	3918	744
131986	3918	746
131987	3918	749
131988	3918	753
131989	3918	759
131990	3918	761
131991	3918	764
131992	3918	768
131993	3918	772
131994	3918	777
131995	3918	784
131996	3918	787
131997	3918	789
131998	3918	792
131999	3918	794
132000	3918	807
132001	3918	811
132002	3918	817
132003	3918	822
132004	3918	828
132005	3918	832
132006	3918	835
132007	3918	840
132008	3918	845
132009	3918	846
132010	3918	851
132011	3918	852
132012	3918	859
132013	3918	860
132014	3919	732
132015	3919	734
132016	3919	740
132017	3919	743
132018	3919	745
132019	3919	748
132020	3919	752
132021	3919	760
132022	3919	761
132023	3919	764
132024	3919	768
132025	3919	772
132026	3919	777
132027	3919	783
132028	3919	787
132029	3919	789
132030	3919	793
132031	3919	794
132032	3919	807
132033	3919	811
132034	3919	819
132035	3919	822
132036	3919	826
132037	3919	833
132038	3919	835
132039	3919	841
132040	3919	845
132041	3919	847
132042	3919	851
132043	3919	853
132044	3919	858
132045	3919	860
132046	3919	870
132047	3919	872
132048	3919	874
132049	3920	732
132050	3920	734
132051	3920	740
132052	3920	744
132053	3920	745
132054	3920	748
132055	3920	752
132056	3920	760
132057	3920	763
132058	3920	764
132059	3920	768
132060	3920	772
132061	3920	777
132062	3920	782
132063	3920	787
132064	3920	789
132065	3920	793
132066	3920	795
132067	3920	797
132068	3920	802
132069	3920	807
132070	3920	811
132071	3920	818
132072	3920	823
132073	3920	825
132074	3920	835
132075	3920	860
132076	3920	871
132077	3920	873
132078	3920	874
132079	3921	732
132080	3921	735
132081	3921	737
132082	3921	740
132083	3921	743
132084	3921	745
132085	3921	748
132086	3921	752
132087	3921	760
132088	3921	763
132089	3921	764
132090	3921	768
132091	3921	775
132092	3921	781
132093	3921	783
132094	3921	787
132095	3921	789
132096	3921	793
132097	3921	794
132098	3921	808
132099	3921	816
132100	3921	818
132101	3921	823
132102	3921	824
132103	3921	835
132104	3921	860
132105	3921	870
132106	3921	872
132107	3921	874
132108	3922	732
132109	3922	735
132110	3922	737
132111	3922	741
132112	3922	744
132113	3922	746
132114	3922	749
132115	3922	753
132116	3922	760
132117	3922	761
132118	3922	764
132119	3922	768
132120	3922	775
132121	3922	777
132122	3922	783
132123	3922	787
132124	3922	789
132125	3922	792
132126	3922	794
132127	3922	806
132128	3922	815
132129	3922	818
132130	3922	821
132131	3922	826
132132	3922	832
132133	3922	835
132134	3922	840
132135	3922	845
132136	3922	846
132137	3922	851
132138	3922	852
132139	3922	859
132140	3922	860
132141	3922	871
132142	3922	872
132143	3922	874
132144	3923	732
132145	3923	734
132146	3923	740
132147	3923	744
132148	3923	746
132149	3923	749
132150	3923	753
132151	3923	760
132152	3923	761
132153	3923	764
132154	3923	768
132155	3923	775
132156	3923	777
132157	3923	783
132158	3923	787
132159	3923	789
132160	3923	793
132161	3923	794
132162	3923	806
132163	3923	815
132164	3923	819
132165	3923	823
132166	3923	826
132167	3923	832
132168	3923	835
132169	3923	840
132170	3923	845
132171	3923	846
132172	3923	851
132173	3923	852
132174	3923	859
132175	3923	860
132176	3923	871
132177	3923	872
132178	3923	874
132179	3924	732
132180	3924	734
132181	3924	740
132182	3924	743
132183	3924	745
132184	3924	748
132185	3924	752
132186	3924	760
132187	3924	761
132188	3924	764
132189	3924	768
132190	3924	772
132191	3924	777
132192	3924	783
132193	3924	787
132194	3924	789
132195	3924	793
132196	3924	795
132197	3924	797
132198	3924	802
132199	3924	807
132200	3924	811
132201	3924	819
132202	3924	823
132203	3924	826
132204	3924	832
132205	3924	835
132206	3924	840
132207	3924	844
132208	3924	846
132209	3924	850
132210	3924	852
132211	3924	858
132212	3924	860
132213	3924	871
132214	3924	873
132215	3924	874
132216	3925	732
132217	3925	734
132218	3925	740
132219	3925	744
132220	3925	746
132221	3925	748
132222	3925	753
132223	3925	759
132224	3925	761
132225	3925	766
132226	3925	771
132227	3925	776
132228	3925	781
132229	3925	784
132230	3925	787
132231	3925	790
132232	3925	793
132233	3925	794
132234	3925	808
132235	3925	816
132236	3925	819
132237	3925	822
132238	3925	828
132239	3925	831
132240	3925	839
132241	3925	842
132242	3925	845
132243	3925	848
132244	3925	851
132245	3925	854
132246	3925	857
132247	3925	860
132248	3925	871
132249	3925	872
132250	3925	876
132251	3926	733
132252	3926	735
132253	3926	737
132254	3926	741
132255	3926	743
132256	3926	746
132257	3926	749
132258	3926	754
132259	3926	758
132260	3926	761
132261	3926	764
132262	3926	768
132263	3926	776
132264	3926	781
132265	3926	783
132266	3926	788
132267	3926	789
132268	3926	792
132269	3926	794
132270	3926	807
132271	3926	815
132272	3926	819
132273	3926	822
132274	3926	828
132275	3926	831
132276	3926	835
132277	3926	842
132278	3926	845
132279	3926	848
132280	3926	851
132281	3926	854
132282	3926	857
132283	3926	860
132284	3926	871
132285	3926	872
132286	3926	874
132287	3927	732
132288	3927	734
132289	3927	740
132290	3927	744
132291	3927	746
132292	3927	748
132293	3927	753
132294	3927	758
132295	3927	761
132296	3927	764
132297	3927	768
132298	3927	772
132299	3927	777
132300	3927	783
132301	3927	787
132302	3927	789
132303	3927	793
132304	3927	795
132305	3927	797
132306	3927	801
132307	3927	806
132308	3927	811
132309	3927	819
132310	3927	822
132311	3927	828
132312	3927	831
132313	3927	835
132314	3927	842
132315	3927	845
132316	3927	847
132317	3927	851
132318	3927	853
132319	3927	858
132320	3927	860
132321	3927	871
132322	3927	872
132323	3927	874
132324	3928	732
132325	3928	734
132326	3928	740
132327	3928	744
132328	3928	746
132329	3928	748
132330	3928	752
132331	3928	760
132332	3928	761
132333	3928	764
132334	3928	768
132335	3928	772
132336	3928	777
132337	3928	784
132338	3928	787
132339	3928	789
132340	3928	793
132341	3928	795
132342	3928	797
132343	3928	802
132344	3928	807
132345	3928	811
132346	3928	819
132347	3928	823
132348	3928	825
132349	3928	833
132350	3928	835
132351	3928	841
132352	3928	844
132353	3928	847
132354	3928	850
132355	3928	853
132356	3928	857
132357	3928	860
132358	3928	871
132359	3928	872
132360	3928	874
132361	3929	740
132362	3929	794
132363	3929	851
132364	3929	859
132365	3929	860
132366	3930	740
132367	3930	794
132368	3930	851
132369	3930	859
132370	3930	860
132371	3931	732
132372	3931	734
132373	3931	740
132374	3931	743
132375	3931	746
132376	3931	748
132377	3931	752
132378	3931	760
132379	3931	761
132380	3931	764
132381	3931	768
132382	3931	772
132383	3931	777
132384	3931	783
132385	3931	787
132386	3931	789
132387	3931	792
132388	3931	795
132389	3931	797
132390	3931	802
132391	3931	806
132392	3931	811
132393	3931	819
132394	3931	823
132395	3931	827
132396	3931	831
132397	3931	835
132398	3931	840
132399	3931	845
132400	3931	846
132401	3931	851
132402	3931	852
132403	3931	859
132404	3931	860
132405	3931	871
132406	3931	873
132407	3931	874
132408	3932	732
132409	3932	734
132410	3932	740
132411	3932	743
132412	3932	745
132413	3932	749
132414	3932	753
132415	3932	759
132416	3932	761
132417	3932	764
132418	3932	768
132419	3932	774
132420	3932	777
132421	3932	784
132422	3932	787
132423	3932	789
132424	3932	793
132425	3932	794
132426	3932	807
132427	3932	814
132428	3932	819
132429	3932	822
132430	3932	827
132431	3932	832
132432	3932	835
132433	3932	841
132434	3932	845
132435	3932	846
132436	3932	851
132437	3932	852
132438	3932	859
132439	3932	860
132440	3932	871
132441	3932	873
132442	3932	874
132443	3933	732
132444	3933	735
132445	3933	737
132446	3933	740
132447	3933	744
132448	3933	745
132449	3933	749
132450	3933	753
132451	3933	759
132452	3933	761
132453	3933	764
132454	3933	768
132455	3933	775
132456	3933	781
132457	3933	785
132458	3933	787
132459	3933	789
132460	3933	793
132461	3933	794
132462	3933	807
132463	3933	815
132464	3933	819
132465	3933	823
132466	3933	827
132467	3933	832
132468	3933	835
132469	3933	841
132470	3933	845
132471	3933	846
132472	3933	851
132473	3933	852
132474	3933	859
132475	3933	860
132476	3933	871
132477	3933	872
132478	3933	874
132479	3934	732
132480	3934	734
132481	3934	740
132482	3934	744
132483	3934	745
132484	3934	748
132485	3934	753
132486	3934	760
132487	3934	761
132488	3934	764
132489	3934	768
132490	3934	775
132491	3934	781
132492	3934	784
132493	3934	787
132494	3934	789
132495	3934	792
132496	3934	794
132497	3934	806
132498	3934	815
132499	3934	818
132500	3934	822
132501	3934	827
132502	3934	831
132503	3934	835
132504	3934	841
132505	3934	845
132506	3934	846
132507	3934	851
132508	3934	852
132509	3934	859
132510	3934	860
132511	3934	871
132512	3934	874
132513	3935	732
132514	3935	734
132515	3935	740
132516	3935	744
132517	3935	745
132518	3935	750
132519	3935	754
132520	3935	760
132521	3935	761
132522	3935	764
132523	3935	768
132524	3935	775
132525	3935	781
132526	3935	783
132527	3935	787
132528	3935	789
132529	3935	793
132530	3935	794
132531	3935	807
132532	3935	815
132533	3935	819
132534	3935	822
132535	3935	827
132536	3935	832
132537	3935	835
132538	3935	841
132539	3935	845
132540	3935	846
132541	3935	851
132542	3935	852
132543	3935	859
132544	3935	860
132545	3935	871
132546	3935	874
132547	3936	732
132548	3936	734
132549	3936	740
132550	3936	744
132551	3936	746
132552	3936	749
132553	3936	754
132554	3936	759
132555	3936	761
132556	3936	764
132557	3936	768
132558	3936	772
132559	3936	777
132560	3936	784
132561	3936	787
132562	3936	789
132563	3936	792
132564	3936	794
132565	3936	808
132566	3936	811
132567	3936	819
132568	3936	822
132569	3936	828
132570	3936	832
132571	3936	835
132572	3936	842
132573	3936	845
132574	3936	847
132575	3936	851
132576	3936	853
132577	3936	858
132578	3936	860
132579	3936	871
132580	3936	874
132581	3937	732
132582	3937	734
132583	3937	740
132584	3937	742
132585	3937	746
132586	3937	748
132587	3937	753
132588	3937	759
132589	3937	761
132590	3937	764
132591	3937	768
132592	3937	772
132593	3937	777
132594	3937	783
132595	3937	787
132596	3937	789
132597	3937	792
132598	3937	794
132599	3937	806
132600	3937	811
132601	3937	818
132602	3937	822
132603	3937	828
132604	3937	832
132605	3937	835
132606	3937	842
132607	3937	844
132608	3937	848
132609	3937	850
132610	3937	854
132611	3937	856
132612	3937	860
132613	3937	871
132614	3937	874
132615	3938	732
132616	3938	734
132617	3938	740
132618	3938	743
132619	3938	745
132620	3938	749
132621	3938	754
132622	3938	759
132623	3938	761
132624	3938	764
132625	3938	768
132626	3938	773
132627	3938	777
132628	3938	782
132629	3938	787
132630	3938	789
132631	3938	792
132632	3938	794
132633	3938	806
132634	3938	811
132635	3938	819
132636	3938	822
132637	3938	828
132638	3938	830
132639	3938	835
132640	3938	841
132641	3938	845
132642	3938	846
132643	3938	851
132644	3938	852
132645	3938	859
132646	3938	860
132647	3938	871
132648	3938	874
132649	3939	732
132650	3939	734
132651	3939	740
132652	3939	743
132653	3939	746
132654	3939	748
132655	3939	753
132656	3939	759
132657	3939	761
132658	3939	764
132659	3939	768
132660	3939	772
132661	3939	777
132662	3939	783
132663	3939	787
132664	3939	789
132665	3939	792
132666	3939	794
132667	3939	806
132668	3939	811
132669	3939	819
132670	3939	822
132671	3939	828
132672	3939	831
132673	3939	835
132674	3939	842
132675	3939	845
132676	3939	847
132677	3939	851
132678	3939	854
132679	3939	857
132680	3939	860
132681	3939	871
132682	3939	874
132683	3940	732
132684	3940	734
132685	3940	740
132686	3940	744
132687	3940	746
132688	3940	749
132689	3940	753
132690	3940	759
132691	3940	761
132692	3940	764
132693	3940	768
132694	3940	772
132695	3940	777
132696	3940	783
132697	3940	787
132698	3940	789
132699	3940	792
132700	3940	794
132701	3940	810
132702	3940	811
132703	3940	819
132704	3940	822
132705	3940	828
132706	3940	832
132707	3940	835
132708	3940	842
132709	3940	845
132710	3940	848
132711	3940	851
132712	3940	854
132713	3940	857
132714	3940	860
132715	3940	871
132716	3940	872
132717	3940	874
132718	3941	732
132719	3941	734
132720	3941	740
132721	3941	744
132722	3941	746
132723	3941	749
132724	3941	753
132725	3941	759
132726	3941	761
132727	3941	764
132728	3941	768
132729	3941	772
132730	3941	777
132731	3941	783
132732	3941	787
132733	3941	789
132734	3941	793
132735	3941	794
132736	3941	806
132737	3941	811
132738	3941	819
132739	3941	823
132740	3941	828
132741	3941	831
132742	3941	836
132743	3941	841
132744	3941	845
132745	3941	846
132746	3941	851
132747	3941	853
132748	3941	858
132749	3941	868
132750	3941	871
132751	3941	872
132752	3941	876
132753	3942	732
132754	3942	735
132755	3942	737
132756	3942	741
132757	3942	744
132758	3942	746
132759	3942	748
132760	3942	752
132761	3942	760
132762	3942	761
132763	3942	764
132764	3942	768
132765	3942	774
132766	3942	777
132767	3942	784
132768	3942	787
132769	3942	789
132770	3942	793
132771	3942	794
132772	3942	806
132773	3942	815
132774	3942	818
132775	3942	822
132776	3942	828
132777	3942	832
132778	3942	835
132779	3942	841
132780	3942	845
132781	3942	847
132782	3942	851
132783	3942	853
132784	3942	857
132785	3942	860
132786	3943	732
132787	3943	734
132788	3943	740
132789	3943	743
132790	3943	746
132791	3943	748
132792	3943	753
132793	3943	758
132794	3943	761
132795	3943	764
132796	3943	768
132797	3943	772
132798	3943	777
132799	3943	783
132800	3943	787
132801	3943	789
132802	3943	792
132803	3943	794
132804	3943	808
132805	3943	811
132806	3943	819
132807	3943	822
132808	3943	827
132809	3943	832
132810	3943	835
132811	3943	842
132812	3943	845
132813	3943	847
132814	3943	851
132815	3943	853
132816	3943	858
132817	3943	860
132818	3944	732
132819	3944	734
132820	3944	740
132821	3944	744
132822	3944	746
132823	3944	749
132824	3944	754
132825	3944	758
132826	3944	761
132827	3944	764
132828	3944	768
132829	3944	772
132830	3944	777
132831	3944	783
132832	3944	787
132833	3944	789
132834	3944	792
132835	3944	795
132836	3944	797
132837	3944	802
132838	3944	806
132839	3944	811
132840	3944	819
132841	3944	822
132842	3944	828
132843	3944	831
132844	3944	835
132845	3944	841
132846	3944	844
132847	3944	848
132848	3944	850
132849	3944	854
132850	3944	856
132851	3944	860
132852	3944	871
132853	3944	872
132854	3944	874
132855	3945	732
132856	3945	734
132857	3945	740
132858	3945	743
132859	3945	746
132860	3945	749
132861	3945	754
132862	3945	761
132863	3945	764
132864	3945	768
132865	3945	772
132866	3945	777
132867	3945	787
132868	3945	789
132869	3945	794
132870	3945	807
132871	3945	811
132872	3945	819
132873	3945	822
132874	3945	828
132875	3945	856
132876	3945	860
132877	3946	732
132878	3946	734
132879	3946	740
132880	3946	742
132881	3946	746
132882	3946	748
132883	3946	753
132884	3946	758
132885	3946	761
132886	3946	764
132887	3946	768
132888	3946	772
132889	3946	777
132890	3946	782
132891	3946	787
132892	3946	789
132893	3946	791
132894	3946	794
132895	3946	808
132896	3946	811
132897	3946	818
132898	3946	821
132899	3946	827
132900	3946	831
132901	3946	835
132902	3946	841
132903	3946	843
132904	3946	847
132905	3946	849
132906	3946	853
132907	3946	856
132908	3946	860
132909	3946	871
132910	3946	872
132911	3946	874
132912	3947	732
132913	3947	734
132914	3947	740
132915	3947	743
132916	3947	746
132917	3947	749
132918	3947	753
132919	3947	758
132920	3947	761
132921	3947	764
132922	3947	768
132923	3947	772
132924	3947	777
132925	3947	783
132926	3947	787
132927	3947	789
132928	3947	792
132929	3947	794
132930	3947	808
132931	3947	811
132932	3947	819
132933	3947	822
132934	3947	828
132935	3947	830
132936	3947	835
132937	3947	841
132938	3947	845
132939	3947	847
132940	3947	851
132941	3947	853
132942	3947	857
132943	3947	860
132944	3947	871
132945	3947	872
132946	3947	874
132947	3948	732
132948	3948	734
132949	3948	740
132950	3948	743
132951	3948	747
132952	3948	749
132953	3948	754
132954	3948	761
132955	3948	764
132956	3948	768
132957	3948	772
132958	3948	777
132959	3948	787
132960	3948	789
132961	3948	794
132962	3948	809
132963	3948	811
132964	3948	819
132965	3948	822
132966	3948	828
132967	3948	860
132968	3949	732
132969	3949	734
132970	3949	740
132971	3949	744
132972	3949	746
132973	3949	749
132974	3949	753
132975	3949	761
132976	3949	764
132977	3949	768
132978	3949	774
132979	3949	781
132980	3949	787
132981	3949	789
132982	3949	794
132983	3949	806
132984	3949	815
132985	3949	819
132986	3949	822
132987	3949	827
132988	3949	860
132989	3950	732
132990	3950	734
132991	3950	740
132992	3950	744
132993	3950	746
132994	3950	748
132995	3950	753
132996	3950	761
132997	3950	764
132998	3950	768
132999	3950	776
133000	3950	781
133001	3950	787
133002	3950	789
133003	3950	794
133004	3950	807
133005	3950	815
133006	3950	819
133007	3950	823
133008	3950	826
133009	3950	835
133010	3950	859
133011	3950	865
133012	3950	871
133013	3950	876
133014	3951	732
133015	3951	734
133016	3951	740
133017	3951	743
133018	3951	746
133019	3951	748
133020	3951	753
133021	3951	757
133022	3951	761
133023	3951	764
133024	3951	768
133025	3951	772
133026	3951	780
133027	3951	783
133028	3951	787
133029	3951	789
133030	3951	792
133031	3951	794
133032	3951	807
133033	3951	811
133034	3951	819
133035	3951	823
133036	3951	828
133037	3951	830
133038	3951	836
133039	3951	841
133040	3951	845
133041	3951	847
133042	3951	851
133043	3951	853
133044	3951	857
133045	3951	868
133046	3951	871
133047	3951	872
133048	3951	876
133049	3952	732
133050	3952	734
133051	3952	740
133052	3952	744
133053	3952	746
133054	3952	748
133055	3952	752
133056	3952	758
133057	3952	761
133058	3952	764
133059	3952	768
133060	3952	772
133061	3952	777
133062	3952	783
133063	3952	787
133064	3952	789
133065	3952	793
133066	3952	794
133067	3952	806
133068	3952	811
133069	3952	818
133070	3952	822
133071	3952	827
133072	3952	831
133073	3952	835
133074	3952	842
133075	3952	845
133076	3952	847
133077	3952	851
133078	3952	853
133079	3952	859
133080	3952	860
133081	3952	871
133082	3952	873
133083	3952	874
133084	3953	732
133085	3953	734
133086	3953	740
133087	3953	743
133088	3953	745
133089	3953	750
133090	3953	754
133091	3953	758
133092	3953	761
133093	3953	764
133094	3953	768
133095	3953	772
133096	3953	777
133097	3953	783
133098	3953	787
133099	3953	789
133100	3953	792
133101	3953	794
133102	3953	806
133103	3953	811
133104	3953	819
133105	3953	822
133106	3953	828
133107	3953	830
133108	3953	835
133109	3953	841
133110	3953	845
133111	3953	846
133112	3953	851
133113	3953	852
133114	3953	859
133115	3953	860
133116	3953	871
133117	3953	873
133118	3953	874
133119	3954	732
133120	3954	735
133121	3954	737
133122	3954	740
133123	3954	743
133124	3954	745
133125	3954	748
133126	3954	752
133127	3954	760
133128	3954	763
133129	3954	764
133130	3954	768
133131	3954	775
133132	3954	781
133133	3954	782
133134	3954	787
133135	3954	789
133136	3954	792
133137	3954	794
133138	3954	806
133139	3954	815
133140	3954	817
133141	3954	822
133142	3954	825
133143	3954	835
133144	3955	733
133145	3955	734
133146	3955	740
133147	3955	743
133148	3955	745
133149	3955	749
133150	3955	753
133151	3955	759
133152	3955	761
133153	3955	764
133154	3955	768
133155	3955	772
133156	3955	777
133157	3955	783
133158	3955	787
133159	3955	789
133160	3955	792
133161	3955	794
133162	3955	806
133163	3955	811
133164	3955	819
133165	3955	823
133166	3955	826
133167	3955	831
133168	3955	835
133169	3955	841
133170	3955	844
133171	3955	847
133172	3955	850
133173	3955	853
133174	3955	857
133175	3955	860
133176	3955	869
133177	3955	872
133178	3955	874
133179	3956	733
133180	3956	735
133181	3956	737
133182	3956	740
133183	3956	743
133184	3956	745
133185	3956	749
133186	3956	753
133187	3956	760
133188	3956	761
133189	3956	764
133190	3956	768
133191	3956	774
133192	3956	777
133193	3956	783
133194	3956	787
133195	3956	789
133196	3956	792
133197	3956	794
133198	3956	806
133199	3956	815
133200	3956	818
133201	3956	821
133202	3956	826
133203	3956	832
133204	3956	835
133205	3956	841
133206	3956	845
133207	3956	846
133208	3956	851
133209	3956	852
133210	3956	858
133211	3956	860
133212	3956	871
133213	3956	872
133214	3956	874
133215	3957	732
133216	3957	734
133217	3957	740
133218	3957	744
133219	3957	746
133220	3957	749
133221	3957	755
133222	3957	758
133223	3957	761
133224	3957	764
133225	3957	768
133226	3957	773
133227	3957	777
133228	3957	784
133229	3957	787
133230	3957	789
133231	3957	792
133232	3957	794
133233	3957	806
133234	3957	814
133235	3957	819
133236	3957	823
133237	3957	826
133238	3957	830
133239	3957	835
133240	3957	841
133241	3957	845
133242	3957	846
133243	3957	851
133244	3957	852
133245	3957	859
133246	3957	860
133247	3957	871
133248	3957	873
133249	3957	874
133250	3958	733
133251	3958	735
133252	3958	737
133253	3958	741
133254	3958	743
133255	3958	746
133256	3958	749
133257	3958	753
133258	3958	758
133259	3958	761
133260	3958	764
133261	3958	768
133262	3958	775
133263	3958	781
133264	3958	783
133265	3958	787
133266	3958	789
133267	3958	793
133268	3958	794
133269	3958	806
133270	3958	815
133271	3958	819
133272	3958	823
133273	3958	828
133274	3958	830
133275	3958	835
133276	3958	841
133277	3958	845
133278	3958	846
133279	3958	851
133280	3958	852
133281	3958	858
133282	3958	860
133283	3958	871
133284	3958	872
133285	3958	874
133286	3959	732
133287	3959	735
133288	3959	737
133289	3959	740
133290	3959	743
133291	3959	746
133292	3959	748
133293	3959	752
133294	3959	760
133295	3959	761
133296	3959	764
133297	3959	768
133298	3959	775
133299	3959	781
133300	3959	784
133301	3959	787
133302	3959	789
133303	3959	793
133304	3959	794
133305	3959	807
133306	3959	813
133307	3959	819
133308	3959	823
133309	3959	826
133310	3959	832
133311	3959	835
133312	3959	840
133313	3959	845
133314	3959	846
133315	3959	851
133316	3959	852
133317	3959	858
133318	3959	860
133319	3959	871
133320	3959	873
133321	3959	874
133322	3960	732
133323	3960	734
133324	3960	740
133325	3960	744
133326	3960	745
133327	3960	750
133328	3960	754
133329	3960	761
133330	3960	764
133331	3960	768
133332	3960	774
133333	3960	780
133334	3960	787
133335	3960	789
133336	3960	794
133337	3960	806
133338	3960	813
133339	3960	819
133340	3960	823
133341	3960	828
133342	3960	860
133343	3960	876
133344	3961	732
133345	3961	734
133346	3961	740
133347	3961	744
133348	3961	746
133349	3961	748
133350	3961	753
133351	3961	758
133352	3961	761
133353	3961	764
133354	3961	768
133355	3961	772
133356	3961	777
133357	3961	783
133358	3961	787
133359	3961	789
133360	3961	793
133361	3961	794
133362	3961	808
133363	3961	811
133364	3961	819
133365	3961	822
133366	3961	828
133367	3961	832
133368	3961	836
133369	3961	841
133370	3961	845
133371	3961	847
133372	3961	851
133373	3961	853
133374	3961	857
133375	3961	865
133376	3961	871
133377	3961	872
133378	3961	874
133379	3962	732
133380	3962	734
133381	3962	740
133382	3962	743
133383	3962	746
133384	3962	749
133385	3962	753
133386	3962	760
133387	3962	761
133388	3962	765
133389	3962	770
133390	3962	775
133391	3962	777
133392	3962	784
133393	3962	787
133394	3962	789
133395	3962	793
133396	3962	795
133397	3962	797
133398	3962	802
133399	3962	807
133400	3962	814
133401	3962	819
133402	3962	823
133403	3962	828
133404	3962	832
133405	3962	836
133406	3962	842
133407	3962	845
133408	3962	848
133409	3962	851
133410	3962	854
133411	3962	857
133412	3962	860
133413	3962	871
133414	3962	873
133415	3962	874
133416	3963	732
133417	3963	734
133418	3963	740
133419	3963	743
133420	3963	746
133421	3963	748
133422	3963	753
133423	3963	759
133424	3963	761
133425	3963	764
133426	3963	768
133427	3963	772
133428	3963	777
133429	3963	784
133430	3963	787
133431	3963	789
133432	3963	792
133433	3963	795
133434	3963	798
133435	3963	803
133436	3963	808
133437	3963	811
133438	3963	818
133439	3963	822
133440	3963	828
133441	3963	831
133442	3963	835
133443	3963	842
133444	3963	845
133445	3963	847
133446	3963	851
133447	3963	853
133448	3963	858
133449	3963	860
133450	3963	871
133451	3963	873
133452	3963	874
133453	3964	732
133454	3964	734
133455	3964	740
133456	3964	743
133457	3964	746
133458	3964	749
133459	3964	753
133460	3964	757
133461	3964	761
133462	3964	764
133463	3964	768
133464	3964	772
133465	3964	777
133466	3964	783
133467	3964	787
133468	3964	789
133469	3964	792
133470	3964	794
133471	3964	806
133472	3964	811
133473	3964	819
133474	3964	822
133475	3964	828
133476	3964	830
133477	3964	835
133478	3964	842
133479	3964	845
133480	3964	847
133481	3964	851
133482	3964	853
133483	3964	857
133484	3964	860
133485	3964	871
133486	3964	872
133487	3964	874
133488	3965	733
133489	3965	734
133490	3965	740
133491	3965	744
133492	3965	746
133493	3965	748
133494	3965	752
133495	3965	759
133496	3965	761
133497	3965	764
133498	3965	768
133499	3965	772
133500	3965	777
133501	3965	784
133502	3965	787
133503	3965	789
133504	3965	793
133505	3965	794
133506	3965	807
133507	3965	811
133508	3965	819
133509	3965	823
133510	3965	827
133511	3965	832
133512	3965	835
133513	3965	841
133514	3965	844
133515	3965	847
133516	3965	850
133517	3965	853
133518	3965	857
133519	3965	860
133520	3965	871
133521	3965	872
133522	3965	874
133523	3966	732
133524	3966	734
133525	3966	740
133526	3966	743
133527	3966	746
133528	3966	749
133529	3966	753
133530	3966	758
133531	3966	761
133532	3966	764
133533	3966	768
133534	3966	773
133535	3966	777
133536	3966	782
133537	3966	787
133538	3966	789
133539	3966	792
133540	3966	794
133541	3966	807
133542	3966	814
133543	3966	819
133544	3966	822
133545	3966	826
133546	3966	832
133547	3966	835
133548	3966	842
133549	3966	845
133550	3966	847
133551	3966	851
133552	3966	853
133553	3966	858
133554	3966	860
133555	3966	871
133556	3966	872
133557	3966	874
133558	3967	732
133559	3967	734
133560	3967	740
133561	3967	742
133562	3967	745
133563	3967	748
133564	3967	752
133565	3967	758
133566	3967	761
133567	3967	764
133568	3967	768
133569	3967	772
133570	3967	777
133571	3967	782
133572	3967	787
133573	3967	789
133574	3967	791
133575	3967	794
133576	3967	808
133577	3967	811
133578	3967	818
133579	3967	822
133580	3967	828
133581	3967	830
133582	3967	835
133583	3967	841
133584	3967	844
133585	3967	847
133586	3967	850
133587	3967	854
133588	3967	856
133589	3967	860
133590	3967	871
133591	3967	872
133592	3967	874
133593	3968	732
133594	3968	734
133595	3968	740
133596	3968	743
133597	3968	745
133598	3968	748
133599	3968	753
133600	3968	758
133601	3968	761
133602	3968	764
133603	3968	768
133604	3968	772
133605	3968	777
133606	3968	784
133607	3968	787
133608	3968	789
133609	3968	792
133610	3968	794
133611	3968	807
133612	3968	811
133613	3968	818
133614	3968	821
133615	3968	828
133616	3968	831
133617	3968	835
133618	3968	840
133619	3968	843
133620	3968	847
133621	3968	849
133622	3968	853
133623	3968	856
133624	3968	860
133625	3968	871
133626	3968	872
133627	3968	874
133628	3969	732
133629	3969	734
133630	3969	740
133631	3969	744
133632	3969	746
133633	3969	750
133634	3969	754
133635	3969	757
133636	3969	761
133637	3969	764
133638	3969	768
133639	3969	772
133640	3969	777
133641	3969	783
133642	3969	787
133643	3969	789
133644	3969	792
133645	3969	795
133646	3969	797
133647	3969	802
133648	3969	808
133649	3969	811
133650	3969	819
133651	3969	822
133652	3969	828
133653	3969	830
133654	3969	835
133655	3969	841
133656	3969	844
133657	3969	848
133658	3969	850
133659	3969	854
133660	3969	856
133661	3969	860
133662	3969	871
133663	3969	872
133664	3969	874
133665	3970	731
133666	3970	734
133667	3970	740
133668	3970	743
133669	3970	745
133670	3970	748
133671	3970	752
133672	3970	761
133673	3970	764
133674	3970	768
133675	3970	772
133676	3970	777
133677	3970	787
133678	3970	789
133679	3970	794
133680	3970	807
133681	3970	811
133682	3970	818
133683	3970	821
133684	3970	828
133685	3970	856
133686	3970	860
133687	3971	732
133688	3971	734
133689	3971	740
133690	3971	743
133691	3971	745
133692	3971	748
133693	3971	752
133694	3971	759
133695	3971	761
133696	3971	764
133697	3971	768
133698	3971	772
133699	3971	777
133700	3971	783
133701	3971	787
133702	3971	789
133703	3971	792
133704	3971	794
133705	3971	808
133706	3971	811
133707	3971	819
133708	3971	823
133709	3971	828
133710	3971	831
133711	3971	835
133712	3971	840
133713	3971	843
133714	3971	847
133715	3971	849
133716	3971	853
133717	3971	856
133718	3971	860
133719	3971	871
133720	3971	872
133721	3971	874
133722	3972	732
133723	3972	734
133724	3972	740
133725	3972	743
133726	3972	745
133727	3972	748
133728	3972	753
133729	3972	758
133730	3972	761
133731	3972	764
133732	3972	768
133733	3972	772
133734	3972	777
133735	3972	783
133736	3972	787
133737	3972	789
133738	3972	792
133739	3972	794
133740	3972	808
133741	3972	811
133742	3972	818
133743	3972	822
133744	3972	828
133745	3972	831
133746	3972	835
133747	3972	840
133748	3972	843
133749	3972	847
133750	3972	849
133751	3972	853
133752	3972	856
133753	3972	860
133754	3972	871
133755	3972	872
133756	3972	874
133757	3973	732
133758	3973	734
133759	3973	740
133760	3973	743
133761	3973	745
133762	3973	748
133763	3973	752
133764	3973	758
133765	3973	761
133766	3973	764
133767	3973	768
133768	3973	772
133769	3973	777
133770	3973	783
133771	3973	787
133772	3973	789
133773	3973	792
133774	3973	794
133775	3973	807
133776	3973	811
133777	3973	818
133778	3973	823
133779	3973	826
133780	3973	831
133781	3973	835
133782	3973	841
133783	3973	843
133784	3973	847
133785	3973	849
133786	3973	853
133787	3973	856
133788	3973	860
133789	3973	871
133790	3973	872
133791	3973	874
133792	3974	732
133793	3974	734
133794	3974	740
133795	3974	742
133796	3974	746
133797	3974	749
133798	3974	753
133799	3974	758
133800	3974	761
133801	3974	764
133802	3974	768
133803	3974	772
133804	3974	777
133805	3974	782
133806	3974	787
133807	3974	789
133808	3974	791
133809	3974	794
133810	3974	808
133811	3974	811
133812	3974	818
133813	3974	822
133814	3974	826
133815	3974	831
133816	3974	835
133817	3974	842
133818	3974	844
133819	3974	848
133820	3974	850
133821	3974	854
133822	3974	856
133823	3974	860
133824	3974	871
133825	3974	872
133826	3974	874
133827	3975	732
133828	3975	734
133829	3975	740
133830	3975	742
133831	3975	746
133832	3975	749
133833	3975	753
133834	3975	758
133835	3975	761
133836	3975	764
133837	3975	768
133838	3975	772
133839	3975	777
133840	3975	782
133841	3975	787
133842	3975	789
133843	3975	792
133844	3975	794
133845	3975	808
133846	3975	811
133847	3975	819
133848	3975	822
133849	3975	828
133850	3975	831
133851	3975	835
133852	3975	842
133853	3975	844
133854	3975	847
133855	3975	850
133856	3975	853
133857	3975	856
133858	3975	860
133859	3977	733
133860	3977	735
133861	3977	737
133862	3977	741
133863	3977	744
133864	3977	745
133865	3977	748
133866	3977	752
133867	3977	759
133868	3977	761
133869	3977	764
133870	3977	768
133871	3977	775
133872	3977	781
133873	3977	782
133874	3977	787
133875	3977	789
133876	3977	792
133877	3977	794
133878	3977	806
133879	3977	815
133880	3977	819
133881	3977	822
133882	3977	825
133883	3977	831
133884	3977	835
133885	3977	841
133886	3977	845
133887	3977	846
133888	3977	851
133889	3977	852
133890	3977	859
133891	3977	861
133892	3977	871
133893	3977	872
133894	3977	874
133895	3978	732
133896	3978	735
133897	3978	737
133898	3978	740
133899	3978	744
133900	3978	746
133901	3978	748
133902	3978	752
133903	3978	759
133904	3978	763
133905	3978	764
133906	3978	768
133907	3978	775
133908	3978	781
133909	3978	782
133910	3978	787
133911	3978	789
133912	3978	793
133913	3978	794
133914	3978	807
133915	3978	815
133916	3978	819
133917	3978	822
133918	3978	825
133919	3978	831
133920	3978	835
133921	3978	840
133922	3978	845
133923	3978	846
133924	3978	851
133925	3978	852
133926	3978	859
133927	3978	860
133928	3978	871
133929	3978	872
133930	3978	874
133931	3979	732
133932	3979	735
133933	3979	737
133934	3979	740
133935	3979	744
133936	3979	746
133937	3979	749
133938	3979	754
133939	3979	761
133940	3979	766
133941	3979	770
133942	3979	775
133943	3979	781
133944	3979	787
133945	3979	790
133946	3979	794
133947	3979	808
133948	3979	815
133949	3979	856
133950	3979	860
133951	3979	871
133952	3979	872
133953	3979	874
133954	3980	732
133955	3980	734
133956	3980	740
133957	3980	744
133958	3980	746
133959	3980	749
133960	3980	753
133961	3980	758
133962	3980	761
133963	3980	764
133964	3980	768
133965	3980	772
133966	3980	777
133967	3980	785
133968	3980	787
133969	3980	789
133970	3980	793
133971	3980	794
133972	3980	808
133973	3980	811
133974	3980	819
133975	3980	822
133976	3980	828
133977	3980	832
133978	3980	835
133979	3980	842
133980	3980	845
133981	3980	848
133982	3980	851
133983	3980	854
133984	3980	856
133985	3980	860
133986	3980	871
133987	3980	872
133988	3980	874
133989	3981	732
133990	3981	734
133991	3981	740
133992	3981	744
133993	3981	747
133994	3981	748
133995	3981	753
133996	3981	758
133997	3981	761
133998	3981	764
133999	3981	768
134000	3981	775
134001	3981	777
134002	3981	784
134003	3981	787
134004	3981	789
134005	3981	793
134006	3981	794
134007	3981	808
134008	3981	814
134009	3981	819
134010	3981	822
134011	3981	828
134012	3981	832
134013	3981	836
134014	3981	842
134015	3981	845
134016	3981	848
134017	3981	851
134018	3981	854
134019	3981	857
134020	3981	860
134021	3981	871
134022	3981	872
134023	3981	874
134024	3982	733
134025	3982	734
134026	3982	740
134027	3982	742
134028	3982	745
134029	3982	749
134030	3982	754
134031	3982	758
134032	3982	761
134033	3982	764
134034	3982	768
134035	3982	773
134036	3982	777
134037	3982	783
134038	3982	787
134039	3982	789
134040	3982	793
134041	3982	794
134042	3982	807
134043	3982	814
134044	3982	819
134045	3982	822
134046	3982	826
134047	3982	832
134048	3982	835
134049	3982	841
134050	3982	845
134051	3982	847
134052	3982	851
134053	3982	853
134054	3982	858
134055	3982	860
134056	3982	871
134057	3982	872
134058	3982	874
134059	3983	740
134060	3983	782
134061	3983	794
134062	3983	851
134063	3983	858
134064	3983	860
134065	3983	874
134066	3984	732
134067	3984	734
134068	3984	740
134069	3984	743
134070	3984	746
134071	3984	749
134072	3984	754
134073	3984	759
134074	3984	761
134075	3984	764
134076	3984	768
134077	3984	772
134078	3984	777
134079	3984	783
134080	3984	787
134081	3984	789
134082	3984	792
134083	3984	795
134084	3984	797
134085	3984	802
134086	3984	809
134087	3984	811
134088	3984	819
134089	3984	822
134090	3984	828
134091	3984	832
134092	3984	835
134093	3984	842
134094	3984	845
134095	3984	847
134096	3984	851
134097	3984	853
134098	3984	858
134099	3984	860
134100	3984	871
134101	3984	872
134102	3984	874
134103	3985	740
134104	3985	784
134105	3985	794
134106	3985	857
134107	3985	860
134108	3985	874
134109	3986	740
134110	3986	784
134111	3986	794
134112	3986	857
134113	3986	860
134114	3986	874
134115	3987	740
134116	3987	782
134117	3987	794
134118	3987	849
134119	3987	855
134120	3987	860
134121	3987	874
134122	3988	732
134123	3988	734
134124	3988	740
134125	3988	743
134126	3988	745
134127	3988	749
134128	3988	754
134129	3988	759
134130	3988	761
134131	3988	764
134132	3988	768
134133	3988	772
134134	3988	777
134135	3988	783
134136	3988	787
134137	3988	789
134138	3988	792
134139	3988	794
134140	3988	807
134141	3988	811
134142	3988	819
134143	3988	823
134144	3988	828
134145	3988	832
134146	3988	835
134147	3988	841
134148	3988	844
134149	3988	847
134150	3988	849
134151	3988	853
134152	3988	856
134153	3988	860
134154	3988	871
134155	3988	872
134156	3988	874
134157	3989	740
134158	3989	757
134159	3989	782
134160	3989	794
134161	3989	849
134162	3989	855
134163	3989	860
134164	3989	874
134165	3990	740
134166	3990	782
134167	3990	794
134168	3990	857
134169	3990	860
134170	3990	874
134171	3991	740
134172	3991	758
134173	3991	795
134174	3991	851
134175	3991	858
134176	3991	860
134177	3991	874
134178	3992	740
134179	3992	758
134180	3992	795
134181	3992	851
134182	3992	858
134183	3992	860
134184	3992	874
134185	3993	740
134186	3993	783
134187	3993	794
134188	3993	857
134189	3993	860
134190	3993	874
134191	3994	731
134192	3994	734
134193	3994	740
134194	3994	744
134195	3994	747
134196	3994	749
134197	3994	753
134198	3994	758
134199	3994	761
134200	3994	764
134201	3994	768
134202	3994	774
134203	3994	777
134204	3994	784
134205	3994	787
134206	3994	789
134207	3994	793
134208	3994	794
134209	3994	808
134210	3994	814
134211	3994	819
134212	3994	823
134213	3994	827
134214	3994	831
134215	3994	837
134216	3994	842
134217	3994	845
134218	3994	848
134219	3994	851
134220	3994	854
134221	3994	857
134222	3994	860
134223	3994	871
134224	3994	873
134225	3994	874
134226	3995	732
134227	3995	734
134228	3995	740
134229	3995	744
134230	3995	745
134231	3995	748
134232	3995	753
134233	3995	758
134234	3995	761
134235	3995	764
134236	3995	768
134237	3995	772
134238	3995	777
134239	3995	783
134240	3995	787
134241	3995	789
134242	3995	792
134243	3995	794
134244	3995	808
134245	3995	811
134246	3995	819
134247	3995	822
134248	3995	828
134249	3995	831
134250	3995	835
134251	3995	842
134252	3995	845
134253	3995	848
134254	3995	851
134255	3995	854
134256	3995	857
134257	3995	860
134258	3995	871
134259	3995	872
134260	3995	874
134261	3996	732
134262	3996	735
134263	3996	737
134264	3996	740
134265	3996	744
134266	3996	746
134267	3996	749
134268	3996	754
134269	3996	761
134270	3996	764
134271	3996	768
134272	3996	775
134273	3996	781
134274	3996	787
134275	3996	790
134276	3996	794
134277	3996	807
134278	3996	815
134279	3996	819
134280	3996	823
134281	3996	828
134282	3996	856
134283	3996	874
134284	3997	732
134285	3997	734
134286	3997	740
134287	3997	743
134288	3997	746
134289	3997	748
134290	3997	753
134291	3997	758
134292	3997	761
134293	3997	764
134294	3997	768
134295	3997	774
134296	3997	781
134297	3997	783
134298	3997	787
134299	3997	789
134300	3997	793
134301	3997	794
134302	3997	808
134303	3997	815
134304	3997	819
134305	3997	823
134306	3997	828
134307	3997	832
134308	3997	835
134309	3997	841
134310	3997	844
134311	3997	847
134312	3997	850
134313	3997	853
134314	3997	856
134315	3997	865
134316	3997	871
134317	3998	732
134318	3998	734
134319	3998	740
134320	3998	744
134321	3998	746
134322	3998	749
134323	3998	753
134324	3998	758
134325	3998	761
134326	3998	764
134327	3998	768
134328	3998	775
134329	3998	777
134330	3998	784
134331	3998	787
134332	3998	789
134333	3998	793
134334	3998	794
134335	3998	806
134336	3998	815
134337	3998	819
134338	3998	822
134339	3998	827
134340	3998	830
134341	3998	835
134342	3998	841
134343	3998	845
134344	3998	846
134345	3998	851
134346	3998	852
134347	3998	859
134348	3998	860
134349	3998	871
134350	3998	873
134351	3998	874
134352	3999	732
134353	3999	734
134354	3999	740
134355	3999	743
134356	3999	746
134357	3999	749
134358	3999	753
134359	3999	758
134360	3999	761
134361	3999	764
134362	3999	768
134363	3999	772
134364	3999	777
134365	3999	783
134366	3999	787
134367	3999	789
134368	3999	792
134369	3999	794
134370	3999	809
134371	3999	811
134372	3999	819
134373	3999	823
134374	3999	828
134375	3999	830
134376	3999	835
134377	3999	842
134378	3999	845
134379	3999	848
134380	3999	851
134381	3999	854
134382	3999	856
134383	3999	860
134384	3999	871
134385	3999	873
134386	3999	874
134387	4000	732
134388	4000	734
134389	4000	740
134390	4000	743
134391	4000	746
134392	4000	749
134393	4000	753
134394	4000	759
134395	4000	761
134396	4000	764
134397	4000	768
134398	4000	776
134399	4000	781
134400	4000	785
134401	4000	787
134402	4000	789
134403	4000	792
134404	4000	794
134405	4000	806
134406	4000	815
134407	4000	819
134408	4000	822
134409	4000	826
134410	4000	832
134411	4000	835
134412	4000	842
134413	4000	845
134414	4000	848
134415	4000	851
134416	4000	854
134417	4000	857
134418	4000	860
134419	4001	732
134420	4001	734
134421	4001	740
134422	4001	743
134423	4001	746
134424	4001	748
134425	4001	753
134426	4001	758
134427	4001	761
134428	4001	764
134429	4001	768
134430	4001	775
134431	4001	781
134432	4001	783
134433	4001	787
134434	4001	789
134435	4001	792
134436	4001	794
134437	4001	806
134438	4001	815
134439	4001	819
134440	4001	822
134441	4001	827
134442	4001	830
134443	4001	835
134444	4001	841
134445	4001	845
134446	4001	846
134447	4001	851
134448	4001	852
134449	4001	859
134450	4001	860
134451	4001	871
134452	4001	873
134453	4001	874
134454	4002	733
134455	4002	734
134456	4002	740
134457	4002	743
134458	4002	746
134459	4002	749
134460	4002	753
134461	4002	760
134462	4002	761
134463	4002	764
134464	4002	768
134465	4002	772
134466	4002	777
134467	4002	783
134468	4002	787
134469	4002	790
134470	4002	792
134471	4002	794
134472	4002	806
134473	4002	811
134474	4002	818
134475	4002	821
134476	4002	827
134477	4002	833
134478	4002	836
134479	4002	841
134480	4002	844
134481	4002	847
134482	4002	850
134483	4002	853
134484	4002	856
134485	4002	860
134486	4003	732
134487	4003	734
134488	4003	740
134489	4003	743
134490	4003	746
134491	4003	750
134492	4003	754
134493	4003	758
134494	4003	761
134495	4003	764
134496	4003	768
134497	4003	772
134498	4003	777
134499	4003	783
134500	4003	787
134501	4003	789
134502	4003	792
134503	4003	794
134504	4003	808
134505	4003	811
134506	4003	819
134507	4003	823
134508	4003	828
134509	4003	830
134510	4003	835
134511	4003	842
134512	4003	845
134513	4003	847
134514	4003	851
134515	4003	853
134516	4003	858
134517	4003	860
134518	4004	732
134519	4004	734
134520	4004	740
134521	4004	743
134522	4004	745
134523	4004	748
134524	4004	752
134525	4004	759
134526	4004	761
134527	4004	764
134528	4004	768
134529	4004	772
134530	4004	777
134531	4004	783
134532	4004	787
134533	4004	789
134534	4004	792
134535	4004	794
134536	4004	806
134537	4004	811
134538	4004	819
134539	4004	823
134540	4004	826
134541	4004	832
134542	4004	835
134543	4004	840
134544	4004	845
134545	4004	846
134546	4004	851
134547	4004	852
134548	4004	859
134549	4004	860
134550	4004	871
134551	4005	732
134552	4005	734
134553	4005	740
134554	4005	744
134555	4005	746
134556	4005	750
134557	4005	755
134558	4005	758
134559	4005	761
134560	4005	764
134561	4005	768
134562	4005	772
134563	4005	777
134564	4005	787
134565	4005	789
134566	4005	794
134567	4005	808
134568	4005	811
134569	4005	819
134570	4005	823
134571	4005	828
134572	4005	835
134573	4005	842
134574	4005	845
134575	4005	848
134576	4005	851
134577	4005	854
134578	4005	857
134579	4005	860
134580	4005	871
134581	4005	872
134582	4005	874
134583	4006	731
134584	4006	734
134585	4006	740
134586	4006	744
134587	4006	746
134588	4006	749
134589	4006	754
134590	4006	757
134591	4006	761
134592	4006	764
134593	4006	768
134594	4006	772
134595	4006	777
134596	4006	784
134597	4006	787
134598	4006	789
134599	4006	792
134600	4006	794
134601	4006	808
134602	4006	811
134603	4006	819
134604	4006	823
134605	4006	828
134606	4006	830
134607	4006	835
134608	4006	841
134609	4006	845
134610	4006	847
134611	4006	851
134612	4006	853
134613	4006	858
134614	4006	860
134615	4006	871
134616	4006	872
134617	4006	874
134618	4007	731
134619	4007	734
134620	4007	740
134621	4007	744
134622	4007	746
134623	4007	749
134624	4007	754
134625	4007	759
134626	4007	761
134627	4007	764
134628	4007	768
134629	4007	772
134630	4007	777
134631	4007	783
134632	4007	787
134633	4007	789
134634	4007	792
134635	4007	794
134636	4007	806
134637	4007	811
134638	4007	819
134639	4007	822
134640	4007	828
134641	4007	831
134642	4007	835
134643	4007	842
134644	4007	845
134645	4007	848
134646	4007	851
134647	4007	854
134648	4007	856
134649	4007	860
134650	4007	871
134651	4007	872
134652	4007	874
134653	4008	732
134654	4008	734
134655	4008	740
134656	4008	743
134657	4008	746
134658	4008	749
134659	4008	753
134660	4008	759
134661	4008	761
134662	4008	764
134663	4008	768
134664	4008	772
134665	4008	777
134666	4008	783
134667	4008	787
134668	4008	789
134669	4008	793
134670	4008	794
134671	4008	806
134672	4008	811
134673	4008	819
134674	4008	822
134675	4008	828
134676	4008	832
134677	4008	835
134678	4008	841
134679	4008	844
134680	4008	846
134681	4008	850
134682	4008	852
134683	4008	858
134684	4008	865
134685	4008	871
134686	4009	732
134687	4009	734
134688	4009	740
134689	4009	743
134690	4009	747
134691	4009	748
134692	4009	753
134693	4009	759
134694	4009	761
134695	4009	764
134696	4009	768
134697	4009	772
134698	4009	777
134699	4009	785
134700	4009	787
134701	4009	789
134702	4009	792
134703	4009	794
134704	4009	809
134705	4009	811
134706	4009	819
134707	4009	823
134708	4009	827
134709	4009	832
134710	4009	835
134711	4009	841
134712	4009	845
134713	4009	847
134714	4009	851
134715	4009	853
134716	4009	858
134717	4009	860
134718	4009	871
134719	4010	733
134720	4010	734
134721	4010	740
134722	4010	744
134723	4010	745
134724	4010	749
134725	4010	755
134726	4010	758
134727	4010	761
134728	4010	764
134729	4010	768
134730	4010	772
134731	4010	777
134732	4010	784
134733	4010	787
134734	4010	789
134735	4010	793
134736	4010	794
134737	4010	806
134738	4010	811
134739	4010	819
134740	4010	823
134741	4010	827
134742	4010	830
134743	4010	836
134744	4010	841
134745	4010	845
134746	4010	846
134747	4010	851
134748	4010	852
134749	4010	859
134750	4010	868
134751	4010	871
134752	4010	872
134753	4010	876
134754	4011	732
134755	4011	734
134756	4011	740
134757	4011	744
134758	4011	746
134759	4011	749
134760	4011	753
134761	4011	758
134762	4011	761
134763	4011	764
134764	4011	768
134765	4011	772
134766	4011	777
134767	4011	783
134768	4011	787
134769	4011	789
134770	4011	792
134771	4011	794
134772	4011	806
134773	4011	811
134774	4011	819
134775	4011	823
134776	4011	827
134777	4011	831
134778	4011	835
134779	4011	842
134780	4011	845
134781	4011	848
134782	4011	851
134783	4011	854
134784	4011	857
134785	4011	860
134786	4011	871
134787	4011	872
134788	4011	874
134789	4012	734
134790	4012	740
134791	4012	743
134792	4012	746
134793	4012	749
134794	4012	753
134795	4012	761
134796	4012	764
134797	4012	769
134798	4012	774
134799	4012	777
134800	4012	787
134801	4012	789
134802	4012	794
134803	4012	808
134804	4012	814
134805	4012	818
134806	4012	821
134807	4012	828
134808	4012	838
134809	4012	856
134810	4012	860
134811	4012	871
134812	4012	873
134813	4012	874
134814	4013	732
134815	4013	734
134816	4013	740
134817	4013	743
134818	4013	746
134819	4013	749
134820	4013	753
134821	4013	758
134822	4013	761
134823	4013	764
134824	4013	768
134825	4013	772
134826	4013	777
134827	4013	784
134828	4013	787
134829	4013	789
134830	4013	792
134831	4013	795
134832	4013	800
134833	4013	803
134834	4013	807
134835	4013	815
134836	4013	819
134837	4013	822
134838	4013	827
134839	4013	831
134840	4013	835
134841	4013	842
134842	4013	845
134843	4013	848
134844	4013	851
134845	4013	854
134846	4013	857
134847	4013	860
134848	4013	871
134849	4013	872
134850	4013	874
134851	4014	732
134852	4014	734
134853	4014	740
134854	4014	744
134855	4014	746
134856	4014	749
134857	4014	753
134858	4014	758
134859	4014	761
134860	4014	764
134861	4014	768
134862	4014	774
134863	4014	781
134864	4014	783
134865	4014	787
134866	4014	789
134867	4014	792
134868	4014	794
134869	4014	807
134870	4014	815
134871	4014	819
134872	4014	822
134873	4014	827
134874	4014	830
134875	4014	835
134876	4014	841
134877	4014	845
134878	4014	846
134879	4014	851
134880	4014	852
134881	4014	859
134882	4014	860
134883	4014	871
134884	4014	873
134885	4014	874
134886	4015	732
134887	4015	734
134888	4015	740
134889	4015	743
134890	4015	745
134891	4015	749
134892	4015	753
134893	4015	759
134894	4015	761
134895	4015	764
134896	4015	768
134897	4015	775
134898	4015	781
134899	4015	782
134900	4015	787
134901	4015	789
134902	4015	792
134903	4015	794
134904	4015	806
134905	4015	815
134906	4015	819
134907	4015	822
134908	4015	825
134909	4015	830
134910	4015	835
134911	4015	841
134912	4015	845
134913	4015	846
134914	4015	851
134915	4015	852
134916	4015	859
134917	4015	860
134918	4015	871
134919	4015	873
134920	4015	874
134921	4016	732
134922	4016	734
134923	4016	740
134924	4016	743
134925	4016	745
134926	4016	749
134927	4016	753
134928	4016	761
134929	4016	764
134930	4016	768
134931	4016	774
134932	4016	780
134933	4016	783
134934	4016	787
134935	4016	789
134936	4016	792
134937	4016	794
134938	4016	806
134939	4016	815
134940	4016	819
134941	4016	822
134942	4016	827
134943	4016	830
134944	4016	835
134945	4016	841
134946	4016	845
134947	4016	846
134948	4016	851
134949	4016	852
134950	4016	859
134951	4016	860
134952	4016	871
134953	4016	873
134954	4016	874
134955	4017	733
134956	4017	734
134957	4017	740
134958	4017	744
134959	4017	746
134960	4017	748
134961	4017	753
134962	4017	758
134963	4017	761
134964	4017	764
134965	4017	768
134966	4017	772
134967	4017	777
134968	4017	783
134969	4017	787
134970	4017	789
134971	4017	793
134972	4017	794
134973	4017	808
134974	4017	811
134975	4017	819
134976	4017	823
134977	4017	827
134978	4017	831
134979	4017	836
134980	4017	841
134981	4017	845
134982	4017	847
134983	4017	851
134984	4017	853
134985	4017	857
134986	4017	868
134987	4017	871
134988	4017	872
134989	4017	874
134990	4018	732
134991	4018	734
134992	4018	740
134993	4018	743
134994	4018	746
134995	4018	748
134996	4018	753
134997	4018	759
134998	4018	761
134999	4018	764
135000	4018	768
135001	4018	772
135002	4018	777
135003	4018	782
135004	4018	787
135005	4018	789
135006	4018	792
135007	4018	795
135008	4018	797
135009	4018	803
135010	4018	806
135011	4018	811
135012	4018	818
135013	4018	821
135014	4018	826
135015	4018	832
135016	4018	835
135017	4018	841
135018	4018	845
135019	4018	847
135020	4018	851
135021	4018	853
135022	4018	857
135023	4018	860
135024	4018	871
135025	4018	872
135026	4018	874
135027	4019	731
135028	4019	734
135029	4019	740
135030	4019	743
135031	4019	747
135032	4019	749
135033	4019	754
135034	4019	759
135035	4019	761
135036	4019	764
135037	4019	768
135038	4019	772
135039	4019	777
135040	4019	784
135041	4019	787
135042	4019	789
135043	4019	793
135044	4019	795
135045	4019	796
135046	4019	801
135047	4019	806
135048	4019	811
135049	4019	819
135050	4019	823
135051	4019	828
135052	4019	832
135053	4019	835
135054	4019	842
135055	4019	845
135056	4019	848
135057	4019	851
135058	4019	854
135059	4019	857
135060	4019	860
135061	4019	871
135062	4019	872
135063	4019	874
135064	4020	731
135065	4020	734
135066	4020	740
135067	4020	743
135068	4020	747
135069	4020	749
135070	4020	753
135071	4020	759
135072	4020	761
135073	4020	764
135074	4020	768
135075	4020	772
135076	4020	777
135077	4020	784
135078	4020	787
135079	4020	789
135080	4020	793
135081	4020	794
135082	4020	808
135083	4020	811
135084	4020	819
135085	4020	822
135086	4020	828
135087	4020	832
135088	4020	835
135089	4020	842
135090	4020	845
135091	4020	848
135092	4020	851
135093	4020	854
135094	4020	858
135095	4020	860
135096	4020	871
135097	4020	872
135098	4020	874
135099	4021	732
135100	4021	734
135101	4021	740
135102	4021	744
135103	4021	746
135104	4021	749
135105	4021	753
135106	4021	758
135107	4021	761
135108	4021	764
135109	4021	768
135110	4021	772
135111	4021	777
135112	4021	783
135113	4021	787
135114	4021	789
135115	4021	793
135116	4021	794
135117	4021	808
135118	4021	811
135119	4021	819
135120	4021	822
135121	4021	826
135122	4021	832
135123	4021	835
135124	4021	842
135125	4021	845
135126	4021	848
135127	4021	851
135128	4021	854
135129	4021	857
135130	4021	860
135131	4021	871
135132	4021	872
135133	4021	874
135134	4022	733
135135	4022	735
135136	4022	737
135137	4022	741
135138	4022	744
135139	4022	746
135140	4022	749
135141	4022	754
135142	4022	759
135143	4022	761
135144	4022	765
135145	4022	770
135146	4022	776
135147	4022	781
135148	4022	785
135149	4022	788
135150	4022	790
135151	4022	793
135152	4022	794
135153	4022	809
135154	4022	815
135155	4022	819
135156	4022	822
135157	4022	828
135158	4022	832
135159	4022	838
135160	4022	842
135161	4022	845
135162	4022	848
135163	4022	851
135164	4022	854
135165	4022	857
135166	4022	860
135167	4022	871
135168	4022	872
135169	4022	874
135170	4023	733
135171	4023	734
135172	4023	740
135173	4023	744
135174	4023	746
135175	4023	749
135176	4023	753
135177	4023	758
135178	4023	761
135179	4023	764
135180	4023	768
135181	4023	772
135182	4023	777
135183	4023	783
135184	4023	787
135185	4023	789
135186	4023	792
135187	4023	795
135188	4023	798
135189	4023	803
135190	4023	806
135191	4023	811
135192	4023	819
135193	4023	822
135194	4023	828
135195	4023	831
135196	4023	835
135197	4023	841
135198	4023	845
135199	4023	847
135200	4023	851
135201	4023	853
135202	4023	857
135203	4023	860
135204	4023	871
135205	4023	872
135206	4023	874
135207	4024	732
135208	4024	734
135209	4024	740
135210	4024	744
135211	4024	746
135212	4024	750
135213	4024	755
135214	4024	757
135215	4024	761
135216	4024	764
135217	4024	768
135218	4024	775
135219	4024	781
135220	4024	783
135221	4024	787
135222	4024	789
135223	4024	793
135224	4024	794
135225	4024	807
135226	4024	815
135227	4024	819
135228	4024	823
135229	4024	827
135230	4024	830
135231	4024	835
135232	4024	842
135233	4024	845
135234	4024	847
135235	4024	851
135236	4024	853
135237	4024	857
135238	4024	860
135239	4024	871
135240	4024	872
135241	4024	874
135242	4025	732
135243	4025	734
135244	4025	740
135245	4025	742
135246	4025	746
135247	4025	748
135248	4025	753
135249	4025	758
135250	4025	761
135251	4025	764
135252	4025	768
135253	4025	772
135254	4025	777
135255	4025	782
135256	4025	787
135257	4025	789
135258	4025	792
135259	4025	794
135260	4025	806
135261	4025	811
135262	4025	818
135263	4025	822
135264	4025	827
135265	4025	831
135266	4025	835
135267	4025	840
135268	4025	843
135269	4025	847
135270	4025	849
135271	4025	853
135272	4025	856
135273	4025	860
135274	4025	871
135275	4025	872
135276	4025	874
135277	4026	732
135278	4026	735
135279	4026	737
135280	4026	741
135281	4026	743
135282	4026	746
135283	4026	749
135284	4026	753
135285	4026	758
135286	4026	761
135287	4026	764
135288	4026	769
135289	4026	775
135290	4026	777
135291	4026	782
135292	4026	787
135293	4026	789
135294	4026	792
135295	4026	795
135296	4026	797
135297	4026	802
135298	4026	807
135299	4026	813
135300	4026	819
135301	4026	822
135302	4026	826
135303	4026	829
135304	4026	836
135305	4026	842
135306	4026	845
135307	4026	848
135308	4026	851
135309	4026	854
135310	4026	857
135311	4026	860
135312	4026	871
135313	4026	873
135314	4026	874
135315	4027	732
135316	4027	734
135317	4027	740
135318	4027	743
135319	4027	746
135320	4027	748
135321	4027	754
135322	4027	760
135323	4027	761
135324	4027	765
135325	4027	769
135326	4027	775
135327	4027	777
135328	4027	784
135329	4027	787
135330	4027	789
135331	4027	792
135332	4027	795
135333	4027	798
135334	4027	803
135335	4027	808
135336	4027	814
135337	4027	819
135338	4027	823
135339	4027	828
135340	4027	833
135341	4027	836
135342	4027	842
135343	4027	845
135344	4027	848
135345	4027	851
135346	4027	854
135347	4027	857
135348	4027	860
135349	4027	871
135350	4027	873
135351	4027	874
135352	4028	732
135353	4028	734
135354	4028	740
135355	4028	743
135356	4028	746
135357	4028	749
135358	4028	753
135359	4028	759
135360	4028	761
135361	4028	764
135362	4028	768
135363	4028	772
135364	4028	777
135365	4028	783
135366	4028	787
135367	4028	789
135368	4028	792
135369	4028	794
135370	4028	808
135371	4028	811
135372	4028	818
135373	4028	822
135374	4028	828
135375	4028	835
135376	4028	841
135377	4028	843
135378	4028	847
135379	4028	849
135380	4028	853
135381	4028	856
135382	4028	860
135383	4028	871
135384	4028	872
135385	4028	874
135386	4029	733
135387	4029	735
135388	4029	737
135389	4029	740
135390	4029	744
135391	4029	745
135392	4029	748
135393	4029	752
135394	4029	760
135395	4029	761
135396	4029	764
135397	4029	768
135398	4029	774
135399	4029	777
135400	4029	782
135401	4029	787
135402	4029	789
135403	4029	793
135404	4029	794
135405	4029	806
135406	4029	815
135407	4029	819
135408	4029	822
135409	4029	825
135410	4029	833
135411	4029	835
135412	4029	840
135413	4029	845
135414	4029	846
135415	4029	851
135416	4029	852
135417	4029	859
135418	4029	861
135419	4029	871
135420	4029	872
135421	4029	874
135422	4030	732
135423	4030	734
135424	4030	740
135425	4030	743
135426	4030	746
135427	4030	749
135428	4030	759
135429	4030	761
135430	4030	764
135431	4030	768
135432	4030	776
135433	4030	777
135434	4030	783
135435	4030	787
135436	4030	789
135437	4030	792
135438	4030	794
135439	4030	808
135440	4030	816
135441	4030	819
135442	4030	822
135443	4030	826
135444	4030	832
135445	4030	835
135446	4030	842
135447	4030	845
135448	4030	847
135449	4030	851
135450	4030	853
135451	4030	857
135452	4030	860
135453	4030	871
135454	4030	872
135455	4030	874
135456	4031	732
135457	4031	734
135458	4031	740
135459	4031	743
135460	4031	747
135461	4031	748
135462	4031	753
135463	4031	758
135464	4031	761
135465	4031	764
135466	4031	768
135467	4031	772
135468	4031	777
135469	4031	783
135470	4031	787
135471	4031	789
135472	4031	792
135473	4031	795
135474	4031	797
135475	4031	802
135476	4031	809
135477	4031	811
135478	4031	819
135479	4031	823
135480	4031	827
135481	4031	831
135482	4031	835
135483	4031	842
135484	4031	845
135485	4031	848
135486	4031	851
135487	4031	854
135488	4031	857
135489	4031	860
135490	4031	871
135491	4031	872
135492	4031	874
135493	4032	732
135494	4032	734
135495	4032	740
135496	4032	743
135497	4032	745
135498	4032	749
135499	4032	753
135500	4032	760
135501	4032	761
135502	4032	764
135503	4032	768
135504	4032	775
135505	4032	780
135506	4032	787
135507	4032	789
135508	4032	792
135509	4032	794
135510	4032	806
135511	4032	815
135512	4032	819
135513	4032	822
135514	4032	828
135515	4032	831
135516	4032	835
135517	4032	841
135518	4032	845
135519	4032	846
135520	4032	851
135521	4032	852
135522	4032	859
135523	4032	860
135524	4032	871
135525	4032	873
135526	4032	874
135527	4033	733
135528	4033	735
135529	4033	737
135530	4033	741
135531	4033	744
135532	4033	746
135533	4033	749
135534	4033	753
135535	4033	758
135536	4033	761
135537	4033	764
135538	4033	768
135539	4033	774
135540	4033	777
135541	4033	787
135542	4033	789
135543	4033	792
135544	4033	795
135545	4033	800
135546	4033	805
135547	4033	808
135548	4033	814
135549	4033	819
135550	4033	822
135551	4033	826
135552	4033	831
135553	4033	836
135554	4033	842
135555	4033	845
135556	4033	848
135557	4033	851
135558	4033	854
135559	4033	857
135560	4033	860
135561	4033	871
135562	4033	872
135563	4033	874
135564	4034	734
135565	4034	740
135566	4034	742
135567	4034	746
135568	4034	748
135569	4034	753
135570	4034	761
135571	4034	764
135572	4034	768
135573	4034	772
135574	4034	777
135575	4034	787
135576	4034	789
135577	4034	794
135578	4034	807
135579	4034	811
135580	4034	818
135581	4034	823
135582	4034	828
135583	4034	871
135584	4034	872
135585	4034	874
135586	4035	734
135587	4035	740
135588	4035	742
135589	4035	746
135590	4035	748
135591	4035	753
135592	4035	761
135593	4035	764
135594	4035	768
135595	4035	772
135596	4035	777
135597	4035	787
135598	4035	789
135599	4035	795
135600	4035	797
135601	4035	802
135602	4035	808
135603	4035	811
135604	4035	818
135605	4035	822
135606	4035	828
135607	4035	871
135608	4035	872
135609	4035	874
135610	4036	733
135611	4036	735
135612	4036	738
135613	4036	741
135614	4036	742
135615	4036	745
135616	4036	748
135617	4036	754
135618	4036	761
135619	4036	764
135620	4036	768
135621	4036	776
135622	4036	781
135623	4036	787
135624	4036	789
135625	4036	794
135626	4036	808
135627	4036	815
135628	4036	819
135629	4036	822
135630	4036	828
135631	4036	871
135632	4036	872
135633	4036	874
135634	4037	733
135635	4037	734
135636	4037	740
135637	4037	743
135638	4037	745
135639	4037	748
135640	4037	752
135641	4037	761
135642	4037	764
135643	4037	768
135644	4037	772
135645	4037	777
135646	4037	787
135647	4037	789
135648	4037	795
135649	4037	797
135650	4037	802
135651	4037	808
135652	4037	811
135653	4037	819
135654	4037	822
135655	4037	826
135656	4037	871
135657	4037	872
135658	4037	874
135659	4038	733
135660	4038	735
135661	4038	737
135662	4038	741
135663	4038	744
135664	4038	745
135665	4038	748
135666	4038	752
135667	4038	761
135668	4038	764
135669	4038	768
135670	4038	775
135671	4038	777
135672	4038	787
135673	4038	789
135674	4038	794
135675	4038	807
135676	4038	814
135677	4038	819
135678	4038	822
135679	4038	825
135680	4038	871
135681	4038	872
135682	4038	874
135683	4039	734
135684	4039	740
135685	4039	744
135686	4039	745
135687	4039	748
135688	4039	753
135689	4039	761
135690	4039	764
135691	4039	768
135692	4039	776
135693	4039	781
135694	4039	787
135695	4039	789
135696	4039	795
135697	4039	797
135698	4039	802
135699	4039	806
135700	4039	815
135701	4039	819
135702	4039	822
135703	4039	828
135704	4039	871
135705	4039	872
135706	4039	874
135707	4040	734
135708	4040	740
135709	4040	743
135710	4040	746
135711	4040	748
135712	4040	753
135713	4040	761
135714	4040	764
135715	4040	768
135716	4040	772
135717	4040	777
135718	4040	787
135719	4040	789
135720	4040	794
135721	4040	808
135722	4040	811
135723	4040	819
135724	4040	822
135725	4040	828
135726	4040	871
135727	4040	872
135728	4040	874
135729	4041	734
135730	4041	740
135731	4041	743
135732	4041	746
135733	4041	748
135734	4041	752
135735	4041	761
135736	4041	764
135737	4041	768
135738	4041	772
135739	4041	777
135740	4041	787
135741	4041	789
135742	4041	794
135743	4041	808
135744	4041	811
135745	4041	819
135746	4041	823
135747	4041	828
135748	4041	871
135749	4041	872
135750	4041	874
135751	4042	731
135752	4042	734
135753	4042	740
135754	4042	744
135755	4042	746
135756	4042	748
135757	4042	753
135758	4042	761
135759	4042	764
135760	4042	768
135761	4042	772
135762	4042	777
135763	4042	787
135764	4042	789
135765	4042	795
135766	4042	800
135767	4042	804
135768	4042	808
135769	4042	811
135770	4042	819
135771	4042	823
135772	4042	828
135773	4042	871
135774	4042	872
135775	4042	874
135776	4043	732
135777	4043	734
135778	4043	740
135779	4043	744
135780	4043	745
135781	4043	748
135782	4043	753
135783	4043	761
135784	4043	764
135785	4043	768
135786	4043	772
135787	4043	777
135788	4043	787
135789	4043	789
135790	4043	794
135791	4043	806
135792	4043	811
135793	4043	819
135794	4043	822
135795	4043	828
135796	4043	871
135797	4043	872
135798	4043	874
135799	4044	734
135800	4044	740
135801	4044	744
135802	4044	746
135803	4044	749
135804	4044	753
135805	4044	761
135806	4044	764
135807	4044	768
135808	4044	775
135809	4044	777
135810	4044	787
135811	4044	789
135812	4044	795
135813	4044	800
135814	4044	804
135815	4044	807
135816	4044	814
135817	4044	819
135818	4044	823
135819	4044	827
135820	4044	871
135821	4044	872
135822	4044	874
135823	4045	734
135824	4045	740
135825	4045	743
135826	4045	746
135827	4045	749
135828	4045	753
135829	4045	761
135830	4045	764
135831	4045	768
135832	4045	772
135833	4045	777
135834	4045	787
135835	4045	789
135836	4045	795
135837	4045	797
135838	4045	802
135839	4045	808
135840	4045	811
135841	4045	871
135842	4045	872
135843	4045	874
135844	4046	734
135845	4046	740
135846	4046	743
135847	4046	746
135848	4046	748
135849	4046	752
135850	4046	761
135851	4046	764
135852	4046	768
135853	4046	772
135854	4046	777
135855	4046	787
135856	4046	789
135857	4046	794
135858	4046	807
135859	4046	811
135860	4046	818
135861	4046	822
135862	4046	826
135863	4046	871
135864	4046	872
135865	4046	874
135866	4047	735
135867	4047	737
135868	4047	741
135869	4047	743
135870	4047	747
135871	4047	749
135872	4047	753
135873	4047	761
135874	4047	765
135875	4047	770
135876	4047	775
135877	4047	777
135878	4047	787
135879	4047	789
135880	4047	794
135881	4047	808
135882	4047	813
135883	4047	819
135884	4047	822
135885	4047	827
135886	4047	871
135887	4047	872
135888	4047	874
135889	4048	734
135890	4048	740
135891	4048	744
135892	4048	746
135893	4048	748
135894	4048	753
135895	4048	761
135896	4048	764
135897	4048	768
135898	4048	772
135899	4048	777
135900	4048	787
135901	4048	789
135902	4048	794
135903	4048	806
135904	4048	811
135905	4048	819
135906	4048	822
135907	4048	827
135908	4048	871
135909	4048	872
135910	4048	874
135911	4049	732
135912	4049	735
135913	4049	741
135914	4049	743
135915	4049	746
135916	4049	749
135917	4049	753
135918	4049	759
135919	4049	761
135920	4049	764
135921	4049	768
135922	4049	772
135923	4049	777
135924	4049	783
135925	4049	787
135926	4049	789
135927	4049	792
135928	4049	794
135929	4049	807
135930	4049	811
135931	4049	819
135932	4049	822
135933	4049	827
135934	4049	832
135935	4049	835
135936	4049	841
135937	4049	845
135938	4049	847
135939	4049	851
135940	4049	853
135941	4049	857
135942	4049	860
135943	4049	871
135944	4049	873
135945	4049	874
135946	4050	732
135947	4050	734
135948	4050	740
135949	4050	742
135950	4050	745
135951	4050	750
135952	4050	754
135953	4050	756
135954	4050	761
135955	4050	764
135956	4050	768
135957	4050	772
135958	4050	777
135959	4050	787
135960	4050	789
135961	4050	794
135962	4050	808
135963	4050	811
135964	4050	819
135965	4050	822
135966	4050	828
135967	4050	829
135968	4050	868
135969	4050	871
135970	4050	872
135971	4050	874
135972	4051	732
135973	4051	734
135974	4051	740
135975	4051	743
135976	4051	747
135977	4051	749
135978	4051	753
135979	4051	758
135980	4051	761
135981	4051	764
135982	4051	768
135983	4051	772
135984	4051	777
135985	4051	784
135986	4051	787
135987	4051	789
135988	4051	792
135989	4051	794
135990	4051	808
135991	4051	811
135992	4051	818
135993	4051	822
135994	4051	828
135995	4051	832
135996	4051	835
135997	4051	841
135998	4051	843
135999	4051	848
136000	4051	849
136001	4051	854
136002	4051	856
136003	4051	860
136004	4051	871
136005	4051	872
136006	4051	874
136007	4052	732
136008	4052	734
136009	4052	740
136010	4052	744
136011	4052	746
136012	4052	748
136013	4052	753
136014	4052	759
136015	4052	761
136016	4052	764
136017	4052	768
136018	4052	775
136019	4052	777
136020	4052	784
136021	4052	787
136022	4052	789
136023	4052	793
136024	4052	794
136025	4052	807
136026	4052	816
136027	4052	819
136028	4052	822
136029	4052	828
136030	4052	832
136031	4052	835
136032	4052	842
136033	4052	845
136034	4052	847
136035	4052	851
136036	4052	853
136037	4052	857
136038	4052	860
136039	4052	871
136040	4052	874
136041	4053	732
136042	4053	734
136043	4053	740
136044	4053	742
136045	4053	746
136046	4053	748
136047	4053	753
136048	4053	759
136049	4053	761
136050	4053	764
136051	4053	768
136052	4053	772
136053	4053	777
136054	4053	784
136055	4053	787
136056	4053	789
136057	4053	791
136058	4053	794
136059	4053	808
136060	4053	811
136061	4053	817
136062	4053	821
136063	4053	828
136064	4053	833
136065	4053	835
136066	4053	841
136067	4053	843
136068	4053	847
136069	4053	849
136070	4053	853
136071	4053	856
136072	4053	860
136073	4053	871
136074	4053	872
136075	4053	874
136076	4054	732
136077	4054	734
136078	4054	740
136079	4054	742
136080	4054	746
136081	4054	749
136082	4054	753
136083	4054	758
136084	4054	761
136085	4054	764
136086	4054	768
136087	4054	772
136088	4054	777
136089	4054	783
136090	4054	787
136091	4054	789
136092	4054	792
136093	4054	794
136094	4054	809
136095	4054	811
136096	4054	818
136097	4054	823
136098	4054	827
136099	4054	831
136100	4054	835
136101	4054	841
136102	4054	844
136103	4054	848
136104	4054	850
136105	4054	854
136106	4054	856
136107	4054	860
136108	4054	871
136109	4054	874
136110	4055	732
136111	4055	734
136112	4055	740
136113	4055	744
136114	4055	747
136115	4055	749
136116	4055	754
136117	4055	759
136118	4055	761
136119	4055	764
136120	4055	768
136121	4055	772
136122	4055	777
136123	4055	784
136124	4055	787
136125	4055	789
136126	4055	793
136127	4055	794
136128	4055	808
136129	4055	811
136130	4055	819
136131	4055	822
136132	4055	827
136133	4055	832
136134	4055	835
136135	4055	842
136136	4055	845
136137	4055	847
136138	4055	851
136139	4055	853
136140	4055	857
136141	4055	860
136142	4055	871
136143	4055	872
136144	4055	874
136145	4056	732
136146	4056	734
136147	4056	740
136148	4056	743
136149	4056	745
136150	4056	748
136151	4056	752
136152	4056	759
136153	4056	761
136154	4056	764
136155	4056	768
136156	4056	775
136157	4056	781
136158	4056	782
136159	4056	787
136160	4056	789
136161	4056	793
136162	4056	794
136163	4056	806
136164	4056	815
136165	4056	819
136166	4056	822
136167	4056	825
136168	4056	831
136169	4056	835
136170	4056	841
136171	4056	845
136172	4056	846
136173	4056	851
136174	4056	852
136175	4056	859
136176	4056	860
136177	4056	871
136178	4056	874
136179	4057	732
136180	4057	734
136181	4057	740
136182	4057	744
136183	4057	746
136184	4057	749
136185	4057	754
136186	4057	758
136187	4057	761
136188	4057	764
136189	4057	768
136190	4057	772
136191	4057	777
136192	4057	784
136193	4057	787
136194	4057	789
136195	4057	792
136196	4057	795
136197	4057	797
136198	4057	801
136199	4057	806
136200	4057	811
136201	4057	819
136202	4057	822
136203	4057	828
136204	4057	831
136205	4057	835
136206	4057	842
136207	4057	845
136208	4057	848
136209	4057	851
136210	4057	854
136211	4057	857
136212	4057	860
136213	4057	871
136214	4057	872
136215	4057	874
136216	4058	732
136217	4058	734
136218	4058	740
136219	4058	742
136220	4058	746
136221	4058	749
136222	4058	753
136223	4058	761
136224	4058	764
136225	4058	768
136226	4058	772
136227	4058	777
136228	4058	787
136229	4058	789
136230	4058	794
136231	4058	808
136232	4058	811
136233	4058	818
136234	4058	822
136235	4058	828
136236	4058	835
136237	4058	841
136238	4058	844
136239	4058	847
136240	4058	850
136241	4058	853
136242	4058	856
136243	4058	860
136244	4058	871
136245	4058	874
136246	4059	732
136247	4059	734
136248	4059	740
136249	4059	744
136250	4059	746
136251	4059	749
136252	4059	754
136253	4059	758
136254	4059	761
136255	4059	764
136256	4059	768
136257	4059	772
136258	4059	777
136259	4059	784
136260	4059	787
136261	4059	789
136262	4059	792
136263	4059	794
136264	4059	806
136265	4059	811
136266	4059	819
136267	4059	823
136268	4059	828
136269	4059	830
136270	4059	835
136271	4059	871
136272	4059	874
136273	4060	732
136274	4060	734
136275	4060	740
136276	4060	744
136277	4060	746
136278	4060	749
136279	4060	753
136280	4060	759
136281	4060	761
136282	4060	764
136283	4060	768
136284	4060	772
136285	4060	777
136286	4060	783
136287	4060	787
136288	4060	789
136289	4060	792
136290	4060	794
136291	4060	806
136292	4060	811
136293	4060	818
136294	4060	822
136295	4060	827
136296	4060	833
136297	4060	835
136298	4060	841
136299	4060	845
136300	4060	848
136301	4060	851
136302	4060	854
136303	4060	857
136304	4060	860
136305	4060	871
136306	4060	872
136307	4060	874
\.


--
-- Data for Name: describe_protocol; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.describe_protocol (id, name, specie_id, url_ref) FROM stdin;
7	TP16/3	53	http://mater.cc
\.


--
-- Data for Name: describe_state; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.describe_state (id, numeric_id, description, trait_id) FROM stdin;
731	3	light	191
732	5	medium	191
733	7	dark	191
734	1	absent	192
735	9	present	192
736	1	on tips only	193
737	2	on margin only	193
738	3	in blotches only	193
739	4	even	193
740	1	absent	194
741	9	present	194
742	3	short	195
743	5	medium	195
744	7	long	195
745	3	narrow	196
746	5	medium	196
747	7	broad	196
748	1	erect	197
749	3	semi-erect	197
750	5	horizontal	197
751	7	recurved	197
752	1	erect	198
753	3	semi-erect	198
754	5	horizontal	198
755	7	recurved	198
756	1	very early	199
757	3	early	199
758	5	medium	199
759	7	late	199
760	9	very late	199
761	1	absent	200
762	2	partially male sterile	200
763	3	male sterile	200
764	1	absent or very weak	201
765	3	weak	201
766	5	medium	201
767	7	strong	201
768	1	absent or very weak	202
769	3	weak	202
770	5	medium	202
771	7	strong	202
772	1	absent or very weak	203
773	3	weak	203
774	5	medium	203
775	7	strong	203
776	9	very strong	203
777	1	white	204
778	2	light green	204
779	3	yellow	204
780	4	light purple	204
781	5	purple	204
782	1	very short	205
783	3	short	205
784	5	medium	205
785	7	long	205
786	9	very long	205
787	1	absent	206
788	9	present	206
789	1	absent	207
790	9	present	207
791	3	short	208
792	5	medium	208
793	7	long	208
794	1	absent	209
795	9	present	209
796	1	tip only	210
797	2	1/4 upper only	210
798	3	upper half only	210
799	4	3/4 of total length	210
800	5	whole length	210
801	1	very short	211
802	3	short	211
803	5	medium	211
804	7	long	211
805	9	very long	211
806	1	absent or very weak	212
807	3	weak	212
808	5	medium	212
809	7	strong	212
810	9	very strong	212
811	1	white	213
812	2	yellowish	213
813	3	brown	213
814	4	red	213
815	5	purple	213
816	6	black	213
817	1	upright	214
818	2	semi-upright	214
819	3	slightly drooping	214
820	4	strongly drooping	214
821	1	erect	215
822	3	semi-erect	215
823	5	spreading	215
824	1	enclosed	216
825	3	partly exserted	216
826	5	just exserted	216
827	7	moderately-well exserted	216
828	9	well exserted	216
829	1	very early	217
830	3	early	217
831	5	intermediate	217
832	7	late	217
833	9	very late	217
834	1	light gold	218
835	2	gold	218
836	3	brown	218
837	4	reddish to light purple	218
838	5	purple	218
839	6	black	218
840	3	low	219
841	5	medium	219
842	7	high	219
843	3	short	220
844	5	medium	220
845	7	long	220
846	3	narrow	221
847	5	medium	221
848	7	broad	221
849	3	short	222
850	5	medium	222
851	7	long	222
852	3	narrow	223
853	5	medium	223
854	7	broad	223
855	1	round	224
856	2	semi-round	224
857	3	half spindle-shaped	224
858	4	spindle-shaped	224
859	5	long spindle-shaped	224
860	1	white	225
861	2	light brown	225
862	3	variegated brown	225
863	4	dark brown	225
864	5	light red	225
865	6	red	225
866	7	variegated purple	225
867	8	purple	225
868	9	dark purple / black	225
869	1	glutinous	226
870	2	intermediate	226
871	3	non-glutinous	226
872	1	low	227
873	2	high	227
874	1	absent or very weak	228
875	2	weak	228
876	3	strong	228
\.


--
-- Data for Name: describe_trait; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.describe_trait (id, numeric_id, description, protocol_id) FROM stdin;
191	1	Leaf: Intensity of green colour	7
192	2	Leaf: anthocyanin coloration	7
193	3	Leaf: distribution of anthocyanin coloration	7
194	4	Leaf: anthocyanin coloration of auricles	7
195	5	Leaf blade: length	7
196	6	Leaf blade: width	7
197	7	Flag leaf: attitude of blade (early observation)	7
198	8	Flag leaf: attitude of blade (late observation)	7
199	9	Time of heading (50% of plants with heads) 	7
200	10	Male sterility	7
201	11	Lemma: anthocyanin coloration of keel (early observation)	7
202	12	Lemma: anthocyanin coloration of area below apex (early observation)	7
203	13	Lemma: anthocyanin coloration of apex (early observation)	7
204	14	Spikelet: colour of stigma	7
205	15	Stem: length (excluding panicle)	7
206	16	Stem: anthocyanin coloration of nodes	7
207	17	Stem: anthocyanin coloration of internodes	7
208	18	Panicle: length of main axis	7
209	19	Panicle: awns	7
210	20	Panicle: distribution of awns	7
211	21	Panicle: length of longest awns	7
212	22	Spikelet: pubescence of lemma 	7
213	23	Spikelet: colour of tip of lemma 	7
214	24	Panicle: attitude in relation to stem	7
215	25	Panicle: attitude of branches	7
216	26	Panicle: exsertion	7
217	27	Time of maturity	7
218	28	Lemma: colour	7
219	29	Grain: weight of 1000 fully developed grain	7
220	30	Grain: length	7
221	31	Grain: width	7
222	32	Decorticated grain: length	7
223	33	Decorticated grain: width	7
224	34	Decorticated grain: shape (in lateral view) 	7
225	35	Decorticated grain: colour	7
226	36	Endosperm: type	7
227	37	Endosperm: content of amylose	7
228	38	Decorticated grain: aroma	7
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2022-02-15 20:53:31.095892+00	2	Location object (2)	3		18	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	register	plantspecies
8	register	plantvariety
9	describe	description
10	describe	protocol
11	describe	trait
12	describe	state
13	describe	expression
14	parameters	varietalparameter
15	parameters	measure
17	parameters	parameter
18	spaces	location
19	spaces	garden
20	spaces	area
21	calculator	crop
22	collect	seedsample
23	collect	germinability
24	collect	sampleweight
16	parameters	speciesparameter
25	calculator	cropparameter
26	collect	storage
27	collect	storageposition
28	register	plantvarietyname
29	calculator	managementtype
30	calculator	management
31	collect	cart
32	collect	cartitem
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2022-02-13 08:51:08.650034+00
2	auth	0001_initial	2022-02-13 08:51:08.781034+00
3	admin	0001_initial	2022-02-13 08:51:08.830289+00
4	admin	0002_logentry_remove_auto_add	2022-02-13 08:51:08.852212+00
5	admin	0003_logentry_add_action_flag_choices	2022-02-13 08:51:08.871703+00
6	contenttypes	0002_remove_content_type_name	2022-02-13 08:51:08.898061+00
7	auth	0002_alter_permission_name_max_length	2022-02-13 08:51:08.91057+00
8	auth	0003_alter_user_email_max_length	2022-02-13 08:51:08.923961+00
9	auth	0004_alter_user_username_opts	2022-02-13 08:51:08.936864+00
10	auth	0005_alter_user_last_login_null	2022-02-13 08:51:08.949833+00
11	auth	0006_require_contenttypes_0002	2022-02-13 08:51:08.953312+00
12	auth	0007_alter_validators_add_error_messages	2022-02-13 08:51:08.96567+00
13	auth	0008_alter_user_username_max_length	2022-02-13 08:51:08.983339+00
14	auth	0009_alter_user_last_name_max_length	2022-02-13 08:51:08.99612+00
15	auth	0010_alter_group_name_max_length	2022-02-13 08:51:09.012904+00
16	auth	0011_update_proxy_permissions	2022-02-13 08:51:09.025615+00
17	auth	0012_alter_user_first_name_max_length	2022-02-13 08:51:09.038587+00
18	register	0001_initial	2022-02-13 08:51:09.074502+00
19	register	0002_auto_20201207_2033	2022-02-13 08:51:09.085537+00
20	describe	0001_initial	2022-02-13 08:51:09.200537+00
21	describe	0002_auto_20201207_2043	2022-02-13 08:51:09.24728+00
22	describe	0003_measure	2022-02-13 08:51:09.28259+00
23	describe	0004_auto_20201207_2102	2022-02-13 08:51:09.301654+00
24	describe	0005_auto_20201213_1014	2022-02-13 08:51:09.311616+00
25	describe	0006_protocol_specie	2022-02-13 08:51:09.325826+00
26	describe	0007_auto_20201213_1019	2022-02-13 08:51:09.339533+00
27	describe	0008_auto_20201213_2007	2022-02-13 08:51:09.389802+00
28	describe	0009_auto_20210106_1258	2022-02-13 08:51:09.412507+00
29	describe	0010_auto_20220211_2218	2022-02-13 08:51:09.423997+00
30	parameters	0001_initial	2022-02-13 08:51:09.491406+00
31	parameters	0002_auto_20201214_2044	2022-02-13 08:51:09.566646+00
32	parameters	0003_auto_20201214_2048	2022-02-13 08:51:09.578092+00
33	parameters	0004_auto_20201214_2050	2022-02-13 08:51:09.603034+00
34	parameters	0005_auto_20201214_2053	2022-02-13 08:51:09.704584+00
35	parameters	0006_auto_20201214_2102	2022-02-13 08:51:09.917279+00
36	parameters	0007_auto_20201226_1323	2022-02-13 08:51:09.966181+00
37	parameters	0008_auto_20210106_1258	2022-02-13 08:51:09.97992+00
38	register	0003_auto_20201220_1437	2022-02-13 08:51:09.994381+00
39	register	0004_auto_20201226_1323	2022-02-13 08:51:10.011898+00
40	sessions	0001_initial	2022-02-13 08:51:10.035616+00
41	spaces	0001_initial	2022-02-13 08:51:10.074629+00
42	calculator	0001_initial	2022-02-28 20:46:56.356005+00
43	collect	0001_initial	2022-03-01 10:27:30.548741+00
44	collect	0002_auto_20220301_1051	2022-03-01 10:51:37.161021+00
45	parameters	0009_rename_cropparameter_speciesparameter	2022-03-03 15:01:29.245728+00
46	calculator	0002_cropparameter	2022-03-03 16:33:03.946734+00
47	spaces	0002_auto_20220303_2116	2022-03-03 21:34:15.723862+00
48	collect	0003_auto_20220304_1102	2022-03-04 11:02:31.729649+00
49	parameters	0010_alter_parameter_code	2022-03-05 21:59:07.281405+00
50	register	0005_alter_plantvariety_options	2022-03-05 21:59:07.305805+00
51	spaces	0003_alter_area_options	2022-03-05 21:59:07.318958+00
52	collect	0004_alter_germinability_performed_at	2022-03-09 09:19:14.38651+00
53	collect	0005_auto_20220309_0934	2022-03-09 09:34:48.498063+00
54	collect	0006_remove_sampleweight_updated_at	2022-03-09 09:35:58.529364+00
55	collect	0007_alter_sampleweight_created_at	2022-03-09 09:37:08.002705+00
56	collect	0008_auto_20220309_1044	2022-03-09 10:44:44.866355+00
57	collect	0009_auto_20220309_2153	2022-03-09 21:53:16.336282+00
58	collect	0010_alter_storage_name	2022-03-09 22:27:49.327239+00
59	calculator	0003_alter_crop_notes	2022-03-20 20:36:10.118942+00
60	calculator	0004_alter_cropparameter_url_ref	2022-03-20 21:16:21.254917+00
61	parameters	0011_auto_20220320_2116	2022-03-20 21:16:21.281415+00
62	register	0006_auto_20220323_0923	2022-03-23 09:23:35.250917+00
63	register	0007_auto_20220323_1022	2022-03-23 10:22:46.854637+00
64	calculator	0005_management_managementtype	2022-03-24 20:10:00.508593+00
65	register	0008_alter_plantvarietyname_change_date	2022-03-24 20:10:00.521169+00
66	calculator	0006_auto_20220324_2017	2022-03-24 20:21:53.116084+00
67	calculator	0007_auto_20220328_1209	2022-03-28 12:09:48.52912+00
68	collect	0011_alter_seedsample_growing_season	2022-03-28 12:09:48.542669+00
69	collect	0012_alter_seedsample_id	2022-03-29 11:23:20.942228+00
70	collect	0013_alter_seedsample_id	2022-03-29 11:24:16.097933+00
71	collect	0014_seedsample_sample_id	2022-03-29 11:32:46.492939+00
72	collect	0015_alter_seedsample_position	2022-03-29 11:56:09.24014+00
73	collect	0016_alter_seedsample_sample_id	2022-03-29 11:57:05.71717+00
74	collect	0017_alter_sampleweight_value	2022-03-29 12:53:39.66962+00
75	collect	0018_auto_20220329_1253	2022-03-29 12:53:39.693962+00
76	collect	0019_auto_20220408_1211	2022-04-08 12:12:00.22818+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
ntycw5uk1nm0ive8p3jvwpjzzqo1oa9z	.eJxVjE0OwiAYRO_C2pACJbQu3XsG8v0hVQNJaVeNd7dNutDlzHszm4qwLjmuTeY4sboqoy6_HQK9pByAn1AeVVMtyzyhPhR90qbvleV9O92_gwwt7-vAI7BlCh0bB5TIm5ES2z0Ig0Px1AMNmKwQoCOThhQYQ0--E4NJfb4vFToo:1nK4mx:Oh7FkW-wGgQLCpzROIHkOYGIhx7-Co5JrjOT8lKvzTE	2022-03-01 20:51:07.044689+00
ig8vz5lo8zf4fup4vh806rgfsczuphvf	.eJxVjE0OwiAYRO_C2pACJbQu3XsG8v0hVQNJaVeNd7dNutDlzHszm4qwLjmuTeY4sboqoy6_HQK9pByAn1AeVVMtyzyhPhR90qbvleV9O92_gwwt7-vAI7BlCh0bB5TIm5ES2z0Ig0Px1AMNmKwQoCOThhQYQ0--E4NJfb4vFToo:1ncqyv:muHE1h4bJ9O3XFAq3BNDo8tTvgvK_HSoB3BTcSnsD4A	2022-04-22 15:57:05.589878+00
7zp5xh8s74r5oma0j6wy82jyi3b8ijc5	.eJxVjE0OwiAYRO_C2pACJbQu3XsG8v0hVQNJaVeNd7dNutDlzHszm4qwLjmuTeY4sboqoy6_HQK9pByAn1AeVVMtyzyhPhR90qbvleV9O92_gwwt7-vAI7BlCh0bB5TIm5ES2z0Ig0Px1AMNmKwQoCOThhQYQ0--E4NJfb4vFToo:1nd4nn:5qFs_e3GDqszT8jJwPOq3hhpKYgJSREYjiXvW3UrFuI	2022-04-23 06:42:31.71721+00
cpk3tnls6rwly3ve4o3drtgjmkfd046m	.eJxVjE0OwiAYRO_C2pACJbQu3XsG8v0hVQNJaVeNd7dNutDlzHszm4qwLjmuTeY4sboqoy6_HQK9pByAn1AeVVMtyzyhPhR90qbvleV9O92_gwwt7-vAI7BlCh0bB5TIm5ES2z0Ig0Px1AMNmKwQoCOThhQYQ0--E4NJfb4vFToo:1ndoG1:uy-OVy7B_MWmkzPMV3tKVkcmz37MXwaUt8LBVk_fE8A	2022-04-25 07:14:41.886303+00
\.


--
-- Data for Name: parameters_measure; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.parameters_measure (id, georeference_lat, georeference_lon, measure_unit, value, trait_id, variety_id) FROM stdin;
\.


--
-- Data for Name: parameters_parameter; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.parameters_parameter (id, code, name, description, measure_unit) FROM stdin;
1	Tbase	Base temperature	The minimum temperature required for plant growth	°C
2	Topt	Optimal temperature for growth	Optimal temperature for growth	°C
3	Thigh	Maximum temperature for growth	Maximum temperature for growth	°C
4	distw	Distance within rows	The distance between plants within a row	meters
5	distb	Distance between rows	The distance between rows	meters
7	GDDmat	Growing degree days to maturity	GDDmat	°C/day
6	yield	Yield	Total yield per square meter	kg/m2
\.


--
-- Data for Name: parameters_speciesparameter; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.parameters_speciesparameter (id, url_ref, value, specie_id, parameter_id, created_at, updated_at) FROM stdin;
1	https://mater.cc	10	34	1	2022-02-13 09:43:00.669936+00	2022-02-13 09:43:00.669964+00
2	https://mater.cc	4	1	1	2022-02-13 09:45:54.835322+00	2022-02-13 09:45:54.835347+00
3	https://mater.cc	5	2	1	2022-02-13 09:45:54.846007+00	2022-02-13 09:45:54.846024+00
4	https://mater.cc	4	3	1	2022-02-13 09:45:54.849705+00	2022-02-13 09:45:54.84973+00
5	https://mater.cc	4	4	1	2022-02-13 09:45:54.856568+00	2022-02-13 09:45:54.856617+00
6	https://mater.cc	7	5	1	2022-02-13 09:45:54.862472+00	2022-02-13 09:45:54.862493+00
7	https://mater.cc	5	6	1	2022-02-13 09:45:54.867701+00	2022-02-13 09:45:54.867756+00
8	https://mater.cc	5	7	1	2022-02-13 09:45:54.874177+00	2022-02-13 09:45:54.874204+00
9	https://mater.cc	5	7	1	2022-02-13 09:45:54.879754+00	2022-02-13 09:45:54.879808+00
10	https://mater.cc	7	17	1	2022-02-13 09:45:54.88291+00	2022-02-13 09:45:54.882927+00
11	https://mater.cc	7	18	1	2022-02-13 09:45:54.886714+00	2022-02-13 09:45:54.886775+00
12	https://mater.cc	6	19	1	2022-02-13 09:45:54.892376+00	2022-02-13 09:45:54.892404+00
13	https://mater.cc	6	19	1	2022-02-13 09:45:54.897505+00	2022-02-13 09:45:54.897526+00
14	https://mater.cc	7	21	1	2022-02-13 09:45:54.900593+00	2022-02-13 09:45:54.900614+00
15	https://mater.cc	15	22	1	2022-02-13 09:45:54.906801+00	2022-02-13 09:45:54.906821+00
16	https://mater.cc	15	23	1	2022-02-13 09:45:54.911316+00	2022-02-13 09:45:54.91134+00
17	https://mater.cc	10	24	1	2022-02-13 09:45:54.914693+00	2022-02-13 09:45:54.914714+00
18	https://mater.cc	15	25	1	2022-02-13 09:45:54.917699+00	2022-02-13 09:45:54.917714+00
19	https://mater.cc	15	26	1	2022-02-13 09:45:54.920129+00	2022-02-13 09:45:54.920142+00
20	https://mater.cc	10	27	1	2022-02-13 09:45:54.922482+00	2022-02-13 09:45:54.922497+00
21	https://mater.cc	10	28	1	2022-02-13 09:45:54.926278+00	2022-02-13 09:45:54.926294+00
22	https://mater.cc	6	29	1	2022-02-13 09:45:54.929787+00	2022-02-13 09:45:54.929821+00
23	https://mater.cc	5	30	1	2022-02-13 09:45:54.9331+00	2022-02-13 09:45:54.933116+00
24	https://mater.cc	7	31	1	2022-02-13 09:45:54.935799+00	2022-02-13 09:45:54.935814+00
25	https://mater.cc	20	32	1	2022-02-13 09:45:54.938518+00	2022-02-13 09:45:54.938533+00
26	https://mater.cc	15	33	1	2022-02-13 09:45:54.941235+00	2022-02-13 09:45:54.94125+00
27	https://mater.cc	5	34	1	2022-02-13 09:45:54.943942+00	2022-02-13 09:45:54.943956+00
28	https://mater.cc	10	35	1	2022-02-13 09:45:54.946571+00	2022-02-13 09:45:54.946588+00
29	https://mater.cc	5	36	1	2022-02-13 09:45:54.949268+00	2022-02-13 09:45:54.949283+00
30	https://mater.cc	15	37	1	2022-02-13 09:45:54.95187+00	2022-02-13 09:45:54.951882+00
31	https://mater.cc	5	38	1	2022-02-13 09:45:54.954915+00	2022-02-13 09:45:54.954929+00
32	https://mater.cc	4	39	1	2022-02-13 09:45:54.957385+00	2022-02-13 09:45:54.957397+00
33	https://mater.cc	5	40	1	2022-02-13 09:45:54.960299+00	2022-02-13 09:45:54.960313+00
34	https://mater.cc	5	41	1	2022-02-13 09:45:54.96284+00	2022-02-13 09:45:54.962851+00
35	https://mater.cc	5	42	1	2022-02-13 09:45:54.965206+00	2022-02-13 09:45:54.965218+00
36	https://mater.cc	12	43	1	2022-02-13 09:45:54.967691+00	2022-02-13 09:45:54.967702+00
37	https://mater.cc	15	44	1	2022-02-13 09:45:54.970197+00	2022-02-13 09:45:54.970208+00
38	https://mater.cc	6	45	1	2022-02-13 09:45:54.973267+00	2022-02-13 09:45:54.973281+00
39	https://mater.cc	5	46	1	2022-02-13 09:45:54.976404+00	2022-02-13 09:45:54.976418+00
40	https://mater.cc	10	47	1	2022-02-13 09:45:54.979509+00	2022-02-13 09:45:54.979523+00
41	https://mater.cc	1	48	1	2022-02-13 09:45:54.982659+00	2022-02-13 09:45:54.982674+00
42	https://mater.cc	1	49	1	2022-02-13 09:45:54.985771+00	2022-02-13 09:45:54.985786+00
43	https://mater.cc	18	50	1	2022-02-13 09:45:54.988385+00	2022-02-13 09:45:54.988397+00
45	https://mater.cc	18	1	2	2022-02-13 09:47:45.703812+00	2022-02-13 09:47:45.70384+00
46	https://mater.cc	20	2	2	2022-02-13 09:47:45.715747+00	2022-02-13 09:47:45.71577+00
47	https://mater.cc	18	3	2	2022-02-13 09:47:45.720633+00	2022-02-13 09:47:45.720665+00
48	https://mater.cc	18	4	2	2022-02-13 09:47:45.726278+00	2022-02-13 09:47:45.726313+00
49	https://mater.cc	18	5	2	2022-02-13 09:47:45.730995+00	2022-02-13 09:47:45.731038+00
50	https://mater.cc	18	6	2	2022-02-13 09:47:45.735506+00	2022-02-13 09:47:45.735533+00
51	https://mater.cc	18	7	2	2022-02-13 09:47:45.741019+00	2022-02-13 09:47:45.741046+00
52	https://mater.cc	18	7	2	2022-02-13 09:47:45.746464+00	2022-02-13 09:47:45.746521+00
53	https://mater.cc	19	17	2	2022-02-13 09:47:45.752693+00	2022-02-13 09:47:45.752736+00
54	https://mater.cc	19	18	2	2022-02-13 09:47:45.758211+00	2022-02-13 09:47:45.758232+00
55	https://mater.cc	19	19	2	2022-02-13 09:47:45.76453+00	2022-02-13 09:47:45.76459+00
56	https://mater.cc	19	19	2	2022-02-13 09:47:45.771085+00	2022-02-13 09:47:45.771113+00
57	https://mater.cc	19	21	2	2022-02-13 09:47:45.776148+00	2022-02-13 09:47:45.776174+00
58	https://mater.cc	23	22	2	2022-02-13 09:47:45.782302+00	2022-02-13 09:47:45.782353+00
59	https://mater.cc	23	23	2	2022-02-13 09:47:45.78639+00	2022-02-13 09:47:45.786411+00
60	https://mater.cc	30	24	2	2022-02-13 09:47:45.790244+00	2022-02-13 09:47:45.790263+00
61	https://mater.cc	25	25	2	2022-02-13 09:47:45.79331+00	2022-02-13 09:47:45.793336+00
62	https://mater.cc	25	26	2	2022-02-13 09:47:45.798948+00	2022-02-13 09:47:45.798974+00
63	https://mater.cc	28	27	2	2022-02-13 09:47:45.804057+00	2022-02-13 09:47:45.804109+00
64	https://mater.cc	28	28	2	2022-02-13 09:47:45.807752+00	2022-02-13 09:47:45.807778+00
65	https://mater.cc	18	29	2	2022-02-13 09:47:45.812476+00	2022-02-13 09:47:45.812503+00
66	https://mater.cc	18	30	2	2022-02-13 09:47:45.816792+00	2022-02-13 09:47:45.816811+00
67	https://mater.cc	20	31	2	2022-02-13 09:47:45.822213+00	2022-02-13 09:47:45.822246+00
68	https://mater.cc	30	32	2	2022-02-13 09:47:45.826992+00	2022-02-13 09:47:45.827037+00
69	https://mater.cc	25	33	2	2022-02-13 09:47:45.831647+00	2022-02-13 09:47:45.831667+00
70	https://mater.cc	17	34	2	2022-02-13 09:47:45.835646+00	2022-02-13 09:47:45.835668+00
71	https://mater.cc	25	35	2	2022-02-13 09:47:45.838847+00	2022-02-13 09:47:45.838865+00
72	https://mater.cc	18	36	2	2022-02-13 09:47:45.841681+00	2022-02-13 09:47:45.841697+00
73	https://mater.cc	25	37	2	2022-02-13 09:47:45.844349+00	2022-02-13 09:47:45.844364+00
74	https://mater.cc	15	38	2	2022-02-13 09:47:45.850072+00	2022-02-13 09:47:45.85012+00
75	https://mater.cc	18	39	2	2022-02-13 09:47:45.855517+00	2022-02-13 09:47:45.855554+00
76	https://mater.cc	15	40	2	2022-02-13 09:47:45.859266+00	2022-02-13 09:47:45.859302+00
77	https://mater.cc	18	41	2	2022-02-13 09:47:45.865152+00	2022-02-13 09:47:45.865199+00
78	https://mater.cc	18	42	2	2022-02-13 09:47:45.869958+00	2022-02-13 09:47:45.869988+00
79	https://mater.cc	21	43	2	2022-02-13 09:47:45.873732+00	2022-02-13 09:47:45.873755+00
80	https://mater.cc	23	44	2	2022-02-13 09:47:45.877348+00	2022-02-13 09:47:45.877371+00
81	https://mater.cc	16	45	2	2022-02-13 09:47:45.880964+00	2022-02-13 09:47:45.880987+00
82	https://mater.cc	15	46	2	2022-02-13 09:47:45.884629+00	2022-02-13 09:47:45.884652+00
83	https://mater.cc	30	47	2	2022-02-13 09:47:45.890444+00	2022-02-13 09:47:45.89049+00
84	https://mater.cc	26	48	2	2022-02-13 09:47:45.897732+00	2022-02-13 09:47:45.897784+00
85	https://mater.cc	26	49	2	2022-02-13 09:47:45.905146+00	2022-02-13 09:47:45.905199+00
86	https://mater.cc	30	50	2	2022-02-13 09:47:45.911867+00	2022-02-13 09:47:45.911901+00
88	https://mater.cc	30	1	3	2022-02-13 09:48:46.395463+00	2022-02-13 09:48:46.395492+00
89	https://mater.cc	35	2	3	2022-02-13 09:48:46.406088+00	2022-02-13 09:48:46.406117+00
90	https://mater.cc	30	3	3	2022-02-13 09:48:46.41115+00	2022-02-13 09:48:46.411189+00
91	https://mater.cc	30	4	3	2022-02-13 09:48:46.416497+00	2022-02-13 09:48:46.416516+00
92	https://mater.cc	26	5	3	2022-02-13 09:48:46.420523+00	2022-02-13 09:48:46.420545+00
93	https://mater.cc	35	6	3	2022-02-13 09:48:46.424887+00	2022-02-13 09:48:46.424907+00
94	https://mater.cc	32	7	3	2022-02-13 09:48:46.429055+00	2022-02-13 09:48:46.429109+00
95	https://mater.cc	35	7	3	2022-02-13 09:48:46.434263+00	2022-02-13 09:48:46.434284+00
96	https://mater.cc	27	17	3	2022-02-13 09:48:46.438593+00	2022-02-13 09:48:46.438649+00
97	https://mater.cc	27	18	3	2022-02-13 09:48:46.442083+00	2022-02-13 09:48:46.442102+00
98	https://mater.cc	27	19	3	2022-02-13 09:48:46.446126+00	2022-02-13 09:48:46.446151+00
99	https://mater.cc	27	19	3	2022-02-13 09:48:46.450401+00	2022-02-13 09:48:46.450421+00
100	https://mater.cc	27	21	3	2022-02-13 09:48:46.4548+00	2022-02-13 09:48:46.454819+00
101	https://mater.cc	35	22	3	2022-02-13 09:48:46.457519+00	2022-02-13 09:48:46.457535+00
102	https://mater.cc	35	23	3	2022-02-13 09:48:46.463098+00	2022-02-13 09:48:46.463151+00
103	https://mater.cc	37	24	3	2022-02-13 09:48:46.468581+00	2022-02-13 09:48:46.468608+00
104	https://mater.cc	38	25	3	2022-02-13 09:48:46.472939+00	2022-02-13 09:48:46.472966+00
105	https://mater.cc	35	26	3	2022-02-13 09:48:46.476669+00	2022-02-13 09:48:46.476691+00
106	https://mater.cc	38	27	3	2022-02-13 09:48:46.479865+00	2022-02-13 09:48:46.479883+00
107	https://mater.cc	38	28	3	2022-02-13 09:48:46.48272+00	2022-02-13 09:48:46.482736+00
108	https://mater.cc	28	29	3	2022-02-13 09:48:46.485636+00	2022-02-13 09:48:46.485652+00
109	https://mater.cc	38	30	3	2022-02-13 09:48:46.488448+00	2022-02-13 09:48:46.488463+00
110	https://mater.cc	31	31	3	2022-02-13 09:48:46.491346+00	2022-02-13 09:48:46.491363+00
111	https://mater.cc	40	32	3	2022-02-13 09:48:46.494266+00	2022-02-13 09:48:46.494282+00
112	https://mater.cc	37	33	3	2022-02-13 09:48:46.497156+00	2022-02-13 09:48:46.497172+00
113	https://mater.cc	27	34	3	2022-02-13 09:48:46.502885+00	2022-02-13 09:48:46.502932+00
114	https://mater.cc	30	35	3	2022-02-13 09:48:46.510326+00	2022-02-13 09:48:46.510377+00
115	https://mater.cc	27	36	3	2022-02-13 09:48:46.517686+00	2022-02-13 09:48:46.517737+00
116	https://mater.cc	35	37	3	2022-02-13 09:48:46.525052+00	2022-02-13 09:48:46.525103+00
117	https://mater.cc	29	38	3	2022-02-13 09:48:46.5325+00	2022-02-13 09:48:46.532551+00
118	https://mater.cc	30	39	3	2022-02-13 09:48:46.540101+00	2022-02-13 09:48:46.540152+00
119	https://mater.cc	25	40	3	2022-02-13 09:48:46.547655+00	2022-02-13 09:48:46.547706+00
120	https://mater.cc	35	41	3	2022-02-13 09:48:46.555142+00	2022-02-13 09:48:46.555195+00
121	https://mater.cc	30	42	3	2022-02-13 09:48:46.562765+00	2022-02-13 09:48:46.562819+00
122	https://mater.cc	35	43	3	2022-02-13 09:48:46.570269+00	2022-02-13 09:48:46.570318+00
123	https://mater.cc	35	44	3	2022-02-13 09:48:46.57771+00	2022-02-13 09:48:46.577762+00
124	https://mater.cc	27	45	3	2022-02-13 09:48:46.585067+00	2022-02-13 09:48:46.585118+00
125	https://mater.cc	25	46	3	2022-02-13 09:48:46.59251+00	2022-02-13 09:48:46.592562+00
126	https://mater.cc	39	47	3	2022-02-13 09:48:46.600014+00	2022-02-13 09:48:46.600067+00
127	https://mater.cc	33	48	3	2022-02-13 09:48:46.606716+00	2022-02-13 09:48:46.606763+00
128	https://mater.cc	33	49	3	2022-02-13 09:48:46.61417+00	2022-02-13 09:48:46.614223+00
129	https://mater.cc	38	50	3	2022-02-13 09:48:46.622614+00	2022-02-13 09:48:46.622698+00
261	http://mater.cc	0.2	1	5	2022-02-13 20:31:28.718709+00	2022-02-13 20:31:28.718784+00
262	http://mater.cc	0.25	2	5	2022-02-13 20:31:28.736484+00	2022-02-13 20:31:28.736553+00
263	http://mater.cc	0.35	3	5	2022-02-13 20:31:28.746085+00	2022-02-13 20:31:28.746145+00
264	http://mater.cc	0.4	4	5	2022-02-13 20:31:28.75649+00	2022-02-13 20:31:28.756572+00
265	http://mater.cc	0.35	5	5	2022-02-13 20:31:28.765707+00	2022-02-13 20:31:28.765784+00
266	http://mater.cc	0.3	6	5	2022-02-13 20:31:28.77594+00	2022-02-13 20:31:28.77603+00
267	http://mater.cc	0.4	7	5	2022-02-13 20:31:28.786266+00	2022-02-13 20:31:28.786344+00
268	http://mater.cc	0.3	7	5	2022-02-13 20:31:28.795771+00	2022-02-13 20:31:28.795833+00
269	http://mater.cc	0.6	17	5	2022-02-13 20:31:28.807433+00	2022-02-13 20:31:28.807499+00
270	http://mater.cc	0.5	18	5	2022-02-13 20:31:28.818333+00	2022-02-13 20:31:28.818397+00
271	http://mater.cc	0.5	19	5	2022-02-13 20:31:28.827266+00	2022-02-13 20:31:28.827316+00
272	http://mater.cc	0.5	19	5	2022-02-13 20:31:28.835668+00	2022-02-13 20:31:28.835718+00
273	http://mater.cc	0.6	21	5	2022-02-13 20:31:28.8446+00	2022-02-13 20:31:28.844665+00
274	http://mater.cc	0.7	22	5	2022-02-13 20:31:28.854327+00	2022-02-13 20:31:28.854387+00
275	http://mater.cc	0.7	23	5	2022-02-13 20:31:28.86409+00	2022-02-13 20:31:28.864143+00
276	http://mater.cc	1	24	5	2022-02-13 20:31:28.872938+00	2022-02-13 20:31:28.87299+00
277	http://mater.cc	1	25	5	2022-02-13 20:31:28.880721+00	2022-02-13 20:31:28.880779+00
278	http://mater.cc	1	26	5	2022-02-13 20:31:28.889695+00	2022-02-13 20:31:28.889758+00
279	http://mater.cc	1	27	5	2022-02-13 20:31:28.89869+00	2022-02-13 20:31:28.898777+00
280	http://mater.cc	1	28	5	2022-02-13 20:31:28.908067+00	2022-02-13 20:31:28.908124+00
281	http://mater.cc	0.25	29	5	2022-02-13 20:31:28.916688+00	2022-02-13 20:31:28.916741+00
282	http://mater.cc	0.25	30	5	2022-02-13 20:31:28.924844+00	2022-02-13 20:31:28.924906+00
283	http://mater.cc	0.4	31	5	2022-02-13 20:31:28.932897+00	2022-02-13 20:31:28.932947+00
284	http://mater.cc	0.15	32	5	2022-02-13 20:31:28.940923+00	2022-02-13 20:31:28.940987+00
285	http://mater.cc	1	33	5	2022-02-13 20:31:28.949135+00	2022-02-13 20:31:28.949196+00
286	http://mater.cc	0.3	34	5	2022-02-13 20:31:28.957174+00	2022-02-13 20:31:28.957227+00
287	http://mater.cc	0.25	35	5	2022-02-13 20:31:28.965707+00	2022-02-13 20:31:28.965761+00
288	http://mater.cc	0.3	36	5	2022-02-13 20:31:28.974643+00	2022-02-13 20:31:28.974692+00
289	http://mater.cc	0.25	37	5	2022-02-13 20:31:28.981898+00	2022-02-13 20:31:28.981948+00
290	http://mater.cc	0.4	38	5	2022-02-13 20:31:28.989109+00	2022-02-13 20:31:28.989162+00
291	http://mater.cc	0.7	39	5	2022-02-13 20:31:28.996969+00	2022-02-13 20:31:28.997028+00
292	http://mater.cc	0.15	40	5	2022-02-13 20:31:29.00518+00	2022-02-13 20:31:29.005236+00
293	http://mater.cc	0.3	41	5	2022-02-13 20:31:29.013874+00	2022-02-13 20:31:29.013936+00
294	http://mater.cc	0.2	42	5	2022-02-13 20:31:29.022448+00	2022-02-13 20:31:29.02251+00
295	http://mater.cc	1	43	5	2022-02-13 20:31:29.031131+00	2022-02-13 20:31:29.031195+00
296	http://mater.cc	0.9	44	5	2022-02-13 20:31:29.039588+00	2022-02-13 20:31:29.03965+00
297	http://mater.cc	0.6	45	5	2022-02-13 20:31:29.047385+00	2022-02-13 20:31:29.047443+00
298	http://mater.cc	0.2	46	5	2022-02-13 20:31:29.056328+00	2022-02-13 20:31:29.056387+00
299	http://mater.cc	0.5	47	5	2022-02-13 20:31:29.066213+00	2022-02-13 20:31:29.066294+00
300	http://mater.cc	0.1	48	5	2022-02-13 20:31:29.074466+00	2022-02-13 20:31:29.074518+00
301	http://mater.cc	0.1	49	5	2022-02-13 20:31:29.082117+00	2022-02-13 20:31:29.082176+00
302	http://mater.cc	0.4	50	5	2022-02-13 20:31:29.090166+00	2022-02-13 20:31:29.090242+00
304	http://mater.cc	0.2	1	4	2022-02-13 20:31:29.110044+00	2022-02-13 20:31:29.110139+00
305	http://mater.cc	0.2	2	4	2022-02-13 20:31:29.117994+00	2022-02-13 20:31:29.11805+00
306	http://mater.cc	0.15	3	4	2022-02-13 20:31:29.126465+00	2022-02-13 20:31:29.126525+00
307	http://mater.cc	0.3	4	4	2022-02-13 20:31:29.134437+00	2022-02-13 20:31:29.134495+00
308	http://mater.cc	0.3	5	4	2022-02-13 20:31:29.142339+00	2022-02-13 20:31:29.142387+00
309	http://mater.cc	0.15	6	4	2022-02-13 20:31:29.149973+00	2022-02-13 20:31:29.150026+00
310	http://mater.cc	0.25	7	4	2022-02-13 20:31:29.157011+00	2022-02-13 20:31:29.157061+00
311	http://mater.cc	0.1	7	4	2022-02-13 20:31:29.164221+00	2022-02-13 20:31:29.164269+00
312	http://mater.cc	0.6	17	4	2022-02-13 20:31:29.172289+00	2022-02-13 20:31:29.172361+00
313	http://mater.cc	0.5	18	4	2022-02-13 20:31:29.17996+00	2022-02-13 20:31:29.180013+00
314	http://mater.cc	0.5	19	4	2022-02-13 20:31:29.187632+00	2022-02-13 20:31:29.187684+00
315	http://mater.cc	0.5	19	4	2022-02-13 20:31:29.195554+00	2022-02-13 20:31:29.195605+00
316	http://mater.cc	0.6	21	4	2022-02-13 20:31:29.203158+00	2022-02-13 20:31:29.20321+00
317	http://mater.cc	0.5	22	4	2022-02-13 20:31:29.210926+00	2022-02-13 20:31:29.210977+00
318	http://mater.cc	0.5	23	4	2022-02-13 20:31:29.218534+00	2022-02-13 20:31:29.218586+00
319	http://mater.cc	1	24	4	2022-02-13 20:31:29.225979+00	2022-02-13 20:31:29.226032+00
320	http://mater.cc	1	25	4	2022-02-13 20:31:29.23383+00	2022-02-13 20:31:29.233883+00
321	http://mater.cc	0.5	26	4	2022-02-13 20:31:29.242456+00	2022-02-13 20:31:29.242514+00
322	http://mater.cc	1	27	4	2022-02-13 20:31:29.249267+00	2022-02-13 20:31:29.249313+00
323	http://mater.cc	0.8	28	4	2022-02-13 20:31:29.256643+00	2022-02-13 20:31:29.256695+00
324	http://mater.cc	0.05	29	4	2022-02-13 20:31:29.2641+00	2022-02-13 20:31:29.264149+00
325	http://mater.cc	0.05	30	4	2022-02-13 20:31:29.271111+00	2022-02-13 20:31:29.271167+00
326	http://mater.cc	0.25	31	4	2022-02-13 20:31:29.279082+00	2022-02-13 20:31:29.27916+00
327	http://mater.cc	0.15	32	4	2022-02-13 20:31:29.287896+00	2022-02-13 20:31:29.287959+00
328	http://mater.cc	0.15	33	4	2022-02-13 20:31:29.296343+00	2022-02-13 20:31:29.296403+00
329	http://mater.cc	0.25	34	4	2022-02-13 20:31:29.305288+00	2022-02-13 20:31:29.30535+00
330	http://mater.cc	0.25	35	4	2022-02-13 20:31:29.3136+00	2022-02-13 20:31:29.313661+00
331	http://mater.cc	0.1	36	4	2022-02-13 20:31:29.321323+00	2022-02-13 20:31:29.321381+00
332	http://mater.cc	0.25	37	4	2022-02-13 20:31:29.328916+00	2022-02-13 20:31:29.328973+00
333	http://mater.cc	0.05	38	4	2022-02-13 20:31:29.337853+00	2022-02-13 20:31:29.337915+00
334	http://mater.cc	0.2	39	4	2022-02-13 20:31:29.345403+00	2022-02-13 20:31:29.345452+00
335	http://mater.cc	0.15	40	4	2022-02-13 20:31:29.352054+00	2022-02-13 20:31:29.352102+00
336	http://mater.cc	0.15	41	4	2022-02-13 20:31:29.359475+00	2022-02-13 20:31:29.359528+00
337	http://mater.cc	0.05	42	4	2022-02-13 20:31:29.367402+00	2022-02-13 20:31:29.367454+00
338	http://mater.cc	0.4	43	4	2022-02-13 20:31:29.375051+00	2022-02-13 20:31:29.375102+00
339	http://mater.cc	0.5	44	4	2022-02-13 20:31:29.382631+00	2022-02-13 20:31:29.382683+00
340	http://mater.cc	0.4	45	4	2022-02-13 20:31:29.38955+00	2022-02-13 20:31:29.3896+00
341	http://mater.cc	0.1	46	4	2022-02-13 20:31:29.397122+00	2022-02-13 20:31:29.397174+00
342	http://mater.cc	0.3	47	4	2022-02-13 20:31:29.404862+00	2022-02-13 20:31:29.404917+00
343	http://mater.cc	0.03	48	4	2022-02-13 20:31:29.411663+00	2022-02-13 20:31:29.411714+00
344	http://mater.cc	0.03	49	4	2022-02-13 20:31:29.419156+00	2022-02-13 20:31:29.419208+00
345	http://mater.cc	0.15	50	4	2022-02-13 20:31:29.426813+00	2022-02-13 20:31:29.426868+00
347	http://mater.cc	3	1	6	2022-02-13 20:31:29.444644+00	2022-02-13 20:31:29.444696+00
348	http://mater.cc	3	2	6	2022-02-13 20:31:29.451422+00	2022-02-13 20:31:29.451471+00
349	http://mater.cc	1	3	6	2022-02-13 20:31:29.458144+00	2022-02-13 20:31:29.458195+00
350	http://mater.cc	1.5	4	6	2022-02-13 20:31:29.464788+00	2022-02-13 20:31:29.464836+00
351	http://mater.cc	3	5	6	2022-02-13 20:31:29.471569+00	2022-02-13 20:31:29.471617+00
352	http://mater.cc	3	6	6	2022-02-13 20:31:29.479075+00	2022-02-13 20:31:29.479134+00
353	http://mater.cc	3	7	6	2022-02-13 20:31:29.487205+00	2022-02-13 20:31:29.487259+00
354	http://mater.cc	3	7	6	2022-02-13 20:31:29.495046+00	2022-02-13 20:31:29.4951+00
355	http://mater.cc	2.5	17	6	2022-02-13 20:31:29.501913+00	2022-02-13 20:31:29.501964+00
357	http://mater.cc	2	19	6	2022-02-13 20:31:29.515563+00	2022-02-13 20:31:29.515613+00
358	http://mater.cc	2	19	6	2022-02-13 20:31:29.52246+00	2022-02-13 20:31:29.52251+00
359	http://mater.cc	4.5	21	6	2022-02-13 20:31:29.529457+00	2022-02-13 20:31:29.529507+00
360	http://mater.cc	4.5	22	6	2022-02-13 20:31:29.536236+00	2022-02-13 20:31:29.536308+00
361	http://mater.cc	0.5	23	6	2022-02-13 20:31:29.543334+00	2022-02-13 20:31:29.543384+00
362	http://mater.cc	16	24	6	2022-02-13 20:31:29.550513+00	2022-02-13 20:31:29.550564+00
363	http://mater.cc	2	25	6	2022-02-13 20:31:29.557322+00	2022-02-13 20:31:29.557373+00
364	http://mater.cc	4	26	6	2022-02-13 20:31:29.564153+00	2022-02-13 20:31:29.564202+00
365	http://mater.cc	8	27	6	2022-02-13 20:31:29.571103+00	2022-02-13 20:31:29.571153+00
366	http://mater.cc	5	28	6	2022-02-13 20:31:29.578671+00	2022-02-13 20:31:29.578724+00
367	http://mater.cc	3	29	6	2022-02-13 20:31:29.586263+00	2022-02-13 20:31:29.586316+00
368	http://mater.cc	1	30	6	2022-02-13 20:31:29.59381+00	2022-02-13 20:31:29.593866+00
369	http://mater.cc	3.5	31	6	2022-02-13 20:31:29.600768+00	2022-02-13 20:31:29.600817+00
370	http://mater.cc	0.3	32	6	2022-02-13 20:31:29.608211+00	2022-02-13 20:31:29.608267+00
371	http://mater.cc	10	33	6	2022-02-13 20:31:29.615077+00	2022-02-13 20:31:29.615128+00
372	http://mater.cc	2	34	6	2022-02-13 20:31:29.622071+00	2022-02-13 20:31:29.622121+00
373	http://mater.cc	2	35	6	2022-02-13 20:31:29.629452+00	2022-02-13 20:31:29.629506+00
374	http://mater.cc	2	36	6	2022-02-13 20:31:29.637059+00	2022-02-13 20:31:29.637111+00
375	http://mater.cc	1.5	37	6	2022-02-13 20:31:29.643957+00	2022-02-13 20:31:29.644006+00
376	http://mater.cc	1.5	38	6	2022-02-13 20:31:29.650609+00	2022-02-13 20:31:29.650661+00
377	http://mater.cc	1	39	6	2022-02-13 20:31:29.657401+00	2022-02-13 20:31:29.65745+00
378	http://mater.cc	3	40	6	2022-02-13 20:31:29.664936+00	2022-02-13 20:31:29.664988+00
379	http://mater.cc	1.5	41	6	2022-02-13 20:31:29.671918+00	2022-02-13 20:31:29.671968+00
380	http://mater.cc	1	42	6	2022-02-13 20:31:29.679539+00	2022-02-13 20:31:29.679592+00
381	http://mater.cc	3.5	43	6	2022-02-13 20:31:29.687426+00	2022-02-13 20:31:29.687481+00
382	http://mater.cc	4	44	6	2022-02-13 20:31:29.694717+00	2022-02-13 20:31:29.694769+00
383	http://mater.cc	3	45	6	2022-02-13 20:31:29.701457+00	2022-02-13 20:31:29.701508+00
384	http://mater.cc	2	46	6	2022-02-13 20:31:29.709026+00	2022-02-13 20:31:29.709083+00
385	http://mater.cc	2	47	6	2022-02-13 20:31:29.716805+00	2022-02-13 20:31:29.71686+00
386	http://mater.cc	0.3	48	6	2022-02-13 20:31:29.724451+00	2022-02-13 20:31:29.724502+00
387	http://mater.cc	0.2	49	6	2022-02-13 20:31:29.732384+00	2022-02-13 20:31:29.732439+00
388	http://mater.cc	0.2	50	6	2022-02-13 20:31:29.739499+00	2022-02-13 20:31:29.739552+00
390	http://mattthefarmer.com	10	35	1	2022-02-28 22:57:30.01143+00	2022-02-28 22:57:30.01152+00
356	http://mater.cc	4.5	18	6	2022-02-13 20:31:29.50869+00	2022-03-06 21:50:33.941474+00
391	\N	1700	19	7	2022-04-10 20:15:51.059593+00	2022-04-10 20:15:51.059618+00
392	\N	1215	31	7	2022-04-10 20:22:41.788177+00	2022-04-10 20:22:41.788232+00
393	\N	12	53	1	2022-04-10 20:29:44.016918+00	2022-04-10 20:29:44.016942+00
394	\N	25	53	2	2022-04-10 20:29:52.289788+00	2022-04-10 20:29:52.289845+00
395	\N	38	53	3	2022-04-10 20:30:01.340051+00	2022-04-10 20:30:01.340106+00
\.


--
-- Data for Name: parameters_varietalparameter; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.parameters_varietalparameter (id, url_ref, value, variety_id, parameter_id, created_at, updated_at) FROM stdin;
1	\N	1200	6998	7	2022-04-10 20:23:47.249536+00	2022-04-10 20:23:47.249594+00
\.


--
-- Data for Name: register_plantspecies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.register_plantspecies (id, common_name, latin_name, plant_type) FROM stdin;
1	Leek	Allium ampeloprasum	
2	Onion	Allium cepa	
3	Garlic	Allium sativum	
4	Shallot	Allium cepa	
5	Celery	Apium graveolens	
6	Beetroot	Beta vulgaris	
7	Chard	Beta vulgaris cicla	
17	Cauliflower	Brassica oleracea botrytis	
18	Cabbage	Brassica oleracea capitata	
19	Kale	Brassica oleracea acephala	
21	Savoy cabbage	Brassica oleracea sabauda	
22	Sweet Pepper	Capsicum annuum	
23	Pepper	Capsicum annuum	
24	Watermelon	Citrullus lanatus 	
25	Melon	Cucumis melo	
26	Cucumber	Cucumis sativus	
27	Pumpkin	Cucurbita maxima	
28	Zucchini	Cucurbita pepo	
29	Carrot	Daucus carota	
30	Rocket	Eruca vesicaria	
31	Fennel	Foeniculum vulgare	
32	Soy	Glycine max	
33	Sweet potato	Ipomea batatas	
34	Lattuce	Lactuca sativa	
35	Basil	Ocimum basilicum	
36	Parsley	Petroselinum crispum	
37	Bean	Phaseolus vulgaris	
38	Pea	Pisum sativum	
39	Broad bean	Vicia faba	
40	Daikon	Raphanus sativus	
41	Turnip	Brassica rapa	
42	Radish	Raphanus sativus	
43	Tomato	Solanum lycopersicon	
44	Eggplant	Solanum melongena	
45	Potato	Solanum tuberosum	
46	Spinach	Spinacia oleracea	
47	Corn	Zea mays	
48	Wheat	Triticum	
49	Rye	Secale cereale	
50	Peanut	Arachis hypogaea	
53	Rice	Oryza sativa	4
\.


--
-- Data for Name: register_plantvariety; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.register_plantvariety (id, species_id, created_at, updated_at) FROM stdin;
7661	53	2022-03-30 13:32:52.774242+00	2022-03-30 13:32:52.77431+00
7665	53	2022-04-13 09:28:59.707185+00	2022-04-13 09:28:59.707245+00
7632	53	2022-03-29 11:35:53.118937+00	2022-03-29 11:35:53.11897+00
7633	53	2022-03-29 11:35:53.124567+00	2022-03-29 11:35:53.124587+00
7634	53	2022-03-29 11:35:53.129815+00	2022-03-29 11:35:53.129834+00
7635	53	2022-03-29 11:35:53.134549+00	2022-03-29 11:35:53.134566+00
7636	53	2022-03-29 11:35:53.138129+00	2022-03-29 11:35:53.138143+00
7637	53	2022-03-29 11:35:53.141767+00	2022-03-29 11:35:53.141782+00
7638	53	2022-03-29 11:35:53.14581+00	2022-03-29 11:35:53.145823+00
7639	53	2022-03-29 11:35:53.153949+00	2022-03-29 11:35:53.153966+00
7640	53	2022-03-29 11:35:53.158207+00	2022-03-29 11:35:53.158224+00
7641	53	2022-03-29 11:35:53.161614+00	2022-03-29 11:35:53.161628+00
7642	53	2022-03-29 11:35:53.165101+00	2022-03-29 11:35:53.165113+00
7643	53	2022-03-29 11:35:53.168628+00	2022-03-29 11:35:53.168641+00
7644	53	2022-03-29 11:35:53.172281+00	2022-03-29 11:35:53.172294+00
7645	53	2022-03-29 11:35:53.175548+00	2022-03-29 11:35:53.175561+00
7646	53	2022-03-29 11:35:53.178812+00	2022-03-29 11:35:53.178824+00
7647	53	2022-03-29 11:35:53.182286+00	2022-03-29 11:35:53.182298+00
7648	53	2022-03-29 11:35:53.185659+00	2022-03-29 11:35:53.18567+00
7649	53	2022-03-29 11:35:53.188914+00	2022-03-29 11:35:53.188927+00
7650	53	2022-03-29 11:35:53.192283+00	2022-03-29 11:35:53.192296+00
7651	53	2022-03-29 11:35:53.195591+00	2022-03-29 11:35:53.195602+00
7652	53	2022-03-29 11:35:53.19894+00	2022-03-29 11:35:53.198953+00
7653	53	2022-03-29 11:35:53.202242+00	2022-03-29 11:35:53.202254+00
7654	53	2022-03-29 11:35:53.205475+00	2022-03-29 11:35:53.205487+00
7655	53	2022-03-29 11:35:53.208688+00	2022-03-29 11:35:53.2087+00
7656	53	2022-03-29 11:35:53.212145+00	2022-03-29 11:35:53.212157+00
7657	53	2022-03-29 11:35:53.216593+00	2022-03-29 11:35:53.216611+00
7658	53	2022-03-29 11:35:53.220437+00	2022-03-29 11:35:53.220452+00
7659	53	2022-03-29 11:35:53.224608+00	2022-03-29 11:35:53.224625+00
7660	53	2022-03-29 11:35:53.228454+00	2022-03-29 11:35:53.22847+00
7663	53	2022-03-30 13:35:28.101869+00	2022-03-30 13:35:28.101939+00
7664	53	2022-03-30 13:46:55.192179+00	2022-03-30 13:46:55.192262+00
6719	53	2022-03-28 12:17:29.279248+00	2022-03-28 12:17:29.279281+00
6720	53	2022-03-28 12:17:29.29489+00	2022-03-28 12:17:29.294915+00
6721	53	2022-03-28 12:17:29.300927+00	2022-03-28 12:17:29.300963+00
6722	53	2022-03-28 12:17:29.305745+00	2022-03-28 12:17:29.305767+00
6723	53	2022-03-28 12:17:29.310363+00	2022-03-28 12:17:29.310387+00
6724	53	2022-03-28 12:17:29.314444+00	2022-03-28 12:17:29.31447+00
6725	53	2022-03-28 12:17:29.318589+00	2022-03-28 12:17:29.318611+00
6726	53	2022-03-28 12:17:29.324769+00	2022-03-28 12:17:29.324819+00
6727	53	2022-03-28 12:17:29.33001+00	2022-03-28 12:17:29.330032+00
6728	53	2022-03-28 12:17:29.334289+00	2022-03-28 12:17:29.33431+00
6729	53	2022-03-28 12:17:29.338667+00	2022-03-28 12:17:29.338702+00
6730	53	2022-03-28 12:17:29.342113+00	2022-03-28 12:17:29.342132+00
6731	53	2022-03-28 12:17:29.345575+00	2022-03-28 12:17:29.345594+00
6732	53	2022-03-28 12:17:29.353153+00	2022-03-28 12:17:29.353213+00
6733	53	2022-03-28 12:17:29.359071+00	2022-03-28 12:17:29.359091+00
6734	53	2022-03-28 12:17:29.363681+00	2022-03-28 12:17:29.363709+00
6735	53	2022-03-28 12:17:29.367338+00	2022-03-28 12:17:29.367357+00
6736	53	2022-03-28 12:17:29.371086+00	2022-03-28 12:17:29.371104+00
6737	53	2022-03-28 12:17:29.37443+00	2022-03-28 12:17:29.374447+00
6738	53	2022-03-28 12:17:29.378327+00	2022-03-28 12:17:29.378376+00
6739	53	2022-03-28 12:17:29.383927+00	2022-03-28 12:17:29.383958+00
6740	53	2022-03-28 12:17:29.388747+00	2022-03-28 12:17:29.388783+00
6741	53	2022-03-28 12:17:29.394226+00	2022-03-28 12:17:29.394265+00
6742	53	2022-03-28 12:17:29.399622+00	2022-03-28 12:17:29.39967+00
6743	53	2022-03-28 12:17:29.404956+00	2022-03-28 12:17:29.405008+00
6744	53	2022-03-28 12:17:29.410231+00	2022-03-28 12:17:29.410271+00
6745	53	2022-03-28 12:17:29.414802+00	2022-03-28 12:17:29.414832+00
6746	53	2022-03-28 12:17:29.419342+00	2022-03-28 12:17:29.419388+00
6747	53	2022-03-28 12:17:29.424753+00	2022-03-28 12:17:29.424778+00
6748	53	2022-03-28 12:17:29.42894+00	2022-03-28 12:17:29.428965+00
6749	53	2022-03-28 12:17:29.433315+00	2022-03-28 12:17:29.433333+00
6750	53	2022-03-28 12:17:29.436664+00	2022-03-28 12:17:29.436679+00
6751	53	2022-03-28 12:17:29.439794+00	2022-03-28 12:17:29.439808+00
6752	53	2022-03-28 12:17:29.442849+00	2022-03-28 12:17:29.442861+00
6753	53	2022-03-28 12:17:29.446533+00	2022-03-28 12:17:29.446552+00
6754	53	2022-03-28 12:17:29.450071+00	2022-03-28 12:17:29.450086+00
6755	53	2022-03-28 12:17:29.45316+00	2022-03-28 12:17:29.453173+00
6756	53	2022-03-28 12:17:29.456723+00	2022-03-28 12:17:29.456741+00
6757	53	2022-03-28 12:17:29.460233+00	2022-03-28 12:17:29.460246+00
6758	53	2022-03-28 12:17:29.463192+00	2022-03-28 12:17:29.463205+00
6759	53	2022-03-28 12:17:29.466254+00	2022-03-28 12:17:29.466266+00
6760	53	2022-03-28 12:17:29.469487+00	2022-03-28 12:17:29.4695+00
6761	53	2022-03-28 12:17:29.474059+00	2022-03-28 12:17:29.474114+00
6762	53	2022-03-28 12:17:29.481205+00	2022-03-28 12:17:29.481258+00
6763	53	2022-03-28 12:17:29.487969+00	2022-03-28 12:17:29.488019+00
6764	53	2022-03-28 12:17:29.495246+00	2022-03-28 12:17:29.495299+00
6765	53	2022-03-28 12:17:29.503144+00	2022-03-28 12:17:29.503198+00
6766	53	2022-03-28 12:17:29.510263+00	2022-03-28 12:17:29.510316+00
6767	53	2022-03-28 12:17:29.51802+00	2022-03-28 12:17:29.518075+00
6768	53	2022-03-28 12:17:29.526071+00	2022-03-28 12:17:29.526126+00
6769	53	2022-03-28 12:17:29.534161+00	2022-03-28 12:17:29.534215+00
6770	53	2022-03-28 12:17:29.542136+00	2022-03-28 12:17:29.542191+00
6771	53	2022-03-28 12:17:29.550069+00	2022-03-28 12:17:29.550123+00
6772	53	2022-03-28 12:17:29.557371+00	2022-03-28 12:17:29.557424+00
6773	53	2022-03-28 12:17:29.565076+00	2022-03-28 12:17:29.565169+00
6774	53	2022-03-28 12:17:29.572989+00	2022-03-28 12:17:29.573043+00
6775	53	2022-03-28 12:17:29.579632+00	2022-03-28 12:17:29.579682+00
6776	53	2022-03-28 12:17:29.590415+00	2022-03-28 12:17:29.590468+00
6777	53	2022-03-28 12:17:29.598372+00	2022-03-28 12:17:29.598426+00
6778	53	2022-03-28 12:17:29.606365+00	2022-03-28 12:17:29.60642+00
6779	53	2022-03-28 12:17:29.612783+00	2022-03-28 12:17:29.61282+00
6780	53	2022-03-28 12:17:29.619008+00	2022-03-28 12:17:29.619044+00
6781	53	2022-03-28 12:17:29.624496+00	2022-03-28 12:17:29.624525+00
6782	53	2022-03-28 12:17:29.629426+00	2022-03-28 12:17:29.629451+00
6783	53	2022-03-28 12:17:29.634299+00	2022-03-28 12:17:29.634323+00
6784	53	2022-03-28 12:17:29.638835+00	2022-03-28 12:17:29.638857+00
6785	53	2022-03-28 12:17:29.642454+00	2022-03-28 12:17:29.642473+00
6786	53	2022-03-28 12:17:29.646802+00	2022-03-28 12:17:29.646824+00
6787	53	2022-03-28 12:17:29.650443+00	2022-03-28 12:17:29.650461+00
6788	53	2022-03-28 12:17:29.654464+00	2022-03-28 12:17:29.654488+00
6789	53	2022-03-28 12:17:29.658871+00	2022-03-28 12:17:29.658894+00
6790	53	2022-03-28 12:17:29.664984+00	2022-03-28 12:17:29.665038+00
6791	53	2022-03-28 12:17:29.672866+00	2022-03-28 12:17:29.67292+00
6792	53	2022-03-28 12:17:29.679344+00	2022-03-28 12:17:29.679392+00
6793	53	2022-03-28 12:17:29.685723+00	2022-03-28 12:17:29.685775+00
6794	53	2022-03-28 12:17:29.692187+00	2022-03-28 12:17:29.692222+00
6795	53	2022-03-28 12:17:29.69671+00	2022-03-28 12:17:29.696733+00
6796	53	2022-03-28 12:17:29.700708+00	2022-03-28 12:17:29.70073+00
6797	53	2022-03-28 12:17:29.705716+00	2022-03-28 12:17:29.705745+00
6798	53	2022-03-28 12:17:29.710623+00	2022-03-28 12:17:29.71065+00
6799	53	2022-03-28 12:17:29.715247+00	2022-03-28 12:17:29.715276+00
6800	53	2022-03-28 12:17:29.720328+00	2022-03-28 12:17:29.720355+00
6801	53	2022-03-28 12:17:29.724288+00	2022-03-28 12:17:29.724312+00
6802	53	2022-03-28 12:17:29.728973+00	2022-03-28 12:17:29.729001+00
6803	53	2022-03-28 12:17:29.733486+00	2022-03-28 12:17:29.733515+00
6804	53	2022-03-28 12:17:29.738366+00	2022-03-28 12:17:29.738393+00
6805	53	2022-03-28 12:17:29.742276+00	2022-03-28 12:17:29.742299+00
6806	53	2022-03-28 12:17:29.746207+00	2022-03-28 12:17:29.746237+00
6807	53	2022-03-28 12:17:29.751517+00	2022-03-28 12:17:29.751546+00
6808	53	2022-03-28 12:17:29.757007+00	2022-03-28 12:17:29.757035+00
6809	53	2022-03-28 12:17:29.761724+00	2022-03-28 12:17:29.761752+00
6810	53	2022-03-28 12:17:29.767041+00	2022-03-28 12:17:29.767069+00
6811	53	2022-03-28 12:17:29.77184+00	2022-03-28 12:17:29.771871+00
6812	53	2022-03-28 12:17:29.777124+00	2022-03-28 12:17:29.777153+00
6813	53	2022-03-28 12:17:29.785369+00	2022-03-28 12:17:29.785397+00
6814	53	2022-03-28 12:17:29.79027+00	2022-03-28 12:17:29.790297+00
6815	53	2022-03-28 12:17:29.795421+00	2022-03-28 12:17:29.795451+00
6816	53	2022-03-28 12:17:29.800463+00	2022-03-28 12:17:29.800492+00
6817	53	2022-03-28 12:17:29.80492+00	2022-03-28 12:17:29.80495+00
6818	53	2022-03-28 12:17:29.809643+00	2022-03-28 12:17:29.809681+00
6819	53	2022-03-28 12:17:29.814483+00	2022-03-28 12:17:29.814526+00
6820	53	2022-03-28 12:17:29.820002+00	2022-03-28 12:17:29.820034+00
6821	53	2022-03-28 12:17:29.824639+00	2022-03-28 12:17:29.824667+00
6822	53	2022-03-28 12:17:29.829547+00	2022-03-28 12:17:29.829577+00
6823	53	2022-03-28 12:17:29.833911+00	2022-03-28 12:17:29.833938+00
6824	53	2022-03-28 12:17:29.837926+00	2022-03-28 12:17:29.837949+00
6825	53	2022-03-28 12:17:29.842377+00	2022-03-28 12:17:29.842407+00
6826	53	2022-03-28 12:17:29.847284+00	2022-03-28 12:17:29.847312+00
6827	53	2022-03-28 12:17:29.851316+00	2022-03-28 12:17:29.851339+00
6828	53	2022-03-28 12:17:29.85541+00	2022-03-28 12:17:29.855435+00
6829	53	2022-03-28 12:17:29.860049+00	2022-03-28 12:17:29.860073+00
6830	53	2022-03-28 12:17:29.864404+00	2022-03-28 12:17:29.864423+00
6831	53	2022-03-28 12:17:29.868334+00	2022-03-28 12:17:29.868354+00
6832	53	2022-03-28 12:17:29.872322+00	2022-03-28 12:17:29.872342+00
6833	53	2022-03-28 12:17:29.875954+00	2022-03-28 12:17:29.875977+00
6834	53	2022-03-28 12:17:29.879273+00	2022-03-28 12:17:29.879294+00
6835	53	2022-03-28 12:17:29.882573+00	2022-03-28 12:17:29.882593+00
6836	53	2022-03-28 12:17:29.885764+00	2022-03-28 12:17:29.885785+00
6837	53	2022-03-28 12:17:29.888979+00	2022-03-28 12:17:29.889+00
6838	53	2022-03-28 12:17:29.892218+00	2022-03-28 12:17:29.892238+00
6839	53	2022-03-28 12:17:29.895437+00	2022-03-28 12:17:29.895458+00
6840	53	2022-03-28 12:17:29.898704+00	2022-03-28 12:17:29.898724+00
6841	53	2022-03-28 12:17:29.901892+00	2022-03-28 12:17:29.901909+00
6842	53	2022-03-28 12:17:29.904896+00	2022-03-28 12:17:29.904914+00
6843	53	2022-03-28 12:17:29.90773+00	2022-03-28 12:17:29.907746+00
6844	53	2022-03-28 12:17:29.910696+00	2022-03-28 12:17:29.910712+00
6845	53	2022-03-28 12:17:29.913704+00	2022-03-28 12:17:29.913719+00
6846	53	2022-03-28 12:17:29.916719+00	2022-03-28 12:17:29.916734+00
6847	53	2022-03-28 12:17:29.919734+00	2022-03-28 12:17:29.919748+00
6848	53	2022-03-28 12:17:29.922828+00	2022-03-28 12:17:29.922842+00
6849	53	2022-03-28 12:17:29.925805+00	2022-03-28 12:17:29.925818+00
6850	53	2022-03-28 12:17:29.928771+00	2022-03-28 12:17:29.928783+00
6851	53	2022-03-28 12:17:29.931732+00	2022-03-28 12:17:29.931745+00
6852	53	2022-03-28 12:17:29.934676+00	2022-03-28 12:17:29.93469+00
6853	53	2022-03-28 12:17:29.937606+00	2022-03-28 12:17:29.937618+00
6854	53	2022-03-28 12:17:29.940567+00	2022-03-28 12:17:29.940579+00
6855	53	2022-03-28 12:17:29.943508+00	2022-03-28 12:17:29.94352+00
6856	53	2022-03-28 12:17:29.946432+00	2022-03-28 12:17:29.946443+00
6857	53	2022-03-28 12:17:29.949179+00	2022-03-28 12:17:29.94919+00
6858	53	2022-03-28 12:17:29.951995+00	2022-03-28 12:17:29.952006+00
6859	53	2022-03-28 12:17:29.954779+00	2022-03-28 12:17:29.954791+00
6860	53	2022-03-28 12:17:29.957554+00	2022-03-28 12:17:29.957565+00
6861	53	2022-03-28 12:17:29.96049+00	2022-03-28 12:17:29.960502+00
6862	53	2022-03-28 12:17:29.963547+00	2022-03-28 12:17:29.963559+00
6863	53	2022-03-28 12:17:29.966498+00	2022-03-28 12:17:29.966511+00
6864	53	2022-03-28 12:17:29.969333+00	2022-03-28 12:17:29.969345+00
6865	53	2022-03-28 12:17:29.972189+00	2022-03-28 12:17:29.972201+00
6866	53	2022-03-28 12:17:29.975033+00	2022-03-28 12:17:29.975045+00
6867	53	2022-03-28 12:17:29.977877+00	2022-03-28 12:17:29.977889+00
6868	53	2022-03-28 12:17:29.980708+00	2022-03-28 12:17:29.98072+00
6869	53	2022-03-28 12:17:29.983403+00	2022-03-28 12:17:29.983416+00
6870	53	2022-03-28 12:17:29.988057+00	2022-03-28 12:17:29.988097+00
6871	53	2022-03-28 12:17:29.99196+00	2022-03-28 12:17:29.991978+00
6872	53	2022-03-28 12:17:29.995187+00	2022-03-28 12:17:29.995204+00
6873	53	2022-03-28 12:17:29.998294+00	2022-03-28 12:17:29.998311+00
6874	53	2022-03-28 12:17:30.001648+00	2022-03-28 12:17:30.001664+00
6875	53	2022-03-28 12:17:30.004992+00	2022-03-28 12:17:30.005004+00
6876	53	2022-03-28 12:17:30.008083+00	2022-03-28 12:17:30.008095+00
6877	53	2022-03-28 12:17:30.011575+00	2022-03-28 12:17:30.011592+00
6878	53	2022-03-28 12:17:30.015458+00	2022-03-28 12:17:30.015474+00
6879	53	2022-03-28 12:17:30.018931+00	2022-03-28 12:17:30.018945+00
6880	53	2022-03-28 12:17:30.022965+00	2022-03-28 12:17:30.022981+00
6881	53	2022-03-28 12:17:30.026513+00	2022-03-28 12:17:30.026527+00
6882	53	2022-03-28 12:17:30.030125+00	2022-03-28 12:17:30.030141+00
6883	53	2022-03-28 12:17:30.033686+00	2022-03-28 12:17:30.033702+00
6884	53	2022-03-28 12:17:30.037488+00	2022-03-28 12:17:30.037536+00
6885	53	2022-03-28 12:17:30.043898+00	2022-03-28 12:17:30.043946+00
6886	53	2022-03-28 12:17:30.051715+00	2022-03-28 12:17:30.05177+00
6887	53	2022-03-28 12:17:30.058281+00	2022-03-28 12:17:30.058329+00
6888	53	2022-03-28 12:17:30.064648+00	2022-03-28 12:17:30.064697+00
6889	53	2022-03-28 12:17:30.07227+00	2022-03-28 12:17:30.072324+00
6890	53	2022-03-28 12:17:30.078802+00	2022-03-28 12:17:30.078849+00
6891	53	2022-03-28 12:17:30.08499+00	2022-03-28 12:17:30.08504+00
6892	53	2022-03-28 12:17:30.091239+00	2022-03-28 12:17:30.091288+00
6893	53	2022-03-28 12:17:30.098099+00	2022-03-28 12:17:30.098155+00
6894	53	2022-03-28 12:17:30.104055+00	2022-03-28 12:17:30.104087+00
6895	53	2022-03-28 12:17:30.109545+00	2022-03-28 12:17:30.109575+00
6896	53	2022-03-28 12:17:30.114922+00	2022-03-28 12:17:30.114952+00
6897	53	2022-03-28 12:17:30.120298+00	2022-03-28 12:17:30.120327+00
6898	53	2022-03-28 12:17:30.125616+00	2022-03-28 12:17:30.125646+00
6899	53	2022-03-28 12:17:30.130458+00	2022-03-28 12:17:30.130485+00
6900	53	2022-03-28 12:17:30.134984+00	2022-03-28 12:17:30.135013+00
6901	53	2022-03-28 12:17:30.140356+00	2022-03-28 12:17:30.140385+00
6902	53	2022-03-28 12:17:30.145558+00	2022-03-28 12:17:30.145588+00
6903	53	2022-03-28 12:17:30.149916+00	2022-03-28 12:17:30.149941+00
6904	53	2022-03-28 12:17:30.153862+00	2022-03-28 12:17:30.153886+00
6905	53	2022-03-28 12:17:30.158272+00	2022-03-28 12:17:30.158301+00
6906	53	2022-03-28 12:17:30.162474+00	2022-03-28 12:17:30.162498+00
6907	53	2022-03-28 12:17:30.166908+00	2022-03-28 12:17:30.166937+00
6908	53	2022-03-28 12:17:30.171206+00	2022-03-28 12:17:30.17123+00
6909	53	2022-03-28 12:17:30.17554+00	2022-03-28 12:17:30.175569+00
6910	53	2022-03-28 12:17:30.181303+00	2022-03-28 12:17:30.18135+00
6911	53	2022-03-28 12:17:30.188053+00	2022-03-28 12:17:30.188108+00
6912	53	2022-03-28 12:17:30.194618+00	2022-03-28 12:17:30.194665+00
6913	53	2022-03-28 12:17:30.200973+00	2022-03-28 12:17:30.201021+00
6914	53	2022-03-28 12:17:30.207229+00	2022-03-28 12:17:30.207276+00
6915	53	2022-03-28 12:17:30.214439+00	2022-03-28 12:17:30.214491+00
6916	53	2022-03-28 12:17:30.221637+00	2022-03-28 12:17:30.22169+00
6917	53	2022-03-28 12:17:30.227895+00	2022-03-28 12:17:30.227943+00
6918	53	2022-03-28 12:17:30.234198+00	2022-03-28 12:17:30.234245+00
6919	53	2022-03-28 12:17:30.241351+00	2022-03-28 12:17:30.241402+00
6920	53	2022-03-28 12:17:30.24816+00	2022-03-28 12:17:30.248216+00
6921	53	2022-03-28 12:17:30.254671+00	2022-03-28 12:17:30.254719+00
6922	53	2022-03-28 12:17:30.262117+00	2022-03-28 12:17:30.262199+00
6923	53	2022-03-28 12:17:30.269059+00	2022-03-28 12:17:30.269116+00
6924	53	2022-03-28 12:17:30.276207+00	2022-03-28 12:17:30.276263+00
6925	53	2022-03-28 12:17:30.283148+00	2022-03-28 12:17:30.2832+00
6926	53	2022-03-28 12:17:30.29025+00	2022-03-28 12:17:30.290305+00
6927	53	2022-03-28 12:17:30.297321+00	2022-03-28 12:17:30.297371+00
6928	53	2022-03-28 12:17:30.304569+00	2022-03-28 12:17:30.304621+00
6929	53	2022-03-28 12:17:30.311861+00	2022-03-28 12:17:30.311916+00
6930	53	2022-03-28 12:17:30.318821+00	2022-03-28 12:17:30.318874+00
6931	53	2022-03-28 12:17:30.325914+00	2022-03-28 12:17:30.325968+00
6932	53	2022-03-28 12:17:30.331428+00	2022-03-28 12:17:30.331463+00
6933	53	2022-03-28 12:17:30.335606+00	2022-03-28 12:17:30.335633+00
6934	53	2022-03-28 12:17:30.339521+00	2022-03-28 12:17:30.339543+00
6935	53	2022-03-28 12:17:30.342973+00	2022-03-28 12:17:30.342991+00
6936	53	2022-03-28 12:17:30.347492+00	2022-03-28 12:17:30.347518+00
6937	53	2022-03-28 12:17:30.351124+00	2022-03-28 12:17:30.35116+00
6938	53	2022-03-28 12:17:30.354466+00	2022-03-28 12:17:30.354484+00
6939	53	2022-03-28 12:17:30.357376+00	2022-03-28 12:17:30.357391+00
6940	53	2022-03-28 12:17:30.363853+00	2022-03-28 12:17:30.363869+00
6941	53	2022-03-28 12:17:30.36688+00	2022-03-28 12:17:30.366898+00
6942	53	2022-03-28 12:17:30.369898+00	2022-03-28 12:17:30.369913+00
6943	53	2022-03-28 12:17:30.372733+00	2022-03-28 12:17:30.372746+00
6944	53	2022-03-28 12:17:30.375723+00	2022-03-28 12:17:30.375739+00
6945	53	2022-03-28 12:17:30.378563+00	2022-03-28 12:17:30.378576+00
6946	53	2022-03-28 12:17:30.381345+00	2022-03-28 12:17:30.381358+00
6947	53	2022-03-28 12:17:30.384294+00	2022-03-28 12:17:30.384309+00
6948	53	2022-03-28 12:17:30.387194+00	2022-03-28 12:17:30.387207+00
6949	53	2022-03-28 12:17:30.390104+00	2022-03-28 12:17:30.390118+00
6950	53	2022-03-28 12:17:30.392882+00	2022-03-28 12:17:30.392896+00
6951	53	2022-03-28 12:17:30.395658+00	2022-03-28 12:17:30.39567+00
6952	53	2022-03-28 12:17:30.398409+00	2022-03-28 12:17:30.398423+00
6953	53	2022-03-28 12:17:30.401167+00	2022-03-28 12:17:30.40118+00
6954	53	2022-03-28 12:17:30.404203+00	2022-03-28 12:17:30.404222+00
6955	53	2022-03-28 12:17:30.40703+00	2022-03-28 12:17:30.407043+00
6956	53	2022-03-28 12:17:30.409659+00	2022-03-28 12:17:30.409671+00
6957	53	2022-03-28 12:17:30.412264+00	2022-03-28 12:17:30.412276+00
6958	53	2022-03-28 12:17:30.414862+00	2022-03-28 12:17:30.414873+00
6959	53	2022-03-28 12:17:30.417647+00	2022-03-28 12:17:30.41766+00
6960	53	2022-03-28 12:17:30.420426+00	2022-03-28 12:17:30.420439+00
6961	53	2022-03-28 12:17:30.423244+00	2022-03-28 12:17:30.423256+00
6962	53	2022-03-28 12:17:30.426085+00	2022-03-28 12:17:30.426097+00
6963	53	2022-03-28 12:17:30.428887+00	2022-03-28 12:17:30.428902+00
6964	53	2022-03-28 12:17:30.431651+00	2022-03-28 12:17:30.431665+00
6965	53	2022-03-28 12:17:30.434517+00	2022-03-28 12:17:30.434532+00
6966	53	2022-03-28 12:17:30.437433+00	2022-03-28 12:17:30.437447+00
6967	53	2022-03-28 12:17:30.440165+00	2022-03-28 12:17:30.44018+00
6968	53	2022-03-28 12:17:30.44284+00	2022-03-28 12:17:30.442852+00
6969	53	2022-03-28 12:17:30.445508+00	2022-03-28 12:17:30.445521+00
6970	53	2022-03-28 12:17:30.44835+00	2022-03-28 12:17:30.448363+00
6971	53	2022-03-28 12:17:30.45124+00	2022-03-28 12:17:30.451253+00
6972	53	2022-03-28 12:17:30.454088+00	2022-03-28 12:17:30.454099+00
6973	53	2022-03-28 12:17:30.456909+00	2022-03-28 12:17:30.456921+00
6974	53	2022-03-28 12:17:30.459611+00	2022-03-28 12:17:30.459623+00
6975	53	2022-03-28 12:17:30.462311+00	2022-03-28 12:17:30.462322+00
6976	53	2022-03-28 12:17:30.46513+00	2022-03-28 12:17:30.465141+00
6977	53	2022-03-28 12:17:30.46796+00	2022-03-28 12:17:30.467972+00
6978	53	2022-03-28 12:17:30.470701+00	2022-03-28 12:17:30.470717+00
6979	53	2022-03-28 12:17:30.473539+00	2022-03-28 12:17:30.473554+00
6980	53	2022-03-28 12:17:30.476776+00	2022-03-28 12:17:30.476791+00
6981	53	2022-03-28 12:17:30.479447+00	2022-03-28 12:17:30.479459+00
6982	53	2022-03-28 12:17:30.482056+00	2022-03-28 12:17:30.482068+00
6983	53	2022-03-28 12:17:30.484938+00	2022-03-28 12:17:30.484955+00
6984	53	2022-03-28 12:17:30.487997+00	2022-03-28 12:17:30.48801+00
6985	53	2022-03-28 12:17:30.490925+00	2022-03-28 12:17:30.490941+00
6986	53	2022-03-28 12:17:30.494573+00	2022-03-28 12:17:30.49459+00
6987	53	2022-03-28 12:17:30.498249+00	2022-03-28 12:17:30.498267+00
6988	53	2022-03-28 12:17:30.501867+00	2022-03-28 12:17:30.501884+00
6989	53	2022-03-28 12:17:30.505078+00	2022-03-28 12:17:30.505095+00
6990	53	2022-03-28 12:17:30.50841+00	2022-03-28 12:17:30.508427+00
6991	53	2022-03-28 12:17:30.512021+00	2022-03-28 12:17:30.512044+00
6992	53	2022-03-28 12:17:30.515349+00	2022-03-28 12:17:30.515366+00
6993	53	2022-03-28 12:17:30.518569+00	2022-03-28 12:17:30.518583+00
6994	53	2022-03-28 12:17:30.521322+00	2022-03-28 12:17:30.521335+00
6995	53	2022-03-28 12:17:30.524073+00	2022-03-28 12:17:30.524086+00
6996	53	2022-03-28 12:17:30.526856+00	2022-03-28 12:17:30.526869+00
6997	53	2022-03-28 12:17:30.529613+00	2022-03-28 12:17:30.529628+00
6998	53	2022-03-28 12:17:30.533851+00	2022-03-28 12:17:30.533872+00
6999	53	2022-03-28 12:17:30.537594+00	2022-03-28 12:17:30.537611+00
7000	53	2022-03-28 12:17:30.54099+00	2022-03-28 12:17:30.541006+00
7001	53	2022-03-28 12:17:30.545786+00	2022-03-28 12:17:30.545809+00
7002	53	2022-03-28 12:17:30.550195+00	2022-03-28 12:17:30.550213+00
7003	53	2022-03-28 12:17:30.554085+00	2022-03-28 12:17:30.554105+00
7004	53	2022-03-28 12:17:30.557985+00	2022-03-28 12:17:30.558005+00
7005	53	2022-03-28 12:17:30.562907+00	2022-03-28 12:17:30.562935+00
7006	53	2022-03-28 12:17:30.56751+00	2022-03-28 12:17:30.567533+00
7007	53	2022-03-28 12:17:30.571957+00	2022-03-28 12:17:30.571994+00
7008	53	2022-03-28 12:17:30.576374+00	2022-03-28 12:17:30.576397+00
7009	53	2022-03-28 12:17:30.580006+00	2022-03-28 12:17:30.580025+00
7010	53	2022-03-28 12:17:30.583485+00	2022-03-28 12:17:30.583504+00
7011	53	2022-03-28 12:17:30.586907+00	2022-03-28 12:17:30.586925+00
7012	53	2022-03-28 12:17:30.590292+00	2022-03-28 12:17:30.59031+00
7013	53	2022-03-28 12:17:30.594043+00	2022-03-28 12:17:30.594066+00
7014	53	2022-03-28 12:17:30.598969+00	2022-03-28 12:17:30.598995+00
7015	53	2022-03-28 12:17:30.603774+00	2022-03-28 12:17:30.603804+00
7016	53	2022-03-28 12:17:30.608925+00	2022-03-28 12:17:30.608962+00
7017	53	2022-03-28 12:17:30.61524+00	2022-03-28 12:17:30.615288+00
7018	53	2022-03-28 12:17:30.622119+00	2022-03-28 12:17:30.622171+00
7019	53	2022-03-28 12:17:30.628381+00	2022-03-28 12:17:30.628428+00
7020	53	2022-03-28 12:17:30.634634+00	2022-03-28 12:17:30.634684+00
7021	53	2022-03-28 12:17:30.642312+00	2022-03-28 12:17:30.642364+00
7022	53	2022-03-28 12:17:30.64974+00	2022-03-28 12:17:30.649791+00
7023	53	2022-03-28 12:17:30.657305+00	2022-03-28 12:17:30.657358+00
7024	53	2022-03-28 12:17:30.665229+00	2022-03-28 12:17:30.665284+00
7025	53	2022-03-28 12:17:30.672592+00	2022-03-28 12:17:30.672646+00
7026	53	2022-03-28 12:17:30.680005+00	2022-03-28 12:17:30.680059+00
7027	53	2022-03-28 12:17:30.687822+00	2022-03-28 12:17:30.687877+00
7028	53	2022-03-28 12:17:30.694922+00	2022-03-28 12:17:30.694975+00
7029	53	2022-03-28 12:17:30.702141+00	2022-03-28 12:17:30.702196+00
7030	53	2022-03-28 12:17:30.709384+00	2022-03-28 12:17:30.709436+00
7031	53	2022-03-28 12:17:30.715508+00	2022-03-28 12:17:30.715556+00
7032	53	2022-03-28 12:17:30.722203+00	2022-03-28 12:17:30.722256+00
7033	53	2022-03-28 12:17:30.728606+00	2022-03-28 12:17:30.728654+00
7034	53	2022-03-28 12:17:30.735604+00	2022-03-28 12:17:30.735657+00
7035	53	2022-03-28 12:17:30.742417+00	2022-03-28 12:17:30.74247+00
7036	53	2022-03-28 12:17:30.748964+00	2022-03-28 12:17:30.749015+00
7037	53	2022-03-28 12:17:30.755396+00	2022-03-28 12:17:30.755448+00
7038	53	2022-03-28 12:17:30.761742+00	2022-03-28 12:17:30.761829+00
7039	53	2022-03-28 12:17:30.767624+00	2022-03-28 12:17:30.767673+00
7040	53	2022-03-28 12:17:30.774248+00	2022-03-28 12:17:30.7743+00
7041	53	2022-03-28 12:17:30.780742+00	2022-03-28 12:17:30.780792+00
7042	53	2022-03-28 12:17:30.787499+00	2022-03-28 12:17:30.78755+00
7043	53	2022-03-28 12:17:30.793682+00	2022-03-28 12:17:30.793719+00
7044	53	2022-03-28 12:17:30.798511+00	2022-03-28 12:17:30.798536+00
7045	53	2022-03-28 12:17:30.802737+00	2022-03-28 12:17:30.802763+00
7046	53	2022-03-28 12:17:30.806864+00	2022-03-28 12:17:30.806888+00
7047	53	2022-03-28 12:17:30.811272+00	2022-03-28 12:17:30.811301+00
7048	53	2022-03-28 12:17:30.816296+00	2022-03-28 12:17:30.816333+00
7049	53	2022-03-28 12:17:30.821915+00	2022-03-28 12:17:30.821938+00
7050	53	2022-03-28 12:17:30.826463+00	2022-03-28 12:17:30.826489+00
7051	53	2022-03-28 12:17:30.830644+00	2022-03-28 12:17:30.830682+00
7052	53	2022-03-28 12:17:30.834806+00	2022-03-28 12:17:30.834828+00
7053	53	2022-03-28 12:17:30.837953+00	2022-03-28 12:17:30.837967+00
7054	53	2022-03-28 12:17:30.840959+00	2022-03-28 12:17:30.840974+00
7055	53	2022-03-28 12:17:30.843762+00	2022-03-28 12:17:30.843776+00
7056	53	2022-03-28 12:17:30.846504+00	2022-03-28 12:17:30.846516+00
7057	53	2022-03-28 12:17:30.849212+00	2022-03-28 12:17:30.849224+00
7058	53	2022-03-28 12:17:30.852387+00	2022-03-28 12:17:30.852401+00
7059	53	2022-03-28 12:17:30.855394+00	2022-03-28 12:17:30.855409+00
7060	53	2022-03-28 12:17:30.857922+00	2022-03-28 12:17:30.857934+00
7061	53	2022-03-28 12:17:30.860374+00	2022-03-28 12:17:30.860386+00
7062	53	2022-03-28 12:17:30.863067+00	2022-03-28 12:17:30.863083+00
7063	53	2022-03-28 12:17:30.865581+00	2022-03-28 12:17:30.865594+00
7064	53	2022-03-28 12:17:30.868356+00	2022-03-28 12:17:30.868373+00
7065	53	2022-03-28 12:17:30.871385+00	2022-03-28 12:17:30.871406+00
7066	53	2022-03-28 12:17:30.874797+00	2022-03-28 12:17:30.874835+00
7067	53	2022-03-28 12:17:30.879108+00	2022-03-28 12:17:30.879125+00
7068	53	2022-03-28 12:17:30.882416+00	2022-03-28 12:17:30.882431+00
7069	53	2022-03-28 12:17:30.885325+00	2022-03-28 12:17:30.885338+00
7070	53	2022-03-28 12:17:30.88811+00	2022-03-28 12:17:30.888122+00
7071	53	2022-03-28 12:17:30.891018+00	2022-03-28 12:17:30.89103+00
7072	53	2022-03-28 12:17:30.894056+00	2022-03-28 12:17:30.894071+00
7073	53	2022-03-28 12:17:30.89652+00	2022-03-28 12:17:30.896532+00
7074	53	2022-03-28 12:17:30.898927+00	2022-03-28 12:17:30.89894+00
7075	53	2022-03-28 12:17:30.901445+00	2022-03-28 12:17:30.901457+00
7076	53	2022-03-28 12:17:30.903951+00	2022-03-28 12:17:30.903963+00
7077	53	2022-03-28 12:17:30.906426+00	2022-03-28 12:17:30.906439+00
7078	53	2022-03-28 12:17:30.90893+00	2022-03-28 12:17:30.908943+00
7079	53	2022-03-28 12:17:30.911397+00	2022-03-28 12:17:30.911409+00
7080	53	2022-03-28 12:17:30.913891+00	2022-03-28 12:17:30.913904+00
7081	53	2022-03-28 12:17:30.916658+00	2022-03-28 12:17:30.916672+00
7082	53	2022-03-28 12:17:30.919201+00	2022-03-28 12:17:30.919214+00
7083	53	2022-03-28 12:17:30.921663+00	2022-03-28 12:17:30.921676+00
7084	53	2022-03-28 12:17:30.924297+00	2022-03-28 12:17:30.924309+00
7085	53	2022-03-28 12:17:30.927103+00	2022-03-28 12:17:30.927115+00
7086	53	2022-03-28 12:17:30.929946+00	2022-03-28 12:17:30.929958+00
7087	53	2022-03-28 12:17:30.932886+00	2022-03-28 12:17:30.932898+00
7088	53	2022-03-28 12:17:30.935788+00	2022-03-28 12:17:30.9358+00
7089	53	2022-03-28 12:17:30.939817+00	2022-03-28 12:17:30.939838+00
7090	53	2022-03-28 12:17:30.943596+00	2022-03-28 12:17:30.943611+00
7091	53	2022-03-28 12:17:30.946707+00	2022-03-28 12:17:30.946722+00
7092	53	2022-03-28 12:17:30.949722+00	2022-03-28 12:17:30.949736+00
7093	53	2022-03-28 12:17:30.952842+00	2022-03-28 12:17:30.952857+00
7094	53	2022-03-28 12:17:30.955978+00	2022-03-28 12:17:30.955993+00
7095	53	2022-03-28 12:17:30.959292+00	2022-03-28 12:17:30.959309+00
7096	53	2022-03-28 12:17:30.962768+00	2022-03-28 12:17:30.962784+00
7097	53	2022-03-28 12:17:30.96562+00	2022-03-28 12:17:30.965633+00
7098	53	2022-03-28 12:17:30.968257+00	2022-03-28 12:17:30.968269+00
7099	53	2022-03-28 12:17:30.970884+00	2022-03-28 12:17:30.970895+00
7100	53	2022-03-28 12:17:30.973452+00	2022-03-28 12:17:30.973463+00
7101	53	2022-03-28 12:17:30.975995+00	2022-03-28 12:17:30.976007+00
7102	53	2022-03-28 12:17:30.978638+00	2022-03-28 12:17:30.978649+00
7103	53	2022-03-28 12:17:30.981279+00	2022-03-28 12:17:30.98129+00
7104	53	2022-03-28 12:17:30.983985+00	2022-03-28 12:17:30.983999+00
7105	53	2022-03-28 12:17:30.986683+00	2022-03-28 12:17:30.986695+00
7106	53	2022-03-28 12:17:30.989503+00	2022-03-28 12:17:30.989514+00
7107	53	2022-03-28 12:17:30.992192+00	2022-03-28 12:17:30.992203+00
7108	53	2022-03-28 12:17:30.994885+00	2022-03-28 12:17:30.994897+00
7109	53	2022-03-28 12:17:30.997708+00	2022-03-28 12:17:30.997719+00
7110	53	2022-03-28 12:17:31.000551+00	2022-03-28 12:17:31.000563+00
7111	53	2022-03-28 12:17:31.003423+00	2022-03-28 12:17:31.003434+00
7112	53	2022-03-28 12:17:31.006239+00	2022-03-28 12:17:31.006251+00
7113	53	2022-03-28 12:17:31.009318+00	2022-03-28 12:17:31.009329+00
7114	53	2022-03-28 12:17:31.012158+00	2022-03-28 12:17:31.01217+00
7115	53	2022-03-28 12:17:31.015142+00	2022-03-28 12:17:31.015157+00
7116	53	2022-03-28 12:17:31.017837+00	2022-03-28 12:17:31.017849+00
7117	53	2022-03-28 12:17:31.020249+00	2022-03-28 12:17:31.020261+00
7118	53	2022-03-28 12:17:31.022903+00	2022-03-28 12:17:31.022914+00
7119	53	2022-03-28 12:17:31.025516+00	2022-03-28 12:17:31.025528+00
7120	53	2022-03-28 12:17:31.028166+00	2022-03-28 12:17:31.028178+00
7121	53	2022-03-28 12:17:31.030815+00	2022-03-28 12:17:31.030826+00
7122	53	2022-03-28 12:17:31.033596+00	2022-03-28 12:17:31.033608+00
7123	53	2022-03-28 12:17:31.037274+00	2022-03-28 12:17:31.03729+00
7124	53	2022-03-28 12:17:31.04113+00	2022-03-28 12:17:31.041146+00
7125	53	2022-03-28 12:17:31.045088+00	2022-03-28 12:17:31.045107+00
7126	53	2022-03-28 12:17:31.048599+00	2022-03-28 12:17:31.048613+00
7127	53	2022-03-28 12:17:31.05143+00	2022-03-28 12:17:31.051442+00
7128	53	2022-03-28 12:17:31.054901+00	2022-03-28 12:17:31.054917+00
7129	53	2022-03-28 12:17:31.058369+00	2022-03-28 12:17:31.058385+00
7130	53	2022-03-28 12:17:31.062469+00	2022-03-28 12:17:31.062485+00
7131	53	2022-03-28 12:17:31.066133+00	2022-03-28 12:17:31.06615+00
7132	53	2022-03-28 12:17:31.069698+00	2022-03-28 12:17:31.069715+00
7133	53	2022-03-28 12:17:31.072595+00	2022-03-28 12:17:31.072608+00
7134	53	2022-03-28 12:17:31.075462+00	2022-03-28 12:17:31.075475+00
7135	53	2022-03-28 12:17:31.078146+00	2022-03-28 12:17:31.078159+00
7136	53	2022-03-28 12:17:31.084662+00	2022-03-28 12:17:31.08468+00
7137	53	2022-03-28 12:17:31.087947+00	2022-03-28 12:17:31.087962+00
7138	53	2022-03-28 12:17:31.090632+00	2022-03-28 12:17:31.090645+00
7139	53	2022-03-28 12:17:31.093395+00	2022-03-28 12:17:31.093408+00
7140	53	2022-03-28 12:17:31.096095+00	2022-03-28 12:17:31.096107+00
7141	53	2022-03-28 12:17:31.098959+00	2022-03-28 12:17:31.098971+00
7142	53	2022-03-28 12:17:31.101845+00	2022-03-28 12:17:31.101857+00
7143	53	2022-03-28 12:17:31.104481+00	2022-03-28 12:17:31.104492+00
7144	53	2022-03-28 12:17:31.107196+00	2022-03-28 12:17:31.107207+00
7145	53	2022-03-28 12:17:31.109909+00	2022-03-28 12:17:31.109921+00
7146	53	2022-03-28 12:17:31.112623+00	2022-03-28 12:17:31.112635+00
7147	53	2022-03-28 12:17:31.115355+00	2022-03-28 12:17:31.115367+00
7148	53	2022-03-28 12:17:31.118196+00	2022-03-28 12:17:31.118207+00
7149	53	2022-03-28 12:17:31.124908+00	2022-03-28 12:17:31.124948+00
7150	53	2022-03-28 12:17:31.134795+00	2022-03-28 12:17:31.134811+00
7151	53	2022-03-28 12:17:31.13807+00	2022-03-28 12:17:31.138084+00
7152	53	2022-03-28 12:17:31.140687+00	2022-03-28 12:17:31.140699+00
7153	53	2022-03-28 12:17:31.143601+00	2022-03-28 12:17:31.143613+00
7154	53	2022-03-28 12:17:31.146268+00	2022-03-28 12:17:31.14628+00
7155	53	2022-03-28 12:17:31.148908+00	2022-03-28 12:17:31.148921+00
7156	53	2022-03-28 12:17:31.151769+00	2022-03-28 12:17:31.151782+00
7157	53	2022-03-28 12:17:31.154649+00	2022-03-28 12:17:31.154661+00
7158	53	2022-03-28 12:17:31.158604+00	2022-03-28 12:17:31.158621+00
7159	53	2022-03-28 12:17:31.162487+00	2022-03-28 12:17:31.162503+00
7160	53	2022-03-28 12:17:31.165568+00	2022-03-28 12:17:31.165581+00
7161	53	2022-03-28 12:17:31.169103+00	2022-03-28 12:17:31.169118+00
7162	53	2022-03-28 12:17:31.17278+00	2022-03-28 12:17:31.172796+00
7163	53	2022-03-28 12:17:31.176575+00	2022-03-28 12:17:31.176592+00
7164	53	2022-03-28 12:17:31.180498+00	2022-03-28 12:17:31.180515+00
7165	53	2022-03-28 12:17:31.183655+00	2022-03-28 12:17:31.18367+00
7166	53	2022-03-28 12:17:31.186993+00	2022-03-28 12:17:31.18701+00
7167	53	2022-03-28 12:17:31.190586+00	2022-03-28 12:17:31.190603+00
7168	53	2022-03-28 12:17:31.193517+00	2022-03-28 12:17:31.193531+00
7169	53	2022-03-28 12:17:31.197278+00	2022-03-28 12:17:31.197296+00
7170	53	2022-03-28 12:17:31.200317+00	2022-03-28 12:17:31.200331+00
7171	53	2022-03-28 12:17:31.203008+00	2022-03-28 12:17:31.203021+00
7172	53	2022-03-28 12:17:31.20566+00	2022-03-28 12:17:31.205672+00
7173	53	2022-03-28 12:17:31.208624+00	2022-03-28 12:17:31.208641+00
7174	53	2022-03-28 12:17:31.211328+00	2022-03-28 12:17:31.211341+00
7175	53	2022-03-28 12:17:31.213883+00	2022-03-28 12:17:31.213895+00
7176	53	2022-03-28 12:17:31.216616+00	2022-03-28 12:17:31.21663+00
7177	53	2022-03-28 12:17:31.219371+00	2022-03-28 12:17:31.219383+00
7178	53	2022-03-28 12:17:31.222092+00	2022-03-28 12:17:31.222104+00
7179	53	2022-03-28 12:17:31.224932+00	2022-03-28 12:17:31.224943+00
7180	53	2022-03-28 12:17:31.227748+00	2022-03-28 12:17:31.227759+00
7181	53	2022-03-28 12:17:31.230441+00	2022-03-28 12:17:31.230452+00
7182	53	2022-03-28 12:17:31.233239+00	2022-03-28 12:17:31.233251+00
7183	53	2022-03-28 12:17:31.236137+00	2022-03-28 12:17:31.236149+00
7184	53	2022-03-28 12:17:31.238899+00	2022-03-28 12:17:31.23891+00
7185	53	2022-03-28 12:17:31.241496+00	2022-03-28 12:17:31.241507+00
7186	53	2022-03-28 12:17:31.243964+00	2022-03-28 12:17:31.243975+00
7187	53	2022-03-28 12:17:31.246648+00	2022-03-28 12:17:31.24666+00
7188	53	2022-03-28 12:17:31.249449+00	2022-03-28 12:17:31.24946+00
7189	53	2022-03-28 12:17:31.252081+00	2022-03-28 12:17:31.252093+00
7190	53	2022-03-28 12:17:31.25465+00	2022-03-28 12:17:31.254661+00
7191	53	2022-03-28 12:17:31.25745+00	2022-03-28 12:17:31.257461+00
7192	53	2022-03-28 12:17:31.259991+00	2022-03-28 12:17:31.260016+00
7193	53	2022-03-28 12:17:31.262663+00	2022-03-28 12:17:31.262673+00
7194	53	2022-03-28 12:17:31.265382+00	2022-03-28 12:17:31.265393+00
7195	53	2022-03-28 12:17:31.268192+00	2022-03-28 12:17:31.268203+00
7196	53	2022-03-28 12:17:31.27092+00	2022-03-28 12:17:31.270931+00
7197	53	2022-03-28 12:17:31.27634+00	2022-03-28 12:17:31.276388+00
7198	53	2022-03-28 12:17:31.282576+00	2022-03-28 12:17:31.282624+00
7199	53	2022-03-28 12:17:31.288953+00	2022-03-28 12:17:31.289002+00
7200	53	2022-03-28 12:17:31.29666+00	2022-03-28 12:17:31.296715+00
7201	53	2022-03-28 12:17:31.304446+00	2022-03-28 12:17:31.3045+00
7202	53	2022-03-28 12:17:31.311766+00	2022-03-28 12:17:31.311857+00
7203	53	2022-03-28 12:17:31.319164+00	2022-03-28 12:17:31.319216+00
7204	53	2022-03-28 12:17:31.325454+00	2022-03-28 12:17:31.325502+00
7205	53	2022-03-28 12:17:31.331609+00	2022-03-28 12:17:31.331656+00
7206	53	2022-03-28 12:17:31.339015+00	2022-03-28 12:17:31.339051+00
7207	53	2022-03-28 12:17:31.344649+00	2022-03-28 12:17:31.344678+00
7208	53	2022-03-28 12:17:31.348949+00	2022-03-28 12:17:31.348973+00
7209	53	2022-03-28 12:17:31.353355+00	2022-03-28 12:17:31.353384+00
7210	53	2022-03-28 12:17:31.358243+00	2022-03-28 12:17:31.358265+00
7211	53	2022-03-28 12:17:31.362563+00	2022-03-28 12:17:31.362583+00
7212	53	2022-03-28 12:17:31.367057+00	2022-03-28 12:17:31.367078+00
7213	53	2022-03-28 12:17:31.37129+00	2022-03-28 12:17:31.37131+00
7214	53	2022-03-28 12:17:31.375579+00	2022-03-28 12:17:31.375599+00
7215	53	2022-03-28 12:17:31.37971+00	2022-03-28 12:17:31.379729+00
7216	53	2022-03-28 12:17:31.382787+00	2022-03-28 12:17:31.382802+00
7217	53	2022-03-28 12:17:31.386656+00	2022-03-28 12:17:31.386676+00
7218	53	2022-03-28 12:17:31.389749+00	2022-03-28 12:17:31.389765+00
7219	53	2022-03-28 12:17:31.393049+00	2022-03-28 12:17:31.393069+00
7220	53	2022-03-28 12:17:31.396541+00	2022-03-28 12:17:31.39656+00
7221	53	2022-03-28 12:17:31.400214+00	2022-03-28 12:17:31.400235+00
7222	53	2022-03-28 12:17:31.404246+00	2022-03-28 12:17:31.404265+00
7223	53	2022-03-28 12:17:31.40782+00	2022-03-28 12:17:31.407838+00
7224	53	2022-03-28 12:17:31.411051+00	2022-03-28 12:17:31.411067+00
7225	53	2022-03-28 12:17:31.413956+00	2022-03-28 12:17:31.413969+00
7226	53	2022-03-28 12:17:31.416831+00	2022-03-28 12:17:31.416843+00
7227	53	2022-03-28 12:17:31.419618+00	2022-03-28 12:17:31.419632+00
7228	53	2022-03-28 12:17:31.42241+00	2022-03-28 12:17:31.422423+00
7229	53	2022-03-28 12:17:31.425384+00	2022-03-28 12:17:31.425395+00
7230	53	2022-03-28 12:17:31.428173+00	2022-03-28 12:17:31.428184+00
7231	53	2022-03-28 12:17:31.430976+00	2022-03-28 12:17:31.430987+00
7232	53	2022-03-28 12:17:31.433648+00	2022-03-28 12:17:31.43366+00
7233	53	2022-03-28 12:17:31.436584+00	2022-03-28 12:17:31.436597+00
7234	53	2022-03-28 12:17:31.439349+00	2022-03-28 12:17:31.439362+00
7235	53	2022-03-28 12:17:31.442187+00	2022-03-28 12:17:31.4422+00
7236	53	2022-03-28 12:17:31.445035+00	2022-03-28 12:17:31.445047+00
7237	53	2022-03-28 12:17:31.447716+00	2022-03-28 12:17:31.447728+00
7238	53	2022-03-28 12:17:31.450308+00	2022-03-28 12:17:31.450321+00
7239	53	2022-03-28 12:17:31.452889+00	2022-03-28 12:17:31.452902+00
7240	53	2022-03-28 12:17:31.455422+00	2022-03-28 12:17:31.455436+00
7241	53	2022-03-28 12:17:31.457949+00	2022-03-28 12:17:31.457962+00
7242	53	2022-03-28 12:17:31.460653+00	2022-03-28 12:17:31.460666+00
7243	53	2022-03-28 12:17:31.463334+00	2022-03-28 12:17:31.463347+00
7244	53	2022-03-28 12:17:31.466055+00	2022-03-28 12:17:31.466067+00
7245	53	2022-03-28 12:17:31.46887+00	2022-03-28 12:17:31.468882+00
7246	53	2022-03-28 12:17:31.471567+00	2022-03-28 12:17:31.471578+00
7247	53	2022-03-28 12:17:31.474194+00	2022-03-28 12:17:31.474205+00
7248	53	2022-03-28 12:17:31.477144+00	2022-03-28 12:17:31.477155+00
7249	53	2022-03-28 12:17:31.479953+00	2022-03-28 12:17:31.479964+00
7250	53	2022-03-28 12:17:31.483068+00	2022-03-28 12:17:31.48309+00
7251	53	2022-03-28 12:17:31.486952+00	2022-03-28 12:17:31.486969+00
7252	53	2022-03-28 12:17:31.490664+00	2022-03-28 12:17:31.490679+00
7253	53	2022-03-28 12:17:31.493893+00	2022-03-28 12:17:31.493908+00
7254	53	2022-03-28 12:17:31.496781+00	2022-03-28 12:17:31.496794+00
7255	53	2022-03-28 12:17:31.499677+00	2022-03-28 12:17:31.499689+00
7256	53	2022-03-28 12:17:31.504142+00	2022-03-28 12:17:31.504198+00
7257	53	2022-03-28 12:17:31.51149+00	2022-03-28 12:17:31.511542+00
7258	53	2022-03-28 12:17:31.518043+00	2022-03-28 12:17:31.518114+00
7259	53	2022-03-28 12:17:31.525099+00	2022-03-28 12:17:31.525188+00
7260	53	2022-03-28 12:17:31.53149+00	2022-03-28 12:17:31.531537+00
7261	53	2022-03-28 12:17:31.537981+00	2022-03-28 12:17:31.53803+00
7262	53	2022-03-28 12:17:31.544327+00	2022-03-28 12:17:31.544376+00
7263	53	2022-03-28 12:17:31.551202+00	2022-03-28 12:17:31.551255+00
7264	53	2022-03-28 12:17:31.557691+00	2022-03-28 12:17:31.557738+00
7265	53	2022-03-28 12:17:31.565525+00	2022-03-28 12:17:31.565578+00
7266	53	2022-03-28 12:17:31.572746+00	2022-03-28 12:17:31.572798+00
7267	53	2022-03-28 12:17:31.578954+00	2022-03-28 12:17:31.579001+00
7268	53	2022-03-28 12:17:31.585228+00	2022-03-28 12:17:31.585279+00
7269	53	2022-03-28 12:17:31.591605+00	2022-03-28 12:17:31.591652+00
7270	53	2022-03-28 12:17:31.597902+00	2022-03-28 12:17:31.597949+00
7271	53	2022-03-28 12:17:31.604155+00	2022-03-28 12:17:31.604202+00
7272	53	2022-03-28 12:17:31.610963+00	2022-03-28 12:17:31.611016+00
7273	53	2022-03-28 12:17:31.618362+00	2022-03-28 12:17:31.618414+00
7274	53	2022-03-28 12:17:31.626059+00	2022-03-28 12:17:31.626112+00
7275	53	2022-03-28 12:17:31.632571+00	2022-03-28 12:17:31.632619+00
7276	53	2022-03-28 12:17:31.640359+00	2022-03-28 12:17:31.640413+00
7277	53	2022-03-28 12:17:31.648441+00	2022-03-28 12:17:31.648539+00
7278	53	2022-03-28 12:17:31.655978+00	2022-03-28 12:17:31.656029+00
7279	53	2022-03-28 12:17:31.663694+00	2022-03-28 12:17:31.663749+00
7280	53	2022-03-28 12:17:31.671221+00	2022-03-28 12:17:31.671276+00
7281	53	2022-03-28 12:17:31.676761+00	2022-03-28 12:17:31.676783+00
7282	53	2022-03-28 12:17:31.680813+00	2022-03-28 12:17:31.680833+00
7283	53	2022-03-28 12:17:31.684783+00	2022-03-28 12:17:31.684835+00
7284	53	2022-03-28 12:17:31.689883+00	2022-03-28 12:17:31.689915+00
7285	53	2022-03-28 12:17:31.69422+00	2022-03-28 12:17:31.694243+00
7286	53	2022-03-28 12:17:31.698763+00	2022-03-28 12:17:31.698783+00
7287	53	2022-03-28 12:17:31.702827+00	2022-03-28 12:17:31.702846+00
7288	53	2022-03-28 12:17:31.706766+00	2022-03-28 12:17:31.706785+00
7289	53	2022-03-28 12:17:31.710384+00	2022-03-28 12:17:31.710405+00
7290	53	2022-03-28 12:17:31.713862+00	2022-03-28 12:17:31.713879+00
7291	53	2022-03-28 12:17:31.717423+00	2022-03-28 12:17:31.717443+00
7292	53	2022-03-28 12:17:31.721024+00	2022-03-28 12:17:31.721042+00
7293	53	2022-03-28 12:17:31.725214+00	2022-03-28 12:17:31.725235+00
7294	53	2022-03-28 12:17:31.72936+00	2022-03-28 12:17:31.72938+00
7295	53	2022-03-28 12:17:31.732838+00	2022-03-28 12:17:31.732856+00
7296	53	2022-03-28 12:17:31.736075+00	2022-03-28 12:17:31.736092+00
7297	53	2022-03-28 12:17:31.7398+00	2022-03-28 12:17:31.739821+00
7298	53	2022-03-28 12:17:31.744292+00	2022-03-28 12:17:31.744312+00
7299	53	2022-03-28 12:17:31.748231+00	2022-03-28 12:17:31.748252+00
7300	53	2022-03-28 12:17:31.751899+00	2022-03-28 12:17:31.751919+00
7301	53	2022-03-28 12:17:31.75596+00	2022-03-28 12:17:31.755982+00
7302	53	2022-03-28 12:17:31.760597+00	2022-03-28 12:17:31.760622+00
7303	53	2022-03-28 12:17:31.765094+00	2022-03-28 12:17:31.765117+00
7304	53	2022-03-28 12:17:31.769745+00	2022-03-28 12:17:31.769768+00
7305	53	2022-03-28 12:17:31.773556+00	2022-03-28 12:17:31.773575+00
7306	53	2022-03-28 12:17:31.777017+00	2022-03-28 12:17:31.777037+00
7307	53	2022-03-28 12:17:31.781604+00	2022-03-28 12:17:31.781626+00
7308	53	2022-03-28 12:17:31.785946+00	2022-03-28 12:17:31.785967+00
7309	53	2022-03-28 12:17:31.790255+00	2022-03-28 12:17:31.790275+00
7310	53	2022-03-28 12:17:31.793808+00	2022-03-28 12:17:31.793823+00
7311	53	2022-03-28 12:17:31.79691+00	2022-03-28 12:17:31.796923+00
7312	53	2022-03-28 12:17:31.799971+00	2022-03-28 12:17:31.799983+00
7313	53	2022-03-28 12:17:31.80297+00	2022-03-28 12:17:31.802983+00
7314	53	2022-03-28 12:17:31.80598+00	2022-03-28 12:17:31.805992+00
7315	53	2022-03-28 12:17:31.808838+00	2022-03-28 12:17:31.808852+00
7316	53	2022-03-28 12:17:31.811762+00	2022-03-28 12:17:31.811776+00
7317	53	2022-03-28 12:17:31.814662+00	2022-03-28 12:17:31.814674+00
7318	53	2022-03-28 12:17:31.817512+00	2022-03-28 12:17:31.817524+00
7319	53	2022-03-28 12:17:31.820475+00	2022-03-28 12:17:31.820488+00
7320	53	2022-03-28 12:17:31.823246+00	2022-03-28 12:17:31.823258+00
7321	53	2022-03-28 12:17:31.825972+00	2022-03-28 12:17:31.825984+00
7322	53	2022-03-28 12:17:31.82879+00	2022-03-28 12:17:31.828802+00
7323	53	2022-03-28 12:17:31.831457+00	2022-03-28 12:17:31.831469+00
7324	53	2022-03-28 12:17:31.834035+00	2022-03-28 12:17:31.834047+00
7325	53	2022-03-28 12:17:31.836836+00	2022-03-28 12:17:31.836848+00
7326	53	2022-03-28 12:17:31.839607+00	2022-03-28 12:17:31.839619+00
7327	53	2022-03-28 12:17:31.842247+00	2022-03-28 12:17:31.842258+00
7328	53	2022-03-28 12:17:31.845007+00	2022-03-28 12:17:31.845019+00
7329	53	2022-03-28 12:17:31.847917+00	2022-03-28 12:17:31.847929+00
7330	53	2022-03-28 12:17:31.850719+00	2022-03-28 12:17:31.850731+00
7331	53	2022-03-28 12:17:31.85346+00	2022-03-28 12:17:31.853471+00
7332	53	2022-03-28 12:17:31.856131+00	2022-03-28 12:17:31.856144+00
7333	53	2022-03-28 12:17:31.858737+00	2022-03-28 12:17:31.858749+00
7334	53	2022-03-28 12:17:31.861431+00	2022-03-28 12:17:31.861442+00
7335	53	2022-03-28 12:17:31.864177+00	2022-03-28 12:17:31.864187+00
7336	53	2022-03-28 12:17:31.8668+00	2022-03-28 12:17:31.866811+00
7337	53	2022-03-28 12:17:31.86938+00	2022-03-28 12:17:31.869391+00
7338	53	2022-03-28 12:17:31.871972+00	2022-03-28 12:17:31.871983+00
7339	53	2022-03-28 12:17:31.87465+00	2022-03-28 12:17:31.874664+00
7340	53	2022-03-28 12:17:31.877354+00	2022-03-28 12:17:31.877367+00
7341	53	2022-03-28 12:17:31.880036+00	2022-03-28 12:17:31.880049+00
7342	53	2022-03-28 12:17:31.882698+00	2022-03-28 12:17:31.882709+00
7343	53	2022-03-28 12:17:31.885545+00	2022-03-28 12:17:31.885557+00
7344	53	2022-03-28 12:17:31.888434+00	2022-03-28 12:17:31.888502+00
7345	53	2022-03-28 12:17:31.892918+00	2022-03-28 12:17:31.892936+00
7346	53	2022-03-28 12:17:31.896803+00	2022-03-28 12:17:31.89682+00
7347	53	2022-03-28 12:17:31.901001+00	2022-03-28 12:17:31.901029+00
7348	53	2022-03-28 12:17:31.904537+00	2022-03-28 12:17:31.904552+00
7349	53	2022-03-28 12:17:31.907677+00	2022-03-28 12:17:31.907694+00
7350	53	2022-03-28 12:17:31.910699+00	2022-03-28 12:17:31.910716+00
7351	53	2022-03-28 12:17:31.913795+00	2022-03-28 12:17:31.913811+00
7352	53	2022-03-28 12:17:31.916931+00	2022-03-28 12:17:31.916946+00
7353	53	2022-03-28 12:17:31.92024+00	2022-03-28 12:17:31.920257+00
7354	53	2022-03-28 12:17:31.926875+00	2022-03-28 12:17:31.926891+00
7355	53	2022-03-28 12:17:31.937523+00	2022-03-28 12:17:31.937543+00
7356	53	2022-03-28 12:17:31.944269+00	2022-03-28 12:17:31.944286+00
7357	53	2022-03-28 12:17:31.947603+00	2022-03-28 12:17:31.947617+00
7358	53	2022-03-28 12:17:31.951894+00	2022-03-28 12:17:31.951914+00
7359	53	2022-03-28 12:17:31.956111+00	2022-03-28 12:17:31.956132+00
7360	53	2022-03-28 12:17:31.96048+00	2022-03-28 12:17:31.960504+00
7361	53	2022-03-28 12:17:31.964362+00	2022-03-28 12:17:31.964386+00
7362	53	2022-03-28 12:17:31.968631+00	2022-03-28 12:17:31.968662+00
7363	53	2022-03-28 12:17:31.973248+00	2022-03-28 12:17:31.97328+00
7364	53	2022-03-28 12:17:31.978552+00	2022-03-28 12:17:31.978589+00
7365	53	2022-03-28 12:17:31.983852+00	2022-03-28 12:17:31.983888+00
7366	53	2022-03-28 12:17:31.989514+00	2022-03-28 12:17:31.989549+00
7367	53	2022-03-28 12:17:31.994819+00	2022-03-28 12:17:31.994856+00
7368	53	2022-03-28 12:17:32.000457+00	2022-03-28 12:17:32.000491+00
7369	53	2022-03-28 12:17:32.00532+00	2022-03-28 12:17:32.005352+00
7370	53	2022-03-28 12:17:32.010455+00	2022-03-28 12:17:32.010505+00
7371	53	2022-03-28 12:17:32.015824+00	2022-03-28 12:17:32.015875+00
7372	53	2022-03-28 12:17:32.021536+00	2022-03-28 12:17:32.021573+00
7373	53	2022-03-28 12:17:32.02736+00	2022-03-28 12:17:32.02741+00
7374	53	2022-03-28 12:17:32.033036+00	2022-03-28 12:17:32.033086+00
7375	53	2022-03-28 12:17:32.038536+00	2022-03-28 12:17:32.038571+00
7376	53	2022-03-28 12:17:32.043901+00	2022-03-28 12:17:32.043936+00
7377	53	2022-03-28 12:17:32.048582+00	2022-03-28 12:17:32.048615+00
7378	53	2022-03-28 12:17:32.05417+00	2022-03-28 12:17:32.054205+00
7379	53	2022-03-28 12:17:32.058883+00	2022-03-28 12:17:32.058914+00
7380	53	2022-03-28 12:17:32.06413+00	2022-03-28 12:17:32.064167+00
7381	53	2022-03-28 12:17:32.069143+00	2022-03-28 12:17:32.069176+00
7382	53	2022-03-28 12:17:32.074636+00	2022-03-28 12:17:32.074672+00
7383	53	2022-03-28 12:17:32.079362+00	2022-03-28 12:17:32.079394+00
7384	53	2022-03-28 12:17:32.084527+00	2022-03-28 12:17:32.084564+00
7385	53	2022-03-28 12:17:32.089509+00	2022-03-28 12:17:32.08954+00
7386	53	2022-03-28 12:17:32.094205+00	2022-03-28 12:17:32.094236+00
7387	53	2022-03-28 12:17:32.100222+00	2022-03-28 12:17:32.10026+00
7388	53	2022-03-28 12:17:32.105473+00	2022-03-28 12:17:32.105505+00
7389	53	2022-03-28 12:17:32.111243+00	2022-03-28 12:17:32.11128+00
7390	53	2022-03-28 12:17:32.116215+00	2022-03-28 12:17:32.116247+00
7391	53	2022-03-28 12:17:32.12099+00	2022-03-28 12:17:32.121023+00
7392	53	2022-03-28 12:17:32.125672+00	2022-03-28 12:17:32.125705+00
7393	53	2022-03-28 12:17:32.130349+00	2022-03-28 12:17:32.130381+00
7394	53	2022-03-28 12:17:32.134995+00	2022-03-28 12:17:32.135026+00
7395	53	2022-03-28 12:17:32.14055+00	2022-03-28 12:17:32.140585+00
7396	53	2022-03-28 12:17:32.146186+00	2022-03-28 12:17:32.146222+00
7397	53	2022-03-28 12:17:32.150963+00	2022-03-28 12:17:32.150996+00
7398	53	2022-03-28 12:17:32.15651+00	2022-03-28 12:17:32.156547+00
7399	53	2022-03-28 12:17:32.162559+00	2022-03-28 12:17:32.162596+00
7400	53	2022-03-28 12:17:32.168024+00	2022-03-28 12:17:32.16806+00
7401	53	2022-03-28 12:17:32.173578+00	2022-03-28 12:17:32.173629+00
7402	53	2022-03-28 12:17:32.178709+00	2022-03-28 12:17:32.178747+00
7403	53	2022-03-28 12:17:32.183246+00	2022-03-28 12:17:32.183278+00
7404	53	2022-03-28 12:17:32.187021+00	2022-03-28 12:17:32.187039+00
7405	53	2022-03-28 12:17:32.190289+00	2022-03-28 12:17:32.190305+00
7406	53	2022-03-28 12:17:32.193568+00	2022-03-28 12:17:32.193582+00
7407	53	2022-03-28 12:17:32.196733+00	2022-03-28 12:17:32.196746+00
7408	53	2022-03-28 12:17:32.200185+00	2022-03-28 12:17:32.200196+00
7409	53	2022-03-28 12:17:32.204153+00	2022-03-28 12:17:32.20417+00
7410	53	2022-03-28 12:17:32.20721+00	2022-03-28 12:17:32.207222+00
7411	53	2022-03-28 12:17:32.210174+00	2022-03-28 12:17:32.210187+00
7412	53	2022-03-28 12:17:32.213182+00	2022-03-28 12:17:32.213194+00
7413	53	2022-03-28 12:17:32.216252+00	2022-03-28 12:17:32.216264+00
7414	53	2022-03-28 12:17:32.220251+00	2022-03-28 12:17:32.220298+00
7415	53	2022-03-28 12:17:32.22656+00	2022-03-28 12:17:32.226609+00
7416	53	2022-03-28 12:17:32.233474+00	2022-03-28 12:17:32.233528+00
7417	53	2022-03-28 12:17:32.240993+00	2022-03-28 12:17:32.241047+00
7418	53	2022-03-28 12:17:32.24881+00	2022-03-28 12:17:32.248866+00
7419	53	2022-03-28 12:17:32.257016+00	2022-03-28 12:17:32.257064+00
7420	53	2022-03-28 12:17:32.264693+00	2022-03-28 12:17:32.264746+00
7421	53	2022-03-28 12:17:32.271504+00	2022-03-28 12:17:32.271554+00
7422	53	2022-03-28 12:17:32.278709+00	2022-03-28 12:17:32.278771+00
7423	53	2022-03-28 12:17:32.286105+00	2022-03-28 12:17:32.286154+00
7424	53	2022-03-28 12:17:32.294463+00	2022-03-28 12:17:32.294535+00
7425	53	2022-03-28 12:17:32.302042+00	2022-03-28 12:17:32.302093+00
7426	53	2022-03-28 12:17:32.310384+00	2022-03-28 12:17:32.310453+00
7427	53	2022-03-28 12:17:32.318169+00	2022-03-28 12:17:32.318217+00
7428	53	2022-03-28 12:17:32.325788+00	2022-03-28 12:17:32.325848+00
7429	53	2022-03-28 12:17:32.333703+00	2022-03-28 12:17:32.333758+00
7430	53	2022-03-28 12:17:32.340751+00	2022-03-28 12:17:32.340812+00
7431	53	2022-03-28 12:17:32.348621+00	2022-03-28 12:17:32.348682+00
7432	53	2022-03-28 12:17:32.355774+00	2022-03-28 12:17:32.355841+00
7433	53	2022-03-28 12:17:32.364589+00	2022-03-28 12:17:32.364637+00
7434	53	2022-03-28 12:17:32.372004+00	2022-03-28 12:17:32.372073+00
7435	53	2022-03-28 12:17:32.380599+00	2022-03-28 12:17:32.380659+00
7436	53	2022-03-28 12:17:32.387695+00	2022-03-28 12:17:32.387759+00
7437	53	2022-03-28 12:17:32.395524+00	2022-03-28 12:17:32.395598+00
7438	53	2022-03-28 12:17:32.403585+00	2022-03-28 12:17:32.403633+00
7439	53	2022-03-28 12:17:32.409783+00	2022-03-28 12:17:32.409831+00
7440	53	2022-03-28 12:17:32.416362+00	2022-03-28 12:17:32.416408+00
7441	53	2022-03-28 12:17:32.42213+00	2022-03-28 12:17:32.422164+00
7442	53	2022-03-28 12:17:32.4276+00	2022-03-28 12:17:32.427634+00
7443	53	2022-03-28 12:17:32.434254+00	2022-03-28 12:17:32.434292+00
7444	53	2022-03-28 12:17:32.440521+00	2022-03-28 12:17:32.440554+00
7445	53	2022-03-28 12:17:32.446396+00	2022-03-28 12:17:32.446445+00
7446	53	2022-03-28 12:17:32.453985+00	2022-03-28 12:17:32.454036+00
7447	53	2022-03-28 12:17:32.45915+00	2022-03-28 12:17:32.459178+00
7448	53	2022-03-28 12:17:32.464911+00	2022-03-28 12:17:32.464972+00
7449	53	2022-03-28 12:17:32.470864+00	2022-03-28 12:17:32.470896+00
7450	53	2022-03-28 12:17:32.475882+00	2022-03-28 12:17:32.475932+00
7451	53	2022-03-28 12:17:32.482609+00	2022-03-28 12:17:32.482647+00
7452	53	2022-03-28 12:17:32.4887+00	2022-03-28 12:17:32.488731+00
7453	53	2022-03-28 12:17:32.493591+00	2022-03-28 12:17:32.49364+00
7454	53	2022-03-28 12:17:32.500383+00	2022-03-28 12:17:32.500431+00
7455	53	2022-03-28 12:17:32.506166+00	2022-03-28 12:17:32.506194+00
7456	53	2022-03-28 12:17:32.510316+00	2022-03-28 12:17:32.510337+00
7457	53	2022-03-28 12:17:32.515433+00	2022-03-28 12:17:32.51546+00
7458	53	2022-03-28 12:17:32.521935+00	2022-03-28 12:17:32.521975+00
7459	53	2022-03-28 12:17:32.526356+00	2022-03-28 12:17:32.526389+00
7460	53	2022-03-28 12:17:32.53061+00	2022-03-28 12:17:32.530631+00
7461	53	2022-03-28 12:17:32.536433+00	2022-03-28 12:17:32.536473+00
7462	53	2022-03-28 12:17:32.541978+00	2022-03-28 12:17:32.542+00
7463	53	2022-03-28 12:17:32.546284+00	2022-03-28 12:17:32.546307+00
7464	53	2022-03-28 12:17:32.551436+00	2022-03-28 12:17:32.551473+00
7465	53	2022-03-28 12:17:32.557389+00	2022-03-28 12:17:32.557416+00
7466	53	2022-03-28 12:17:32.561883+00	2022-03-28 12:17:32.561905+00
7467	53	2022-03-28 12:17:32.566268+00	2022-03-28 12:17:32.566292+00
7468	53	2022-03-28 12:17:32.571939+00	2022-03-28 12:17:32.571965+00
7469	53	2022-03-28 12:17:32.576286+00	2022-03-28 12:17:32.576308+00
7470	53	2022-03-28 12:17:32.581535+00	2022-03-28 12:17:32.581563+00
7471	53	2022-03-28 12:17:32.587762+00	2022-03-28 12:17:32.58779+00
7472	53	2022-03-28 12:17:32.592247+00	2022-03-28 12:17:32.592268+00
7473	53	2022-03-28 12:17:32.596494+00	2022-03-28 12:17:32.596517+00
7474	53	2022-03-28 12:17:32.602637+00	2022-03-28 12:17:32.602709+00
7475	53	2022-03-28 12:17:32.608027+00	2022-03-28 12:17:32.608049+00
7476	53	2022-03-28 12:17:32.612312+00	2022-03-28 12:17:32.612335+00
7477	53	2022-03-28 12:17:32.618044+00	2022-03-28 12:17:32.618093+00
7478	53	2022-03-28 12:17:32.623934+00	2022-03-28 12:17:32.62396+00
7479	53	2022-03-28 12:17:32.628346+00	2022-03-28 12:17:32.62837+00
7480	53	2022-03-28 12:17:32.633719+00	2022-03-28 12:17:32.633758+00
7481	53	2022-03-28 12:17:32.640087+00	2022-03-28 12:17:32.640118+00
7482	53	2022-03-28 12:17:32.644555+00	2022-03-28 12:17:32.644576+00
7483	53	2022-03-28 12:17:32.648956+00	2022-03-28 12:17:32.648978+00
7484	53	2022-03-28 12:17:32.655049+00	2022-03-28 12:17:32.655089+00
7485	53	2022-03-28 12:17:32.660292+00	2022-03-28 12:17:32.660314+00
7486	53	2022-03-28 12:17:32.664573+00	2022-03-28 12:17:32.664596+00
7487	53	2022-03-28 12:17:32.669521+00	2022-03-28 12:17:32.669556+00
7488	53	2022-03-28 12:17:32.675451+00	2022-03-28 12:17:32.67548+00
7489	53	2022-03-28 12:17:32.680509+00	2022-03-28 12:17:32.680565+00
7490	53	2022-03-28 12:17:32.689418+00	2022-03-28 12:17:32.689496+00
7491	53	2022-03-28 12:17:32.695791+00	2022-03-28 12:17:32.695825+00
7492	53	2022-03-28 12:17:32.701139+00	2022-03-28 12:17:32.701175+00
7493	53	2022-03-28 12:17:32.707674+00	2022-03-28 12:17:32.707715+00
7494	53	2022-03-28 12:17:32.713263+00	2022-03-28 12:17:32.7133+00
7495	53	2022-03-28 12:17:32.720889+00	2022-03-28 12:17:32.720927+00
7496	53	2022-03-28 12:17:32.726936+00	2022-03-28 12:17:32.726971+00
7497	53	2022-03-28 12:17:32.732986+00	2022-03-28 12:17:32.733051+00
7498	53	2022-03-28 12:17:32.740663+00	2022-03-28 12:17:32.740696+00
7499	53	2022-03-28 12:17:32.745266+00	2022-03-28 12:17:32.745295+00
7500	53	2022-03-28 12:17:32.751247+00	2022-03-28 12:17:32.751292+00
7501	53	2022-03-28 12:17:32.757607+00	2022-03-28 12:17:32.757638+00
7502	53	2022-03-28 12:17:32.762217+00	2022-03-28 12:17:32.762246+00
7503	53	2022-03-28 12:17:32.767517+00	2022-03-28 12:17:32.767563+00
7504	53	2022-03-28 12:17:32.773196+00	2022-03-28 12:17:32.773223+00
7505	53	2022-03-28 12:17:32.777939+00	2022-03-28 12:17:32.777982+00
7506	53	2022-03-28 12:17:32.78453+00	2022-03-28 12:17:32.784573+00
7507	53	2022-03-28 12:17:32.79061+00	2022-03-28 12:17:32.790631+00
7508	53	2022-03-28 12:17:32.794531+00	2022-03-28 12:17:32.794551+00
7509	53	2022-03-28 12:17:32.799688+00	2022-03-28 12:17:32.799734+00
7510	53	2022-03-28 12:17:32.806131+00	2022-03-28 12:17:32.806163+00
7511	53	2022-03-28 12:17:32.810749+00	2022-03-28 12:17:32.81077+00
7512	53	2022-03-28 12:17:32.815093+00	2022-03-28 12:17:32.815115+00
7513	53	2022-03-28 12:17:32.821287+00	2022-03-28 12:17:32.821325+00
7514	53	2022-03-28 12:17:32.826763+00	2022-03-28 12:17:32.826786+00
7515	53	2022-03-28 12:17:32.830717+00	2022-03-28 12:17:32.830737+00
7516	53	2022-03-28 12:17:32.835866+00	2022-03-28 12:17:32.835905+00
7517	53	2022-03-28 12:17:32.842472+00	2022-03-28 12:17:32.842497+00
7518	53	2022-03-28 12:17:32.846889+00	2022-03-28 12:17:32.846909+00
7519	53	2022-03-28 12:17:32.851073+00	2022-03-28 12:17:32.851093+00
7520	53	2022-03-28 12:17:32.857351+00	2022-03-28 12:17:32.857391+00
7521	53	2022-03-28 12:17:32.862843+00	2022-03-28 12:17:32.862865+00
7522	53	2022-03-28 12:17:32.866703+00	2022-03-28 12:17:32.866723+00
7523	53	2022-03-28 12:17:32.871912+00	2022-03-28 12:17:32.871955+00
7524	53	2022-03-28 12:17:32.878036+00	2022-03-28 12:17:32.87807+00
7525	53	2022-03-28 12:17:32.882491+00	2022-03-28 12:17:32.88251+00
7526	53	2022-03-28 12:17:32.886797+00	2022-03-28 12:17:32.886852+00
7527	53	2022-03-28 12:17:32.893716+00	2022-03-28 12:17:32.893763+00
7528	53	2022-03-28 12:17:32.89964+00	2022-03-28 12:17:32.899674+00
7529	53	2022-03-28 12:17:32.904148+00	2022-03-28 12:17:32.904173+00
7530	53	2022-03-28 12:17:32.909161+00	2022-03-28 12:17:32.909189+00
7531	53	2022-03-28 12:17:32.91525+00	2022-03-28 12:17:32.915282+00
7532	53	2022-03-28 12:17:32.919781+00	2022-03-28 12:17:32.919801+00
7533	53	2022-03-28 12:17:32.924097+00	2022-03-28 12:17:32.924117+00
7534	53	2022-03-28 12:17:32.929922+00	2022-03-28 12:17:32.929963+00
7535	53	2022-03-28 12:17:32.935222+00	2022-03-28 12:17:32.935242+00
7536	53	2022-03-28 12:17:32.939885+00	2022-03-28 12:17:32.939916+00
7537	53	2022-03-28 12:17:32.946288+00	2022-03-28 12:17:32.946333+00
7538	53	2022-03-28 12:17:32.952119+00	2022-03-28 12:17:32.952149+00
7539	53	2022-03-28 12:17:32.957155+00	2022-03-28 12:17:32.957188+00
7540	53	2022-03-28 12:17:32.964007+00	2022-03-28 12:17:32.964048+00
7541	53	2022-03-28 12:17:32.969975+00	2022-03-28 12:17:32.970006+00
7542	53	2022-03-28 12:17:32.975367+00	2022-03-28 12:17:32.975387+00
7543	53	2022-03-28 12:17:32.981097+00	2022-03-28 12:17:32.981141+00
7544	53	2022-03-28 12:17:32.986841+00	2022-03-28 12:17:32.986862+00
\.


--
-- Data for Name: register_plantvarietyname; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.register_plantvarietyname (id, name, variety_id, change_date) FROM stdin;
9811	Achille	6719	2022-03-01
9812	Adone	6720	2022-03-01
9813	Adret	6721	2022-03-01
9814	Aegeon	6722	2022-03-01
9815	Afar	6723	2022-03-01
9816	Aguirre	6724	2022-03-01
9817	Aiace	6725	2022-03-01
9818	Akitakomachi	6726	2022-03-01
9819	Albatros	6727	2022-03-01
9820	Albufera	6728	2022-03-01
9821	Alena	6729	2022-03-01
9822	Aleramo	6730	2022-03-01
9823	Alice	6731	2022-03-01
9824	Alpe	6732	2022-03-01
9825	Ambra	6733	2022-03-01
9826	Andolla	6734	2022-03-01
9827	Antares	6735	2022-03-01
9828	Apollo	6736	2022-03-01
9829	Arborio	6737	2022-03-01
9830	Arcadia	6738	2022-03-01
9831	Arco	6739	2022-03-01
9832	Ares	6740	2022-03-01
9833	Argo	6741	2022-03-01
9834	Ariete	6742	2022-03-01
9835	Aristotele	6743	2022-03-01
9836	Arpa	6744	2022-03-01
9837	Arsenal	6745	2022-03-01
9838	Artemide	6746	2022-03-01
9839	Artiglio	6747	2022-03-01
9840	Asia	6748	2022-03-01
9841	Asso	6749	2022-03-01
9842	Astro	6750	2022-03-01
9843	Atene	6751	2022-03-01
9844	Atlantis	6752	2022-03-01
9845	Augusto	6753	2022-03-01
9846	Aurelia	6754	2022-03-01
9847	Axios	6755	2022-03-01
9848	Aychade	6756	2022-03-01
9849	Bacco	6757	2022-03-01
9850	Bahia	6758	2022-03-01
9851	Baixet	6759	2022-03-01
9852	Baldo	6760	2022-03-01
9853	Balilla	6761	2022-03-01
9854	Balilla X Sollana	6762	2022-03-01
9855	Barcarin	6763	2022-03-01
9856	Bendret	6764	2022-03-01
9857	Benisants	6765	2022-03-01
9858	Bianca	6766	2022-03-01
9859	Bomba	6767	2022-03-01
9860	Bombonet	6768	2022-03-01
9861	Bravo	6769	2022-03-01
9862	Brio	6770	2022-03-01
9863	BS1	6771	2022-03-01
9864	Cadet	6772	2022-03-01
9865	Cala	6773	2022-03-01
9866	Calca	6774	2022-03-01
9867	Calipso	6775	2022-03-01
9868	Carmen	6776	2022-03-01
9869	Carmen (Es)	6777	2022-03-01
9870	Carnaroli	6778	2022-03-01
9871	Carnise	6779	2022-03-01
9872	Carnise Precoce	6780	2022-03-01
9873	Castells	6781	2022-03-01
9874	Castelmochi	6782	2022-03-01
9875	Centauro	6783	2022-03-01
9876	Cerere	6784	2022-03-01
9877	Cervo	6785	2022-03-01
9878	Cesare	6786	2022-03-01
9879	Chimera	6787	2022-03-01
9880	Cigalon	6788	2022-03-01
9881	CL26	6789	2022-03-01
9882	CL71	6790	2022-03-01
9883	CL8825	6791	2022-03-01
9884	Clavel	6792	2022-03-01
9885	CLXL745	6793	2022-03-01
9886	Cobra	6794	2022-03-01
9887	Coco	6795	2022-03-01
9888	Condor	6796	2022-03-01
9889	Corbetta	6797	2022-03-01
9890	Cormoran	6798	2022-03-01
9891	Cosmic	6799	2022-03-01
9892	Creso	6800	2022-03-01
9893	Cripto	6801	2022-03-01
9894	CRLB1	6802	2022-03-01
9895	Crono	6803	2022-03-01
9896	CRW3	6804	2022-03-01
9897	Dardo	6805	2022-03-01
9898	Dedalo	6806	2022-03-01
9899	Delfino	6807	2022-03-01
9900	Delmar	6808	2022-03-01
9901	Delta	6809	2022-03-01
9902	Deneb	6810	2022-03-01
9903	Dimitra	6811	2022-03-01
9904	Dion	6812	2022-03-01
9905	Donana	6813	2022-03-01
9906	Drago	6814	2022-03-01
9907	Ducato	6815	2022-03-01
9908	Dunarea	6816	2022-03-01
9909	Ebro	6817	2022-03-01
9910	Elba	6818	2022-03-01
9911	Elida	6819	2022-03-01
9912	Elio	6820	2022-03-01
9913	Ellebi	6821	2022-03-01
9914	Eolo	6822	2022-03-01
9915	Ercole	6823	2022-03-01
9916	Eridano	6824	2022-03-01
9917	Europa	6825	2022-03-01
9918	Eurosis	6826	2022-03-01
9919	Evropi	6827	2022-03-01
9920	Fanga	6828	2022-03-01
9921	Fani	6829	2022-03-01
9922	Fast	6830	2022-03-01
9923	Fenis	6831	2022-03-01
9924	Fidji	6832	2022-03-01
9925	Filira	6833	2022-03-01
9926	Flipper	6834	2022-03-01
9927	Fonsa	6835	2022-03-01
9928	Fragrance	6836	2022-03-01
9929	Fulgente-Iro	6837	2022-03-01
9930	Galatxo	6838	2022-03-01
9931	Galileo	6839	2022-03-01
9932	Gallis	6840	2022-03-01
9933	Galo	6841	2022-03-01
9934	Gange	6842	2022-03-01
9935	Garda	6843	2022-03-01
9936	Gavina	6844	2022-03-01
9937	Gemini	6845	2022-03-01
9938	Genio	6846	2022-03-01
9939	Giada	6847	2022-03-01
9940	Giano	6848	2022-03-01
9941	Gigante Vercelli	6849	2022-03-01
9942	Giglio	6850	2022-03-01
9943	Giove	6851	2022-03-01
9944	Gladio	6852	2022-03-01
9945	Gleva	6853	2022-03-01
9946	Gloria	6854	2022-03-01
9947	Golden	6855	2022-03-01
9948	Graldo	6856	2022-03-01
9949	Greppi	6857	2022-03-01
9950	Guadiamar	6858	2022-03-01
9951	Guara	6859	2022-03-01
9952	Guixel	6860	2022-03-01
9953	Hidalgo	6861	2022-03-01
9954	Hispagrain	6862	2022-03-01
9955	Ibis	6863	2022-03-01
9956	Ilda	6864	2022-03-01
9957	IR64	6865	2022-03-01
9958	Ispaniki A	6866	2022-03-01
9959	Italmochi	6867	2022-03-01
9960	J Sendra	6868	2022-03-01
9961	Jacinto	6869	2022-03-01
9962	Jefferson	6870	2022-03-01
9963	Kalliston	6871	2022-03-01
9964	Karnak	6872	2022-03-01
9965	King	6873	2022-03-01
9966	Kir	6874	2022-03-01
9967	Koral	6875	2022-03-01
9968	Lady Wright	6876	2022-03-01
9969	Lamone	6877	2022-03-01
9970	Lampo	6878	2022-03-01
9972	Libero	6880	2022-03-01
9973	Libra	6881	2022-03-01
9974	Lido	6882	2022-03-01
9975	Lince	6883	2022-03-01
9976	Lomellino	6884	2022-03-01
9977	Loto	6885	2022-03-01
9978	Lucero	6886	2022-03-01
9979	Luna Cl	6887	2022-03-01
9980	Luxor	6888	2022-03-01
9981	Magic	6889	2022-03-01
9982	Makedonia	6890	2022-03-01
9983	Mantova	6891	2022-03-01
9984	Mar	6892	2022-03-01
9985	Maratelli	6893	2022-03-01
9986	Mare Cl	6894	2022-03-01
9987	Marisma	6895	2022-03-01
9988	Marte	6896	2022-03-01
9989	Maso	6897	2022-03-01
9990	Mercurio	6898	2022-03-01
9991	Minima	6899	2022-03-01
9992	Mistik	6900	2022-03-01
9993	Mistral	6901	2022-03-01
9994	Miura	6902	2022-03-01
9995	Miziya	6903	2022-03-01
9996	Molo	6904	2022-03-01
9997	Monticelli	6905	2022-03-01
9998	Montsianell	6906	2022-03-01
9999	Musa	6907	2022-03-01
10000	Nembo	6908	2022-03-01
10001	Nerone	6909	2022-03-01
10002	Niki	6910	2022-03-01
10003	Niva	6911	2022-03-01
10004	Novara	6912	2022-03-01
10005	Nuovo Maratelli	6913	2022-03-01
10006	Okura	6914	2022-03-01
10007	Olympiada	6915	2022-03-01
10008	Onice	6916	2022-03-01
10009	Opale	6917	2022-03-01
10010	Orellana	6918	2022-03-01
10011	Chinese Originario	6919	2022-03-01
10012	Orione	6920	2022-03-01
10013	Ostiglia	6921	2022-03-01
10014	Panda	6922	2022-03-01
10015	Pegaso	6923	2022-03-01
10016	Perla	6924	2022-03-01
10017	Perla Rosso	6925	2022-03-01
10018	Perseo	6926	2022-03-01
10019	Piemonte	6927	2022-03-01
10020	Pierrot	6928	2022-03-01
10021	Pi'ana	6929	2022-03-01
10022	Polizesti 28	6930	2022-03-01
10023	Poseidone	6931	2022-03-01
10024	Primo	6932	2022-03-01
10025	Prometeo	6933	2022-03-01
10026	Puebla	6934	2022-03-01
10027	Puma	6935	2022-03-01
10028	Puntal	6936	2022-03-01
10029	Razza77	6937	2022-03-01
10030	Rea	6938	2022-03-01
10031	Redi	6939	2022-03-01
10032	Ribe	6940	2022-03-01
10033	Ribe (Euribe)	6941	2022-03-01
10034	Rinaldo Bersani	6942	2022-03-01
10035	Ringo	6943	2022-03-01
10036	Ripallo	6944	2022-03-01
10037	Rodeo	6945	2022-03-01
10038	Roma	6946	2022-03-01
10039	Rombo	6947	2022-03-01
10040	Romolo	6948	2022-03-01
10041	Ronaldo	6949	2022-03-01
10042	Rosa Marchetti	6950	2022-03-01
10043	Roxani	6951	2022-03-01
10044	RTID3854	6952	2022-03-01
10045	RTID3858	6953	2022-03-01
10046	Ruille	6954	2022-03-01
10047	S. Andrea	6955	2022-03-01
10048	Salvo	6956	2022-03-01
10049	Samba	6957	2022-03-01
10050	Sambuc	6958	2022-03-01
10051	Sancio P6	6959	2022-03-01
10052	Santerno	6960	2022-03-01
10053	Sara	6961	2022-03-01
10054	Sarcet	6962	2022-03-01
10055	Saturno	6963	2022-03-01
10056	Savio	6964	2022-03-01
10057	Scirocco	6965	2022-03-01
10058	Scudo	6966	2022-03-01
10059	Sedora	6967	2022-03-01
10060	Selenio	6968	2022-03-01
10061	Senia	6969	2022-03-01
10062	Sereno	6970	2022-03-01
10063	Sesiamochi	6971	2022-03-01
10064	Silla	6972	2022-03-01
10065	Sillaro	6973	2022-03-01
10066	Sirbal	6974	2022-03-01
10067	Sirio Cl	6975	2022-03-01
10068	Sirmione	6976	2022-03-01
10069	SISR215	6977	2022-03-01
10070	Sivert	6978	2022-03-01
10071	Smeraldo	6979	2022-03-01
10072	Sole Cl	6980	2022-03-01
10073	Soulanet	6981	2022-03-01
10074	Sp55	6982	2022-03-01
10075	Sp601	6983	2022-03-01
10076	Sp602	6984	2022-03-01
10077	Spina	6985	2022-03-01
10078	Sprint	6986	2022-03-01
10079	Stresa	6987	2022-03-01
10080	Strymonas	6988	2022-03-01
10081	Susan	6989	2022-03-01
10082	SYCR 128	6990	2022-03-01
10083	SYCR 72	6991	2022-03-01
10084	SYCR 73	6992	2022-03-01
10085	SYCR 85	6993	2022-03-01
10086	SYCR 86	6994	2022-03-01
10087	SYCR 90	6995	2022-03-01
10088	Tamarin	6996	2022-03-01
10089	Tarriso	6997	2022-03-01
10090	Tea	6998	2022-03-01
10091	Tebre	6999	2022-03-01
10092	Tejo	7000	2022-03-01
10093	Teqing	7001	2022-03-01
10094	Thaibonnet	7002	2022-03-01
10095	Thainato	7003	2022-03-01
10096	Thaiperla	7004	2022-03-01
10097	Titanio	7005	2022-03-01
10098	Tosca	7006	2022-03-01
10099	Ulisse	7007	2022-03-01
10100	Ullal	7008	2022-03-01
10101	Urano	7009	2022-03-01
10102	Vega	7010	2022-03-01
10103	Venere	7011	2022-03-01
10104	Veneria	7012	2022-03-01
10105	Veta	7013	2022-03-01
10106	Vialone 190	7014	2022-03-01
10107	Vialone Nano	7015	2022-03-01
10108	Virgo	7016	2022-03-01
10109	Volano	7017	2022-03-01
10110	Vulcano	7018	2022-03-01
10111	Yume	7019	2022-03-01
10112	Zefir	7020	2022-03-01
10113	Zena	7021	2022-03-01
10114	Zeus	7022	2022-03-01
10115	Tramonto	7023	2022-03-01
10116	Krystallino	7024	2022-03-01
10117	Presen	7025	2022-03-01
10118	Strella	7026	2022-03-01
10119	Top	7027	2022-03-01
10120	Valzer	7028	2022-03-01
10121	Riva	7029	2022-03-01
10122	Bali	7030	2022-03-01
10123	Tanaro	7031	2022-03-01
10124	Radon	7032	2022-03-01
10125	Oscar	7033	2022-03-01
10126	Nebbione	7034	2022-03-01
10127	Orta	7035	2022-03-01
10128	Mida	7036	2022-03-01
10129	Icaro	7037	2022-03-01
10130	Diana	7038	2022-03-01
10131	CRT2	7039	2022-03-01
10132	Bastia	7040	2022-03-01
10133	Artico	7041	2022-03-01
10134	Arona	7042	2022-03-01
10135	Acquario	7043	2022-03-01
10136	Adelio	7044	2022-03-01
10137	Albada	7045	2022-03-01
10138	Betis	7046	2022-03-01
10139	Archimede	7047	2022-03-01
10140	Filippo	7048	2022-03-01
10141	Perfum	7049	2022-03-01
10142	Ricastello	7050	2022-03-01
10143	Festa	7051	2022-03-01
10144	Skybonnet	7052	2022-03-01
10145	Lemont	7053	2022-03-01
10146	Jucar	7054	2022-03-01
10147	Helene	7055	2022-03-01
10148	Clot	7056	2022-03-01
10149	Arborio Precoce	7057	2022-03-01
10150	Armonia	7058	2022-03-01
10151	Dorella	7059	2022-03-01
10152	Elvo	7060	2022-03-01
10153	Ghibli	7061	2022-03-01
10154	Gigante	7062	2022-03-01
10155	Idra	7063	2022-03-01
10156	Medusa	7064	2022-03-01
10157	Minerva	7065	2022-03-01
10158	Romeo	7066	2022-03-01
10159	Otello	7067	2022-03-01
10160	Pony	7068	2022-03-01
10161	Prezioso	7069	2022-03-01
10162	Roncolo	7070	2022-03-01
10163	Onda	7071	2022-03-01
10164	Oceano	7072	2022-03-01
10165	Agata	7073	2022-03-01
10166	Iarim	7074	2022-03-01
10167	Teseo	7075	2022-03-01
10168	Sfera	7076	2022-03-01
10169	Presto	7077	2022-03-01
10170	Ninfa	7078	2022-03-01
10171	Meco	7079	2022-03-01
10172	Fedra	7080	2022-03-01
10173	Febo	7081	2022-03-01
10174	Falco	7082	2022-03-01
10175	Elettra	7083	2022-03-01
10176	CL 80	7084	2022-03-01
10177	CL 46	7085	2022-03-01
10178	CL12	7086	2022-03-01
10179	Centro	7087	2022-03-01
10180	Koala	7088	2022-03-01
10181	Agave	7089	2022-03-01
10182	Adelaide Chiappelli	7090	2022-03-01
10183	Agostano	7091	2022-03-01
10184	Agusta	7092	2022-03-01
10185	Airone	7093	2022-03-01
10186	Allorio	7094	2022-03-01
10187	Americano 1600	7095	2022-03-01
10188	Anseatico	7096	2022-03-01
10189	Ardizzone	7097	2022-03-01
10190	Auro	7098	2022-03-01
10191	Aurora	7099	2022-03-01
10192	Avalya	7100	2022-03-01
10193	Balilla Gg	7101	2022-03-01
10194	Balocco	7102	2022-03-01
10195	Balzaretti	7103	2022-03-01
10196	Baraggia	7104	2022-03-01
10197	Bellardone	7105	2022-03-01
10198	Benito	7106	2022-03-01
10199	Bertone	7107	2022-03-01
10200	Bogdan	7108	2022-03-01
10201	Bonni	7109	2022-03-01
10202	Calliope	7110	2022-03-01
10203	Calmochi 101	7111	2022-03-01
10204	Cammeo	7112	2022-03-01
10205	Caravaggio	7113	2022-03-01
10206	Cassiopea	7114	2022-03-01
10207	Castello	7115	2022-03-01
10208	Castore	7116	2022-03-01
10209	Catullo	7117	2022-03-01
10210	Cellini	7118	2022-03-01
10211	A201	7119	2022-03-01
10212	Cistella	7120	2022-03-01
10213	Cleopatra	7121	2022-03-01
10214	Corimbo	7122	2022-03-01
10215	Dellrose	7123	2022-03-01
10216	Demetra	7124	2022-03-01
10217	Dunav	7125	2022-03-01
10218	ECCO 63	7126	2022-03-01
10219	Emma	7127	2022-03-01
10220	Ermes	7128	2022-03-01
10221	Espidio	7129	2022-03-01
10222	Brezza	7130	2022-03-01
10223	Fado	7131	2022-03-01
10224	Faro	7132	2022-03-01
10225	Fenice	7133	2022-03-01
10226	Feronio	7134	2022-03-01
10227	Ferraris	7135	2022-03-01
10228	Fortuna	7136	2022-03-01
10229	Gageron	7137	2022-03-01
10230	Giovanni Marchetti	7138	2022-03-01
10231	Greggio	7139	2022-03-01
10232	Gritna	7140	2022-03-01
10233	Guadiagran	7141	2022-03-01
10234	Ice	7142	2022-03-01
10235	Indio	7143	2022-03-01
10236	Irgr Dani	7144	2022-03-01
10237	Irgr Viki	7145	2022-03-01
10238	Iskra	7146	2022-03-01
10239	Italico	7147	2022-03-01
10240	Italico Livorno	7148	2022-03-01
10241	Italpatna 48	7149	2022-03-01
10242	Keope	7150	2022-03-01
10243	Korostaj 333	7151	2022-03-01
10244	La Ferla	7152	2022-03-01
10245	Lencino	7153	2022-03-01
10246	Lieto	7154	2022-03-01
10247	LMPB	7155	2022-03-01
10248	Lomello	7156	2022-03-01
10249	M 225	7157	2022-03-01
10250	M 488	7158	2022-03-01
10251	M 60	7159	2022-03-01
10252	Mariana	7160	2022-03-01
10253	Medea	7161	2022-03-01
10254	Merle	7162	2022-03-01
10255	Molinella	7163	2022-03-01
10256	Navile	7164	2022-03-01
10257	Nemesi Cl	7165	2022-03-01
10258	Neretto	7166	2022-03-01
10259	Nero	7167	2022-03-01
10260	Neve	7168	2022-03-01
10261	Nova	7169	2022-03-01
10262	Olcenengo	7170	2022-03-01
10263	Oldenico	7171	2022-03-01
10264	Orion	7172	2022-03-01
10265	Orione (Storico)	7173	2022-03-01
10266	Oryzella	7174	2022-03-01
10267	Pecos	7175	2022-03-01
10268	Petronio	7176	2022-03-01
10269	Polluce Cl	7177	2022-03-01
10270	Precoce Monticelli	7178	2022-03-01
10271	Prostor	7179	2022-03-01
10272	Proteo	7180	2022-03-01
10273	Raffaello	7181	2022-03-01
10274	Ranghino	7182	2022-03-01
10275	Rialto	7183	2022-03-01
10276	Ribello	7184	2022-03-01
10277	Ringola	7185	2022-03-01
10278	Rizzotto	7186	2022-03-01
10279	Rocca	7187	2022-03-01
10280	Romanico	7188	2022-03-01
10281	Roncarolo	7189	2022-03-01
10282	Rova	7190	2022-03-01
10283	Rubino	7191	2022-03-01
10284	S.Pietro	7192	2022-03-01
10285	S.Rocco	7193	2022-03-01
10286	Senatore Novelli	7194	2022-03-01
10287	Sesila	7195	2022-03-01
10288	Sirion	7196	2022-03-01
10289	Sorriso	7197	2022-03-01
10290	Teti	7198	2022-03-01
10291	Torio	7199	2022-03-01
10292	Trionfo Fassone	7200	2022-03-01
10293	Vasco	7201	2022-03-01
10294	Vento	7202	2022-03-01
10295	Vialone Nero	7203	2022-03-01
10296	Vitro	7204	2022-03-01
10297	Wang	7205	2022-03-01
10298	Zhen Sha	7206	2022-03-01
10299	Sagittario	7207	2022-03-01
10300	Dixiebelle	7208	2022-03-01
10301	Giza 177	7209	2022-03-01
10302	Rodio	7210	2022-03-01
10303	Insubria	7211	2022-03-01
10304	Leonidas CL	7212	2022-03-01
10305	Ardea	7213	2022-03-01
10306	Iride CL	7214	2022-03-01
10307	Arianna CL	7215	2022-03-01
10308	Karmina	7216	2022-03-01
10309	Risabell	7217	2022-03-01
10310	Sandora	7218	2022-03-01
10311	Qm 1003	7219	2022-03-01
10312	Janka	7220	2022-03-01
10313	Marquesa	7221	2022-03-01
10314	Fruzsinam	7222	2022-03-01
10315	Hispamar	7223	2022-03-01
10316	Dma	7224	2022-03-01
10317	Bioryza H	7225	2022-03-01
10318	Kolorado	7226	2022-03-01
10319	Barone CL	7227	2022-03-01
10320	Unico	7228	2022-03-01
10321	Furia CL	7229	2022-03-01
10322	Galassia	7230	2022-03-01
10323	Generale	7231	2022-03-01
10324	Lagostino	7232	2022-03-01
10325	Megumi	7233	2022-03-01
10326	Mirko	7234	2022-03-01
10327	Pato	7235	2022-03-01
10328	Risrus	7236	2022-03-01
10329	Terra CL	7237	2022-03-01
10330	ECCO 51 CL	7238	2022-03-01
10331	ECCO 61	7239	2022-03-01
10332	LT 155	7240	2022-03-01
10333	RTID4355	7241	2022-03-01
10334	RTID4631	7242	2022-03-01
10335	RTID4639	7243	2022-03-01
10336	CL31	7244	2022-03-01
10337	CL15	7245	2022-03-01
10338	Egeo CL	7246	2022-03-01
10339	David CL	7247	2022-03-01
10340	Vaccares	7248	2022-03-01
10341	Tam Tam	7249	2022-03-01
10342	Spada	7250	2022-03-01
10343	Kirkpinar	7251	2022-03-01
10344	Norma	7252	2022-03-01
10345	Halibey	7253	2022-03-01
10346	Balgarka	7254	2022-03-01
10347	Milkana	7255	2022-03-01
10348	Gala	7256	2022-03-01
10349	Sommo	7257	2022-03-01
10350	Riet	7258	2022-03-01
10351	Montell	7259	2022-03-01
10352	Mata	7260	2022-03-01
10353	Fanicris	7261	2022-03-01
10354	Carlet	7262	2022-03-01
10355	RG200	7263	2022-03-01
10356	Dante	7264	2022-03-01
10357	Allegro	7265	2022-03-01
10358	Ribaldo	7266	2022-03-01
10359	Carnaval	7267	2022-03-01
10360	Casanova	7268	2022-03-01
10361	CL111	7269	2022-03-01
10362	CL261	7270	2022-03-01
10363	Ghiaccio	7271	2022-03-01
10364	Reperso	7272	2022-03-01
10365	Il Cardinale	7273	2022-03-01
10366	Aniride	7274	2022-03-01
10367	Nero Beppino	7275	2022-03-01
10368	Ariosto CL	7276	2022-03-01
10369	RTID3547	7277	2022-03-01
10370	Verel	7278	2022-03-01
10371	BVT01	7279	2022-03-01
10372	Mirai	7280	2022-03-01
10373	CL33	7281	2022-03-01
10374	CL28	7282	2022-03-01
10375	Felix	7283	2022-03-01
10376	Anteo	7284	2022-03-01
10377	Telemaco	7285	2022-03-01
10378	Leonardo	7286	2022-03-01
10379	Apache Red	7287	2022-03-01
10380	RG201	7288	2022-03-01
10381	RG202	7289	2022-03-01
10382	Ametist	7290	2022-03-01
10383	Fiamma	7291	2022-03-01
10384	Fuoco	7292	2022-03-01
10385	Marchese CL	7293	2022-03-01
10386	Sapi-GV	7294	2022-03-01
10387	Macchiavelli	7295	2022-03-01
10388	Gelso	7296	2022-03-01
10389	Sanluca	7297	2022-03-01
10390	Gilda	7298	2022-03-01
10391	CRR	7299	2022-03-01
10392	Manuela	7300	2022-03-01
10393	Albaron	7301	2022-03-01
10394	Impuls	7302	2022-03-01
10395	Orange Nori	7303	2022-03-01
10396	Violet Nori	7304	2022-03-01
10397	Osmancik 97	7305	2022-03-01
10398	XL 723	7306	2022-03-01
10399	Gavella	7307	2022-03-01
10400	Gines	7308	2022-03-01
10401	Cirene	7309	2022-03-01
10402	Damyan	7310	2022-03-01
10403	Argila	7311	2022-03-01
10404	Bolero	7312	2022-03-01
10405	Antara	7313	2022-03-01
10406	Il Moro	7314	2022-03-01
10407	Pierrot (Stocchi)	7315	2022-03-01
10408	Kemet	7316	2022-03-01
10409	Keris	7317	2022-03-01
10410	Illeta	7318	2022-03-01
10411	Lirio	7319	2022-03-01
10412	Soto	7320	2022-03-01
10413	Estany	7321	2022-03-01
10414	Zorba	7322	2022-03-01
10415	Golden bon	7323	2022-03-01
10416	Fenomeno	7324	2022-03-01
10417	Lord	7325	2022-03-01
10418	Spillo	7326	2022-03-01
10419	Limperatore	7327	2022-03-01
10420	Precocissimo molina	7328	2022-03-01
10421	Caban	7329	2022-03-01
10422	Prever	7330	2022-03-01
10423	Cambon	7331	2022-03-01
10424	Manobi	7332	2022-03-01
10425	Rousty	7333	2022-03-01
10426	Tiber	7334	2022-03-01
10427	Fleixa	7335	2022-03-01
10428	Paty	7336	2022-03-01
10429	Riege	7337	2022-03-01
10430	Valente	7338	2022-03-01
10431	CL388	7339	2022-03-01
10432	CLA01	7340	2022-03-01
10433	Delfo	7341	2022-03-01
10434	Inov CL	7342	2022-03-01
10435	Nerone Gold	7343	2022-03-01
10436	Re CL	7344	2022-03-01
10437	Regina Sa.Pi.Se.	7345	2022-03-01
10438	RTID4706	7346	2022-03-01
10439	RTID6121	7347	2022-03-01
10440	RTID6118	7348	2022-03-01
10441	Samurai	7349	2022-03-01
10442	Suami	7350	2022-03-01
10443	Kori	7351	2022-03-01
10444	CL35	7352	2022-03-01
10445	PVL024	7353	2022-03-01
10446	CL510	7354	2022-03-01
10447	Tiberio	7355	2022-03-01
10448	Laser	7356	2022-03-01
10449	Nairobi One	7357	2022-03-01
10450	Real	7358	2022-03-01
10451	Zar	7359	2022-03-01
10452	Avana Gold	7360	2022-03-01
10453	Meridio	7361	2022-03-01
10454	Maestrale	7362	2022-03-01
10455	RG C1/1/1/2	7363	2022-03-01
10456	Armida Cl	7364	2022-03-01
10457	Levante	7365	2022-03-01
10458	Traiano Cl	7366	2022-03-01
10459	Penelope	7367	2022-03-01
10460	Corsaro	7368	2022-03-01
10461	Karbor	7369	2022-03-01
10462	Precoce Gallina	7370	2022-03-01
10463	Nano	7371	2022-03-01
10464	Dellarolle	7372	2022-03-01
10465	Marjal	7373	2022-03-01
10466	Leda	7374	2022-03-01
10467	Mareny	7375	2022-03-01
10468	Adriano	7376	2022-03-01
10469	PVL01	7377	2022-03-01
10470	IDR 15/38	7378	2022-03-01
10471	TREBON	7379	2022-03-01
10472	Dellarole	7380	2022-03-01
10473	Chinese ostiglia	7381	2022-03-01
10474	PVL136-IT	7382	2022-03-01
10475	ECCO 975FP	7383	2022-03-01
10476	SJKT	7384	2022-03-01
10477	DUILIO	7385	2022-03-01
10478	COLONNELLO	7386	2022-03-01
10479	MASSIMO	7387	2022-03-01
10481	CL18	7389	2022-03-01
10482	Golia	7390	2022-03-01
10483	ROSSO ROSETTA	7391	2022-03-01
10484	BORANDOTTO	7392	2022-03-01
10485	KIKKO	7393	2022-03-01
10486	Solitario	7394	2022-03-01
10488	ECLISSE	7396	2022-03-01
10489	MAMBO	7397	2022-03-01
10490	DELICIA	7398	2022-03-01
10491	PACO	7399	2022-03-01
10492	BOMBOM	7400	2022-03-01
10493	TOLL	7401	2022-03-01
10494	TURBO	7402	2022-03-01
10495	MELAS	7403	2022-03-01
10496	SYN-RI-NRXaR1007	7404	2022-03-01
10497	SYN-RI-NA-9531	7405	2022-03-01
10498	RTF11	7406	2022-03-01
10499	RTM22	7407	2022-03-01
10500	RTM21	7408	2022-03-01
10501	SYN-RI-NB-9531	7409	2022-03-01
10502	RG300	7410	2022-03-01
10503	NEMO	7411	2022-03-01
10504	LUSITANO	7412	2022-03-01
10505	SYN 049	7413	2022-03-01
10506	CLM-2	7414	2022-03-01
10507	CLM-1	7415	2022-03-01
10508	SJKK	7416	2022-03-01
10509	EVEREST	7417	2022-03-01
10510	ECCO 977FP	7418	2022-03-01
10511	ANSAR	7419	2022-03-01
10512	ARODELTA	7420	2022-03-01
10513	Carogran	7421	2022-03-01
10514	COPSEMAR-7	7422	2022-03-01
10515	OLESA	7423	2022-03-01
10516	POTENCIA	7424	2022-03-01
10517	Virgilio	7425	2022-03-01
10518	Jemma	7426	2022-03-01
10519	Bruma	7427	2022-03-01
10520	Marismilla	7428	2022-03-01
10521	Castigliano	7429	2022-03-01
10522	4Ri15/20	7430	2022-03-01
10523	Capo	7431	2022-03-01
10524	Tesla	7432	2022-03-01
10525	SA1905	7433	2022-03-01
10526	SA1904	7434	2022-03-01
10527	RG 13712/1/1/1	7435	2022-03-01
10528	Nerone 2	7436	2022-03-01
10529	GAIA EG	7437	2022-03-01
10530	Andromeda CL	7438	2022-03-01
10531	RTF13	7439	2022-03-01
10532	RTM25	7440	2022-03-01
10533	RTM23	7441	2022-03-01
10534	BSIN19	7442	2022-03-01
10535	ECCO 951FP	7443	2022-03-01
10536	ECCO 985FP	7444	2022-03-01
10537	SA1906	7445	2022-03-01
10538	Ardente EG	7446	2022-03-01
10539	Caroly	7447	2022-03-01
10540	Narciso EG	7448	2022-03-01
10541	Velox	7449	2022-03-01
10542	ECCO 365	7450	2022-03-01
10543	G2215	7451	2022-03-01
10544	BST1	7452	2022-03-01
10545	Dario CL	7453	2022-03-01
10546	BST2	7454	2022-03-01
10547	SA1902	7455	2022-03-01
10548	Misaki	7456	2022-03-01
10549	Edison	7457	2022-03-01
10550	Yari	7458	2022-03-01
10551	Sucro CL	7459	2022-03-01
10552	Regina	7460	2022-03-01
10553	prova	7461	2022-03-01
10554	CL122HP	7462	2022-03-01
10555	CL125HP	7463	2022-03-01
10556	VN28(11)BC14F29F02	7464	2022-03-01
10557	IRES 1117	7465	2022-03-01
10558	IRES 1172	7466	2022-03-01
10559	MZA7	7467	2022-03-01
10560	MZA6	7468	2022-03-01
10561	CL007	7469	2022-03-01
10562	PV226	7470	2022-03-01
10563	PV234	7471	2022-03-01
10564	MZA10	7472	2022-03-01
10565	RG 23913/1/2/2	7473	2022-03-01
10566	MZA9	7474	2022-03-01
10567	MZA2	7475	2022-03-01
10568	MZA4	7476	2022-03-01
10569	MZA8	7477	2022-03-01
10570	MZA3	7478	2022-03-01
10571	Cartesio	7479	2022-03-01
10572	Volta	7480	2022-03-01
10573	VN25(24)BC8F17	7481	2022-03-01
10574	ALEGRE	7482	2022-03-01
10575	BRINCA	7483	2022-03-01
10576	Copsemar 9	7484	2022-03-01
10577	Copsemar 8	7485	2022-03-01
10578	MOLETA	7486	2022-03-01
10579	Sol	7487	2022-03-01
10580	Ceres	7488	2022-03-01
10581	Macarico	7489	2022-03-01
10582	Grifone	7490	2022-03-01
10583	Irene	7491	2022-03-01
10584	Isabela	7492	2022-03-01
10585	Vampair	7493	2022-03-01
10586	DIANA (Portogallo)	7494	2022-03-01
10587	Jolly nero	7495	2022-03-01
10588	Pascal	7496	2022-03-01
10487	Gioiello	7395	2022-03-01
10589	4RI16/167	7497	2022-03-01
10590	LASJKK20	7498	2022-03-01
10591	PV 03-IT	7499	2022-03-01
10592	PV 23-IT	7500	2022-03-01
10593	PV 221 IT	7501	2022-03-01
10594	Naomi	7502	2022-03-01
10595	Zuanshi	7503	2022-03-01
10596	CL712GL	7504	2022-03-01
10597	CL712V	7505	2022-03-01
10598	MZ105	7506	2022-03-01
10599	MZ181	7507	2022-03-01
10600	Billy	7508	2022-03-01
10601	Celtiko	7509	2022-03-01
10602	Chirone	7510	2022-03-01
10603	Circe	7511	2022-03-01
10604	CL44	7512	2022-03-01
10605	CL112	7513	2022-03-01
10606	CL131 HP	7514	2022-03-01
10607	CL145	7515	2022-03-01
10608	Corsa	7516	2022-03-01
10609	Formula PV	7517	2022-03-01
10610	Sibilla	7518	2022-03-01
10611	4ri16/128	7519	2022-03-01
10612	4ri16/170	7520	2022-03-01
10613	4ri17/164	7521	2022-03-01
10614	CL225 HP	7522	2022-03-01
10615	CL228 HP	7523	2022-03-01
10616	Diva PV	7524	2022-03-01
10617	Luce PV	7525	2022-03-01
10618	Eusake01	7526	2022-03-01
10619	Eusake02	7527	2022-03-01
10620	MZA11	7528	2022-03-01
10621	SA2001	7529	2022-03-01
10622	SA2002	7530	2022-03-01
10623	SA2003	7531	2022-03-01
10624	SA2004	7532	2022-03-01
10625	Sunrose PV	7533	2022-03-01
10626	Aivori	7534	2022-03-01
10627	Ebano max	7535	2022-03-01
10628	Enea	7536	2022-03-01
10629	Etrusco	7537	2022-03-01
10630	Fortunato	7538	2022-03-01
10631	Garbell	7539	2022-03-01
10632	Kaldor	7540	2022-03-01
10633	Lluent	7541	2022-03-01
10634	Minosse	7542	2022-03-01
10635	Polizesti 19	7543	2022-03-01
10636	Sofia	7544	2022-03-01
10847	Tolima	7632	2022-03-02
10848	SYNRINB95321	7633	2022-03-02
10849	RTID3856	7634	2022-03-02
10850	Molina	7635	2022-03-02
10851	Marco	7636	2022-03-02
10852	PV1010	7637	2022-03-02
10853	RG17810/1/1/2	7638	2022-03-02
10854	SAPD2101	7639	2022-03-02
10855	RTM24	7640	2022-03-02
10857	RTF15	7642	2022-03-02
10858	Felix 2	7643	2022-03-02
10859	Araldo PV	7644	2022-03-02
10860	Oriente	7645	2022-03-02
10861	CLXL729	7646	2022-03-02
10862	Capitano	7647	2022-03-02
10863	S. Eusebio	7648	2022-03-02
10864	Euro	7649	2022-03-02
10865	A301	7650	2022-03-02
10866	Montebello	7651	2022-03-02
10867	Black Egipt	7652	2022-03-02
10868	Perlato Ferrarese	7653	2022-03-02
10869	Scorpione	7654	2022-03-02
10870	RG9504	7655	2022-03-02
10871	Iseo	7656	2022-03-02
10872	Edirne	7657	2022-03-02
10873	Alexandros	7658	2022-03-02
10874	Dama	7659	2022-03-02
10875	Arelate	7660	2022-03-02
10876	RIOND	7452	2022-03-28
10877	Hispagran	6862	2022-03-28
10878	Copsemar 7	7422	2022-03-28
10879	San Rocco	7193	2022-03-28
10880	Verelé	7278	2022-03-28
10881	Fulgente	6837	2022-03-28
10882	RG300A	7638	2022-03-28
10883	Atena	6751	2022-03-28
10884	RTH17	7443	2021-01-01
10885	RTH33	7450	2021-01-01
10886	RTH27	7444	2021-01-01
10887	Rondolino	7502	2021-01-01
10889	4RI13/53	7432	2021-01-01
10890	4RI15/43	7457	2021-01-01
10891	SA1901	7456	2021-01-01
10892	SA1907	7438	2021-01-01
10893	SA1903	7453	2021-01-01
10894	Brisa	6892	2021-01-01
10895	Italico Roncarolo	7147	2021-01-01
10896	Padano	6758	2021-01-01
10897	RG101	7365	2021-01-01
10898	RG203	7362	2021-01-01
10899	4RI16/97	7480	2021-01-01
10900	4RI16/79	7479	2021-01-01
10901	4RI16/29BIS	7496	2021-01-01
10902	RFH1612284	7383	2021-01-01
10903	RG 36313/1/6/2	7447	2021-01-01
10904	RFH1612282	7418	2021-01-01
10905	Apache-Red	7287	2021-01-01
10906	Tommy	7508	2021-01-01
10907	Originario	6919	2021-01-01
10908	L201	7359	2021-01-01
10909	SYN-RI-20530	7413	2021-01-01
10910	Nero CRA	7652	2021-01-01
10911	Purple Check	7652	2021-01-01
10912	Bestrose	7286	2021-01-01
10913	3C/15	7304	2021-01-01
10914	4C/15	7303	2021-01-01
10915	M-60	7159	2021-01-01
10916	M-488	7158	2021-01-01
10917	JOR 89 CL	7661	2022-03-30
10919	BWO 1047 CL	7663	2022-03-30
10920	BWO 1404 CL	7664	2022-03-30
10480	Omega CL	7388	2022-03-01
9971	Leonardo Gentinetta	6879	2022-03-01
10921	Tigre	7074	2020-04-08
10856	O11(22)BC19F28F05	7641	2022-03-02
10922	PVL080	7665	2022-04-13
10923	38R/16	7665	2016-04-13
\.


--
-- Data for Name: spaces_area; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spaces_area (id, name, length, width, temp_offset, location_id) FROM stdin;
306	va31	21	0.75	0	3
307	va32	22	0.75	0	3
308	va33	24	0.75	0	3
288	sg6	36	0.75	0	3
289	sg7	36	0.75	0	3
313	va39	30	1.2	0	3
314	va41	30	1.2	0	3
316	b2	12	1.2	0	3
317	b4s	12	1	0	3
290	sg8	36	0.75	0	3
291	su1	15	1.2	0	3
292	su2	15	1.2	0	3
293	su3	15	1.2	0	3
294	su4	15	1.2	0	3
295	su5	15	1.2	0	3
296	su6	15	1.2	0	3
297	su7	15	1.2	0	3
298	su8	15	1.2	0	3
299	su9	15	1.2	0	3
302	va27	16	1.2	0	3
321	b8	8	1	0	3
322	b9	13	0.75	0	3
323	b10	13	0.75	0	3
324	b11	13	1	0	3
325	b12	8	0.75	0	3
326	b13	8	0.75	0	3
327	b14	8	0.75	0	3
329	b16s	10	0.75	0	3
330	b17s	10	0.75	0	3
331	b18s	10	0.75	0	3
332	b19s	10	0.75	0	3
267	vb1	18	1.2	0	3
268	vb2s	20	0.75	0	3
269	vb3s	20	0.75	0	3
315	b1	12	1.2	0	3
328	b15s	10	0.75	0	3
275	vb9s	21	1.2	0	4
271	vb5s	20	0.75	0	4
303	va28	18	0.75	0	3
304	va29	19	0.75	0	3
305	va30	20	0.75	0	3
309	va34	26	0.75	0	3
310	va35	27	0.75	0	3
311	va36	28	0.75	0	3
312	va38	29	0.75	0	3
318	b5s	12	1	0	3
319	b6s	12	0.75	0	3
320	b7s	12	1.2	0	3
270	vb4s	20	0.75	0	3
272	vb6s	20	0.75	0	3
273	vb7s	20	0.75	0	3
274	vb8s	21	1.2	0	3
276	vb10s	21	0.75	0	3
277	va1	20	0.75	0	3
278	va2	20	0.75	0	3
279	va3	20	0.75	0	3
280	va4	20	0.75	0	3
281	va5	36	1.2	0	3
282	va6	36	1.2	0	3
283	sg1	36	0.75	0	3
284	sg2	36	0.75	0	3
285	sg3	36	0.75	0	3
286	sg4	36	0.75	0	3
287	sg5	36	0.75	0	3
\.


--
-- Data for Name: spaces_location; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spaces_location (id, name, latitude, longitude) FROM stdin;
3	valle	45	9
4	casa	45	9
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 132, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: calculator_crop_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.calculator_crop_id_seq', 78, true);


--
-- Name: calculator_cropparameter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.calculator_cropparameter_id_seq', 281, true);


--
-- Name: calculator_management_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.calculator_management_id_seq', 12, true);


--
-- Name: calculator_managementtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.calculator_managementtype_id_seq', 2, true);


--
-- Name: collect_cart_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.collect_cart_id_seq', 5, true);


--
-- Name: collect_cartitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.collect_cartitem_id_seq', 83, true);


--
-- Name: collect_germinability_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.collect_germinability_id_seq', 160, true);


--
-- Name: collect_sampleweight_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.collect_sampleweight_id_seq', 6137, true);


--
-- Name: collect_seedsample_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.collect_seedsample_id_seq', 1370, true);


--
-- Name: collect_storage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.collect_storage_id_seq', 564, true);


--
-- Name: collect_storageposition_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.collect_storageposition_id_seq', 7878, true);


--
-- Name: describe_description_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.describe_description_id_seq', 4060, true);


--
-- Name: describe_expression_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.describe_expression_id_seq', 136307, true);


--
-- Name: describe_protocol_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.describe_protocol_id_seq', 7, true);


--
-- Name: describe_state_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.describe_state_id_seq', 876, true);


--
-- Name: describe_trait_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.describe_trait_id_seq', 228, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 32, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 76, true);


--
-- Name: parameters_cropparameter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.parameters_cropparameter_id_seq', 395, true);


--
-- Name: parameters_measure_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.parameters_measure_id_seq', 1, false);


--
-- Name: parameters_parameter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.parameters_parameter_id_seq', 7, true);


--
-- Name: parameters_varietalparameter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.parameters_varietalparameter_id_seq', 1, true);


--
-- Name: register_plantspecies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.register_plantspecies_id_seq', 54, true);


--
-- Name: register_plantvariety_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.register_plantvariety_id_seq', 7666, true);


--
-- Name: register_plantvarietyname_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.register_plantvarietyname_id_seq', 10924, true);


--
-- Name: spaces_area_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.spaces_area_id_seq', 332, true);


--
-- Name: spaces_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.spaces_location_id_seq', 4, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: calculator_crop calculator_crop_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calculator_crop
    ADD CONSTRAINT calculator_crop_pkey PRIMARY KEY (id);


--
-- Name: calculator_cropparameter calculator_cropparameter_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calculator_cropparameter
    ADD CONSTRAINT calculator_cropparameter_pkey PRIMARY KEY (id);


--
-- Name: calculator_management calculator_management_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calculator_management
    ADD CONSTRAINT calculator_management_pkey PRIMARY KEY (id);


--
-- Name: calculator_managementtype calculator_managementtype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calculator_managementtype
    ADD CONSTRAINT calculator_managementtype_pkey PRIMARY KEY (id);


--
-- Name: collect_cart collect_cart_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_cart
    ADD CONSTRAINT collect_cart_pkey PRIMARY KEY (id);


--
-- Name: collect_cartitem collect_cartitem_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_cartitem
    ADD CONSTRAINT collect_cartitem_pkey PRIMARY KEY (id);


--
-- Name: collect_germinability collect_germinability_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_germinability
    ADD CONSTRAINT collect_germinability_pkey PRIMARY KEY (id);


--
-- Name: collect_sampleweight collect_sampleweight_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_sampleweight
    ADD CONSTRAINT collect_sampleweight_pkey PRIMARY KEY (id);


--
-- Name: collect_seedsample collect_seedsample_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_seedsample
    ADD CONSTRAINT collect_seedsample_pkey PRIMARY KEY (id);


--
-- Name: collect_seedsample collect_seedsample_sample_id_4cd71407_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_seedsample
    ADD CONSTRAINT collect_seedsample_sample_id_4cd71407_uniq UNIQUE (sample_id);


--
-- Name: collect_storage collect_storage_name_21377b9a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_storage
    ADD CONSTRAINT collect_storage_name_21377b9a_uniq UNIQUE (name);


--
-- Name: collect_storage collect_storage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_storage
    ADD CONSTRAINT collect_storage_pkey PRIMARY KEY (id);


--
-- Name: collect_storageposition collect_storageposition_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_storageposition
    ADD CONSTRAINT collect_storageposition_pkey PRIMARY KEY (id);


--
-- Name: describe_description describe_description_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.describe_description
    ADD CONSTRAINT describe_description_pkey PRIMARY KEY (id);


--
-- Name: describe_expression describe_expression_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.describe_expression
    ADD CONSTRAINT describe_expression_pkey PRIMARY KEY (id);


--
-- Name: describe_protocol describe_protocol_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.describe_protocol
    ADD CONSTRAINT describe_protocol_pkey PRIMARY KEY (id);


--
-- Name: describe_state describe_state_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.describe_state
    ADD CONSTRAINT describe_state_pkey PRIMARY KEY (id);


--
-- Name: describe_trait describe_trait_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.describe_trait
    ADD CONSTRAINT describe_trait_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: parameters_speciesparameter parameters_cropparameter_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parameters_speciesparameter
    ADD CONSTRAINT parameters_cropparameter_pkey PRIMARY KEY (id);


--
-- Name: parameters_measure parameters_measure_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parameters_measure
    ADD CONSTRAINT parameters_measure_pkey PRIMARY KEY (id);


--
-- Name: parameters_parameter parameters_parameter_code_5a45e0df_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parameters_parameter
    ADD CONSTRAINT parameters_parameter_code_5a45e0df_uniq UNIQUE (code);


--
-- Name: parameters_parameter parameters_parameter_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parameters_parameter
    ADD CONSTRAINT parameters_parameter_pkey PRIMARY KEY (id);


--
-- Name: parameters_varietalparameter parameters_varietalparameter_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parameters_varietalparameter
    ADD CONSTRAINT parameters_varietalparameter_pkey PRIMARY KEY (id);


--
-- Name: register_plantspecies register_plantspecies_common_name_860bf487_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.register_plantspecies
    ADD CONSTRAINT register_plantspecies_common_name_860bf487_uniq UNIQUE (common_name);


--
-- Name: register_plantspecies register_plantspecies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.register_plantspecies
    ADD CONSTRAINT register_plantspecies_pkey PRIMARY KEY (id);


--
-- Name: register_plantvariety register_plantvariety_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.register_plantvariety
    ADD CONSTRAINT register_plantvariety_pkey PRIMARY KEY (id);


--
-- Name: register_plantvarietyname register_plantvarietyname_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.register_plantvarietyname
    ADD CONSTRAINT register_plantvarietyname_pkey PRIMARY KEY (id);


--
-- Name: spaces_area spaces_area_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.spaces_area
    ADD CONSTRAINT spaces_area_pkey PRIMARY KEY (id);


--
-- Name: spaces_location spaces_location_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.spaces_location
    ADD CONSTRAINT spaces_location_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: calculator_crop_area_id_c992067d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX calculator_crop_area_id_c992067d ON public.calculator_crop USING btree (area_id);


--
-- Name: calculator_crop_content_type_id_ac59b19f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX calculator_crop_content_type_id_ac59b19f ON public.calculator_crop USING btree (content_type_id);


--
-- Name: calculator_cropparameter_crop_id_2e339518; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX calculator_cropparameter_crop_id_2e339518 ON public.calculator_cropparameter USING btree (crop_id);


--
-- Name: calculator_cropparameter_parameter_id_e96c2082; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX calculator_cropparameter_parameter_id_e96c2082 ON public.calculator_cropparameter USING btree (parameter_id);


--
-- Name: calculator_management_crop_id_cf5d6b2e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX calculator_management_crop_id_cf5d6b2e ON public.calculator_management USING btree (crop_id);


--
-- Name: calculator_management_type_id_77dc66ab; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX calculator_management_type_id_77dc66ab ON public.calculator_management USING btree (type_id);


--
-- Name: collect_cart_user_id_2d6e9c32; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX collect_cart_user_id_2d6e9c32 ON public.collect_cart USING btree (user_id);


--
-- Name: collect_cartitem_cart_id_3ab6ca4a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX collect_cartitem_cart_id_3ab6ca4a ON public.collect_cartitem USING btree (cart_id);


--
-- Name: collect_cartitem_sample_id_455cca86; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX collect_cartitem_sample_id_455cca86 ON public.collect_cartitem USING btree (sample_id);


--
-- Name: collect_germinability_seedsample_id_b584cc4a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX collect_germinability_seedsample_id_b584cc4a ON public.collect_germinability USING btree (seedsample_id);


--
-- Name: collect_sampleweight_seedsample_id_24cdd9da; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX collect_sampleweight_seedsample_id_24cdd9da ON public.collect_sampleweight USING btree (seedsample_id);


--
-- Name: collect_seedsample_position_id_5cb5fbf2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX collect_seedsample_position_id_5cb5fbf2 ON public.collect_seedsample USING btree (position_id);


--
-- Name: collect_seedsample_variety_id_5dd155c1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX collect_seedsample_variety_id_5dd155c1 ON public.collect_seedsample USING btree (variety_id);


--
-- Name: collect_storage_name_21377b9a_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX collect_storage_name_21377b9a_like ON public.collect_storage USING btree (name varchar_pattern_ops);


--
-- Name: collect_storageposition_storage_id_8a0d948b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX collect_storageposition_storage_id_8a0d948b ON public.collect_storageposition USING btree (storage_id);


--
-- Name: describe_description_protocol_id_6bc19dad; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX describe_description_protocol_id_6bc19dad ON public.describe_description USING btree (protocol_id);


--
-- Name: describe_description_variety_id_eb7763ad; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX describe_description_variety_id_eb7763ad ON public.describe_description USING btree (variety_id);


--
-- Name: describe_expression_description_id_9b713d79; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX describe_expression_description_id_9b713d79 ON public.describe_expression USING btree (description_id);


--
-- Name: describe_expression_state_of_expression_id_bea5d4c4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX describe_expression_state_of_expression_id_bea5d4c4 ON public.describe_expression USING btree (state_of_expression_id);


--
-- Name: describe_protocol_specie_id_f000bd4f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX describe_protocol_specie_id_f000bd4f ON public.describe_protocol USING btree (specie_id);


--
-- Name: describe_state_trait_id_ce1459a2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX describe_state_trait_id_ce1459a2 ON public.describe_state USING btree (trait_id);


--
-- Name: describe_trait_protocol_id_7369cc28; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX describe_trait_protocol_id_7369cc28 ON public.describe_trait USING btree (protocol_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: parameters_cropparameter_parameter_id_791dcb40; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX parameters_cropparameter_parameter_id_791dcb40 ON public.parameters_speciesparameter USING btree (parameter_id);


--
-- Name: parameters_cropparameter_specie_id_ad34fef1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX parameters_cropparameter_specie_id_ad34fef1 ON public.parameters_speciesparameter USING btree (specie_id);


--
-- Name: parameters_measure_trait_id_c7b7cb90; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX parameters_measure_trait_id_c7b7cb90 ON public.parameters_measure USING btree (trait_id);


--
-- Name: parameters_measure_variety_id_a28bd752; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX parameters_measure_variety_id_a28bd752 ON public.parameters_measure USING btree (variety_id);


--
-- Name: parameters_parameter_code_5a45e0df_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX parameters_parameter_code_5a45e0df_like ON public.parameters_parameter USING btree (code varchar_pattern_ops);


--
-- Name: parameters_varietalparameter_parameter_id_2eb3dfa7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX parameters_varietalparameter_parameter_id_2eb3dfa7 ON public.parameters_varietalparameter USING btree (parameter_id);


--
-- Name: parameters_varietalparameter_variety_id_4b2414c8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX parameters_varietalparameter_variety_id_4b2414c8 ON public.parameters_varietalparameter USING btree (variety_id);


--
-- Name: register_plantspecies_common_name_860bf487_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX register_plantspecies_common_name_860bf487_like ON public.register_plantspecies USING btree (common_name varchar_pattern_ops);


--
-- Name: register_plantvariety_species_id_dab5e5d0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX register_plantvariety_species_id_dab5e5d0 ON public.register_plantvariety USING btree (species_id);


--
-- Name: register_plantvarietyname_variety_id_8e222cd8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX register_plantvarietyname_variety_id_8e222cd8 ON public.register_plantvarietyname USING btree (variety_id);


--
-- Name: spaces_area_location_id_69580507; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX spaces_area_location_id_69580507 ON public.spaces_area USING btree (location_id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calculator_crop calculator_crop_area_id_c992067d_fk_spaces_area_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calculator_crop
    ADD CONSTRAINT calculator_crop_area_id_c992067d_fk_spaces_area_id FOREIGN KEY (area_id) REFERENCES public.spaces_area(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calculator_crop calculator_crop_content_type_id_ac59b19f_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calculator_crop
    ADD CONSTRAINT calculator_crop_content_type_id_ac59b19f_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calculator_cropparameter calculator_cropparam_parameter_id_e96c2082_fk_parameter; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calculator_cropparameter
    ADD CONSTRAINT calculator_cropparam_parameter_id_e96c2082_fk_parameter FOREIGN KEY (parameter_id) REFERENCES public.parameters_parameter(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calculator_cropparameter calculator_cropparameter_crop_id_2e339518_fk_calculator_crop_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calculator_cropparameter
    ADD CONSTRAINT calculator_cropparameter_crop_id_2e339518_fk_calculator_crop_id FOREIGN KEY (crop_id) REFERENCES public.calculator_crop(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calculator_management calculator_managemen_type_id_77dc66ab_fk_calculato; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calculator_management
    ADD CONSTRAINT calculator_managemen_type_id_77dc66ab_fk_calculato FOREIGN KEY (type_id) REFERENCES public.calculator_managementtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calculator_management calculator_management_crop_id_cf5d6b2e_fk_calculator_crop_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calculator_management
    ADD CONSTRAINT calculator_management_crop_id_cf5d6b2e_fk_calculator_crop_id FOREIGN KEY (crop_id) REFERENCES public.calculator_crop(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: collect_cart collect_cart_user_id_2d6e9c32_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_cart
    ADD CONSTRAINT collect_cart_user_id_2d6e9c32_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: collect_cartitem collect_cartitem_cart_id_3ab6ca4a_fk_collect_cart_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_cartitem
    ADD CONSTRAINT collect_cartitem_cart_id_3ab6ca4a_fk_collect_cart_id FOREIGN KEY (cart_id) REFERENCES public.collect_cart(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: collect_cartitem collect_cartitem_sample_id_455cca86_fk_collect_seedsample_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_cartitem
    ADD CONSTRAINT collect_cartitem_sample_id_455cca86_fk_collect_seedsample_id FOREIGN KEY (sample_id) REFERENCES public.collect_seedsample(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: collect_germinability collect_germinabilit_seedsample_id_b584cc4a_fk_collect_s; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_germinability
    ADD CONSTRAINT collect_germinabilit_seedsample_id_b584cc4a_fk_collect_s FOREIGN KEY (seedsample_id) REFERENCES public.collect_seedsample(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: collect_sampleweight collect_sampleweight_seedsample_id_24cdd9da_fk_collect_s; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_sampleweight
    ADD CONSTRAINT collect_sampleweight_seedsample_id_24cdd9da_fk_collect_s FOREIGN KEY (seedsample_id) REFERENCES public.collect_seedsample(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: collect_seedsample collect_seedsample_position_id_5cb5fbf2_fk_collect_s; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_seedsample
    ADD CONSTRAINT collect_seedsample_position_id_5cb5fbf2_fk_collect_s FOREIGN KEY (position_id) REFERENCES public.collect_storageposition(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: collect_seedsample collect_seedsample_variety_id_5dd155c1_fk_register_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_seedsample
    ADD CONSTRAINT collect_seedsample_variety_id_5dd155c1_fk_register_ FOREIGN KEY (variety_id) REFERENCES public.register_plantvariety(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: collect_storageposition collect_storageposit_storage_id_8a0d948b_fk_collect_s; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collect_storageposition
    ADD CONSTRAINT collect_storageposit_storage_id_8a0d948b_fk_collect_s FOREIGN KEY (storage_id) REFERENCES public.collect_storage(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: describe_description describe_description_protocol_id_6bc19dad_fk_describe_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.describe_description
    ADD CONSTRAINT describe_description_protocol_id_6bc19dad_fk_describe_ FOREIGN KEY (protocol_id) REFERENCES public.describe_protocol(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: describe_description describe_description_variety_id_eb7763ad_fk_register_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.describe_description
    ADD CONSTRAINT describe_description_variety_id_eb7763ad_fk_register_ FOREIGN KEY (variety_id) REFERENCES public.register_plantvariety(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: describe_expression describe_expression_description_id_9b713d79_fk_describe_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.describe_expression
    ADD CONSTRAINT describe_expression_description_id_9b713d79_fk_describe_ FOREIGN KEY (description_id) REFERENCES public.describe_description(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: describe_expression describe_expression_state_of_expression__bea5d4c4_fk_describe_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.describe_expression
    ADD CONSTRAINT describe_expression_state_of_expression__bea5d4c4_fk_describe_ FOREIGN KEY (state_of_expression_id) REFERENCES public.describe_state(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: describe_protocol describe_protocol_specie_id_f000bd4f_fk_register_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.describe_protocol
    ADD CONSTRAINT describe_protocol_specie_id_f000bd4f_fk_register_ FOREIGN KEY (specie_id) REFERENCES public.register_plantspecies(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: describe_state describe_state_trait_id_ce1459a2_fk_describe_trait_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.describe_state
    ADD CONSTRAINT describe_state_trait_id_ce1459a2_fk_describe_trait_id FOREIGN KEY (trait_id) REFERENCES public.describe_trait(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: describe_trait describe_trait_protocol_id_7369cc28_fk_describe_protocol_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.describe_trait
    ADD CONSTRAINT describe_trait_protocol_id_7369cc28_fk_describe_protocol_id FOREIGN KEY (protocol_id) REFERENCES public.describe_protocol(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: parameters_speciesparameter parameters_cropparam_parameter_id_791dcb40_fk_parameter; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parameters_speciesparameter
    ADD CONSTRAINT parameters_cropparam_parameter_id_791dcb40_fk_parameter FOREIGN KEY (parameter_id) REFERENCES public.parameters_parameter(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: parameters_speciesparameter parameters_cropparam_specie_id_ad34fef1_fk_register_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parameters_speciesparameter
    ADD CONSTRAINT parameters_cropparam_specie_id_ad34fef1_fk_register_ FOREIGN KEY (specie_id) REFERENCES public.register_plantspecies(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: parameters_measure parameters_measure_trait_id_c7b7cb90_fk_describe_trait_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parameters_measure
    ADD CONSTRAINT parameters_measure_trait_id_c7b7cb90_fk_describe_trait_id FOREIGN KEY (trait_id) REFERENCES public.describe_trait(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: parameters_measure parameters_measure_variety_id_a28bd752_fk_register_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parameters_measure
    ADD CONSTRAINT parameters_measure_variety_id_a28bd752_fk_register_ FOREIGN KEY (variety_id) REFERENCES public.register_plantvariety(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: parameters_varietalparameter parameters_varietalp_parameter_id_2eb3dfa7_fk_parameter; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parameters_varietalparameter
    ADD CONSTRAINT parameters_varietalp_parameter_id_2eb3dfa7_fk_parameter FOREIGN KEY (parameter_id) REFERENCES public.parameters_parameter(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: parameters_varietalparameter parameters_varietalp_variety_id_4b2414c8_fk_register_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parameters_varietalparameter
    ADD CONSTRAINT parameters_varietalp_variety_id_4b2414c8_fk_register_ FOREIGN KEY (variety_id) REFERENCES public.register_plantvariety(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: register_plantvariety register_plantvariet_species_id_dab5e5d0_fk_register_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.register_plantvariety
    ADD CONSTRAINT register_plantvariet_species_id_dab5e5d0_fk_register_ FOREIGN KEY (species_id) REFERENCES public.register_plantspecies(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: register_plantvarietyname register_plantvariet_variety_id_8e222cd8_fk_register_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.register_plantvarietyname
    ADD CONSTRAINT register_plantvariet_variety_id_8e222cd8_fk_register_ FOREIGN KEY (variety_id) REFERENCES public.register_plantvariety(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: spaces_area spaces_area_location_id_69580507_fk_spaces_location_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.spaces_area
    ADD CONSTRAINT spaces_area_location_id_69580507_fk_spaces_location_id FOREIGN KEY (location_id) REFERENCES public.spaces_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

