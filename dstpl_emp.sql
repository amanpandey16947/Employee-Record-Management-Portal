--
-- PostgreSQL database dump
--

\restrict qfV0rmnZUPGkaU7JAcxzwuQe71iipTDDK83qykS1KQakKgvcycg5zj9LbHqOVtl

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

-- Started on 2026-01-09 15:00:08

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5015 (class 1262 OID 24598)
-- Name: DSTPL_emp; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE "DSTPL_emp" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_India.1252';


ALTER DATABASE "DSTPL_emp" OWNER TO postgres;

\unrestrict qfV0rmnZUPGkaU7JAcxzwuQe71iipTDDK83qykS1KQakKgvcycg5zj9LbHqOVtl
\connect "DSTPL_emp"
\restrict qfV0rmnZUPGkaU7JAcxzwuQe71iipTDDK83qykS1KQakKgvcycg5zj9LbHqOVtl

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 220 (class 1259 OID 24600)
-- Name: employee_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employee_info (
    employee_id integer NOT NULL,
    name text NOT NULL,
    email text NOT NULL,
    contact character varying(15),
    bachelors_degree text,
    bachelors_university text,
    masters_degree text,
    masters_university text,
    years_of_experience numeric(3,1),
    linkedin_profile text,
    aadhar_number character varying(12),
    upload_aadhar_card text,
    upload_degree text,
    submitted_at timestamp without time zone DEFAULT now(),
    designation character varying(30),
    gender text,
    pass_word text,
    admin text,
    image text,
    work_status character varying(10) DEFAULT 'active'::character varying NOT NULL,
    joining_date date,
    leaving_date date
);


ALTER TABLE public.employee_info OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 24599)
-- Name: employee_info_employee_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.employee_info_employee_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employee_info_employee_id_seq OWNER TO postgres;

--
-- TOC entry 5016 (class 0 OID 0)
-- Dependencies: 219
-- Name: employee_info_employee_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employee_info_employee_id_seq OWNED BY public.employee_info.employee_id;


--
-- TOC entry 4856 (class 2604 OID 24603)
-- Name: employee_info employee_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee_info ALTER COLUMN employee_id SET DEFAULT nextval('public.employee_info_employee_id_seq'::regclass);


--
-- TOC entry 5009 (class 0 OID 24600)
-- Dependencies: 220
-- Data for Name: employee_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employee_info (employee_id, name, email, contact, bachelors_degree, bachelors_university, masters_degree, masters_university, years_of_experience, linkedin_profile, aadhar_number, upload_aadhar_card, upload_degree, submitted_at, designation, gender, pass_word, admin, image, work_status, joining_date, leaving_date) FROM stdin;
105	Arjun Mehta	arjun.mehta@example.com	+919945612345	B.Tech (IT)	VIT Vellore	M.Tech (CSE)	BITS Pilani	6.5	https://linkedin.com/in/arjunmehta	567856785678	https://drive.google.com/file/d/aadhar_arjun/view	https://drive.google.com/file/d/degree_arjun/view	2025-11-03 12:46:34.848721	Senior Software Engineer	Male	arjun	0	hZPuJ.png	active	2024-12-01	\N
103	Vikram Singh	vikram.singh@example.com	+919876543211	BSc Computer Science	DU	MSc Computer Science	JNU	3.5	https://linkedin.com/in/vikramsingh	345634563456	https://drive.google.com/file/d/aadhar_vikram/view	https://drive.google.com/file/d/degree_vikram/view	2025-11-03 12:46:34.848721	Data Analyst	Male	\N	0	\N	active	2024-12-01	\N
102	Riya Sharma	riya.sharma@example.com	+919812345678	B.Tech (CSE)	IIT Delhi	M.Tech (AI)	IIT Bombay	4.0	https://linkedin.com/in/riyasharma	234523452345	https://drive.google.com/file/d/aadhar_riya/view	https://drive.google.com/file/d/degree_riya/view	2025-11-03 12:46:34.848721	AI Research Engineer	female	\N	0	\N	active	2024-12-01	\N
111	Sahil Khan	sahil.khan@example.com	+919955512233	B.Tech (IT)	Jamia Millia Islamia	M.Tech (Data Science)	IIT Kanpur	5.7	https://linkedin.com/in/sahilkhan	223322332233	https://drive.google.com/file/d/aadhar_sahil/view	https://drive.google.com/file/d/degree_sahil/view	2025-11-03 12:46:34.848721	DevOps Engineer	Male	\N	0	\N	active	2024-12-01	\N
104	Sneha Verma	sneha.verma@example.com	+919934567890	B.Com	Lucknow University	MBA	IIM Bangalore	5.2	https://linkedin.com/in/snehaverma	456745674567	https://drive.google.com/file/d/aadhar_sneha/view	https://drive.google.com/file/d/degree_sneha/view	2025-11-03 12:46:34.848721	Business Analyst	female	\N	0	\N	active	2024-12-01	\N
106	Priya Nair	priya.nair@example.com	+919876512340	B.Sc Electronics	Kerala University	MCA	NIT Calicut	3.0	https://linkedin.com/in/priyanair	678967896789	https://drive.google.com/file/d/aadhar_priya/view	https://drive.google.com/file/d/degree_priya/view	2025-11-03 12:46:34.848721	Web Developer	female	\N	0	\N	active	2024-12-01	\N
110	Neha Yadav	neha.yadav@example.com	+919943210987	BCA	IGNOU	MCA	IGNOU	1.5	https://linkedin.com/in/nehayadav	112211221122	https://drive.google.com/file/d/aadhar_neha/view	https://drive.google.com/file/d/degree_neha/view	2025-11-03 12:46:34.848721	Cloud Architect	female	\N	0	\N	active	2024-12-01	\N
113	Deepak Kumar	deepak.kumar@example.com	+919876987654	B.Tech (CSE)	NIT Warangal	M.Tech (AI)	IIT Madras	7.0	https://linkedin.com/in/deepakkumar	445544554455	https://drive.google.com/file/d/aadhar_deepak/view	https://drive.google.com/file/d/degree_deepak/view	2025-11-03 12:46:34.848721	UI/UX Designer	Male	\N	0	\N	inactive	2024-12-01	2024-12-19
107	Rahul Das	rahul.das@example.com	+919912345600	BCA	NIT Durgapur	MCA	NIT Trichy	2.8	https://linkedin.com/in/rahuldas	789078907890	https://drive.google.com/file/d/aadhar_rahul/view	https://drive.google.com/file/d/degree_rahul/view	2025-11-03 12:46:34.848721	Project Manager	Male	\N	0	\N	inactive	2024-12-01	2024-12-19
109	Manish Patel	manish.patel@example.com	+919976543219	B.E Mechanical	Gujarat Technological University	MBA	Symbiosis Pune	8.0	https://linkedin.com/in/manishpatel	901290129012	https://drive.google.com/file/d/aadhar_manish/view	https://drive.google.com/file/d/degree_manish/view	2025-11-03 12:46:34.848721	System Analyst	Male	\N	0	\N	inactive	2024-12-01	2024-12-19
115	Rohit Sen	rohit.sen@example.com	+919933445566	B.Tech (ECE)	NIT Silchar	M.Tech (Embedded Systems)	IIT Kharagpur	9.1	https://linkedin.com/in/rohitsen	667766776677	https://drive.google.com/file/d/aadhar_rohit/view	https://drive.google.com/file/d/degree_rohit/view	2025-11-03 12:46:34.848721	Technical Support Engineer	Male	\N	0	\N	active	2024-12-01	\N
112	Kavita Joshi	kavita.joshi@example.com	+919876000111	B.Sc (Maths)	Mumbai University	MCA	Pune University	3.2	https://linkedin.com/in/kavitajoshi	334433443344	https://drive.google.com/file/d/aadhar_kavita/view	https://drive.google.com/file/d/degree_kavita/view	2025-11-03 12:46:34.848721	Cybersecurity Specialist	female	\N	0	\N	active	2024-12-01	\N
114	Simran Kaur	simran.kaur@example.com	+919911223344	BCA	Guru Nanak Dev University	MCA	Punjab University	2.0	https://linkedin.com/in/simrankaur	556655665566	https://drive.google.com/file/d/aadhar_simran/view	https://drive.google.com/file/d/degree_simran/view	2025-11-03 12:46:34.848721	Machine Learning Engineer	female	\N	0	\N	active	2024-12-01	\N
101	Aman Pandey	aman@example.com	+919876543210	BCA	Parul University			0.0	https://linkedin.com/in/amanpandey	123412341234	https://drive.google.com/file/d/aadhar_link/view	https://drive.google.com/file/d/degree_link/view	2025-11-03 12:46:34.848721	Junior Software Engineer	Male	aman	1	BCXuL.png	active	2024-12-01	\N
108	Isha Gupta	isha.gupta@example.com	+919832145678	B.Tech (CSE)	SRM University	M.Tech (AI)	Amity University	4.3	https://linkedin.com/in/ishagupta	890189018901	https://drive.google.com/file/d/aadhar_isha/view	https://drive.google.com/file/d/degree_isha/view	2025-11-03 12:46:34.848721	Database Administrator	female	isha	0	39MCt.png	active	2024-12-01	\N
\.


--
-- TOC entry 5017 (class 0 OID 0)
-- Dependencies: 219
-- Name: employee_info_employee_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employee_info_employee_id_seq', 2, true);


--
-- TOC entry 4860 (class 2606 OID 24611)
-- Name: employee_info employee_info_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee_info
    ADD CONSTRAINT employee_info_pkey PRIMARY KEY (employee_id);


-- Completed on 2026-01-09 15:00:08

--
-- PostgreSQL database dump complete
--

\unrestrict qfV0rmnZUPGkaU7JAcxzwuQe71iipTDDK83qykS1KQakKgvcycg5zj9LbHqOVtl

