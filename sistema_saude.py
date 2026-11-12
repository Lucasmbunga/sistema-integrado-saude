import json
import os


class UnidadeSaude:
    def __init__(self, id_unidade, nome, municipio, tipo):
        self.id_unidade = id_unidade
        self.nome = nome
        self.municipio = municipio
        self.tipo = tipo

    def to_dict(self):
        return {
            "id_unidade": self.id_unidade,
            "nome": self.nome,
            "municipio": self.municipio,
            "tipo": self.tipo,
        }

    @classmethod
    def from_dict(cls, dados):
        return cls(
            dados["id_unidade"],
            dados["nome"],
            dados["municipio"],
            dados["tipo"],
        )

    def __str__(self):
        return f"[{self.id_unidade}] {self.nome} ({self.tipo}) - Município: {self.municipio}"


class Paciente:
    def __init__(self, id_paciente, nome, data_nascimento, genero, nif="N/A"):
        self.id_paciente = id_paciente
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.genero = genero
        self.nif = nif

    def to_dict(self):
        return {
            "id_paciente": self.id_paciente,
            "nome": self.nome,
            "data_nascimento": self.data_nascimento,
            "genero": self.genero,
            "nif": self.nif,
        }

    @classmethod
    def from_dict(cls, dados):
        return cls(
            dados["id_paciente"],
            dados["nome"],
            dados["data_nascimento"],
            dados["genero"],
            dados.get("nif", "N/A"),
        )

    def __str__(self):
        return f"ID: {self.id_paciente} | Nome: {self.nome} | Nasc.: {self.data_nascimento} | Género: {self.genero} | NIF: {self.nif}"


class RegistoClinico:
    def __init__(self, id_registo, id_paciente, id_unidade, medico, data, diagnostico, tratamento):
        self.id_registo = id_registo
        self.id_paciente = id_paciente
        self.id_unidade = id_unidade
        self.medico = medico
        self.data = data
        self.diagnostico = diagnostico
        self.tratamento = tratamento

    def to_dict(self):
        return {
            "id_registo": self.id_registo,
            "id_paciente": self.id_paciente,
            "id_unidade": self.id_unidade,
            "medico": self.medico,
            "data": self.data,
            "diagnostico": self.diagnostico,
            "tratamento": self.tratamento,
        }

    @classmethod
    def from_dict(cls, dados):
        return cls(
            dados["id_registo"],
            dados["id_paciente"],
            dados["id_unidade"],
            dados["medico"],
            dados["data"],
            dados["diagnostico"],
            dados["tratamento"],
        )

    def __str__(self):
        return (
            f"  - Registo [{self.id_registo}] | Data: {self.data} | Médico: {self.medico}\n"
            f"    Diagnóstico: {self.diagnostico}\n"
            f"    Tratamento: {self.tratamento}"
        )


class SistemaIntegradoSaude:
    def __init__(self, ficheiro_dados="dados_saude_uige.json"):
        self.ficheiro_dados = ficheiro_dados
        self.unidades = {}
        self.pacientes = {}
        self.registos = []
        self._carregar_dados()

    # --- Persistência de Dados (JSON) ---
    def _guardar_dados(self):
        dados = {
            "unidades": {k: v.to_dict() for k, v in self.unidades.items()},
            "pacientes": {k: v.to_dict() for k, v in self.pacientes.items()},
            "registos": [r.to_dict() for r in self.registos],
        }
        try:
            with open(self.ficheiro_dados, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"[Erro de Sistema] Não foi possível guardar os dados no disco: {e}")

    def _carregar_dados(self):
        if not os.path.exists(self.ficheiro_dados):
            self._inicializar_dados_base()
            self._guardar_dados()
            return

        try:
            with open(self.ficheiro_dados, "r", encoding="utf-8") as f:
                dados = json.load(f)
                self.unidades = {
                    k: UnidadeSaude.from_dict(v) for k, v in dados.get("unidades", {}).items()
                }
                self.pacientes = {
                    k: Paciente.from_dict(v) for k, v in dados.get("pacientes", {}).items()
                }
                self.registos = [
                    RegistoClinico.from_dict(r) for r in dados.get("registos", [])
                ]
        except (json.JSONDecodeError, KeyError, IOError) as e:
            print(f"[Aviso] Ficheiro de dados corrompido ({e}). A restaurar dados base...")
            self._inicializar_dados_base()
            self._guardar_dados()

    def _inicializar_dados_base(self):
        self.unidades["HGU01"] = UnidadeSaude("HGU01", "Hospital Geral do Uíge", "Uíge", "Hospital")
        self.unidades["CS02"] = UnidadeSaude("CS02", "Centro de Saúde do Mangue", "Uíge", "Centro de Saúde")
        self.pacientes["P001"] = Paciente("P001", "Mário Kanjila", "12/05/1998", "Masculino", "004589231LA042")
        self.registos.append(
            RegistoClinico("R001", "P001", "HGU01", "Dr. Nsaku", "10/11/2026", "Malária Simples", "Artemether/Lumefantrine")
        )

    # --- Validação de Entradas ---
    @staticmethod
    def _ler_texto_obrigatorio(mensagem):
        while True:
            valor = input(mensagem).strip()
            if valor:
                return valor
            print("  [Aviso] Este campo é obrigatório.")

    @staticmethod
    def _ler_data_valida(mensagem, permitir_vazio=False):
        while True:
            data = input(mensagem).strip()
            if permitir_vazio and not data:
                return None
            partes = data.split("/")
            if len(partes) == 3 and all(p.isdigit() for p in partes):
                dia, mes, ano = int(partes[0]), int(partes[1]), int(partes[2])
                if 1 <= dia <= 31 and 1 <= mes <= 12 and 1900 <= ano <= 2100:
                    return f"{dia:02d}/{mes:02d}/{ano}"
            print("  [Aviso] Data inválida. Utilize o padrão DD/MM/AAAA (ex: 12/11/2026).")

    @staticmethod
    def _confirmar_acao(mensagem):
        resp = input(f"{mensagem} (S/N): ").strip().upper()
        return resp == "S"

    # =========================================================================
    # CRUD 1: UNIDADES DE SAÚDE
    # =========================================================================
    def menu_unidades(self):
        while True:
            print("\n--- GESTÃO DE UNIDADES DE SAÚDE ---")
            print("1. Registar Nova Unidade (Create)")
            print("2. Listar Todas as Unidades (Read)")
            print("3. Atualizar Dados da Unidade (Update)")
            print("4. Eliminar Unidade (Delete)")
            print("0. Voltar ao Menu Principal")
            op = input("Opção: ").strip()

            if op == "1":
                self._criar_unidade()
            elif op == "2":
                self._listar_unidades()
            elif op == "3":
                self._atualizar_unidade()
            elif op == "4":
                self._eliminar_unidade()
            elif op == "0":
                break
            else:
                print("[Aviso] Opção inválida.")

    def _criar_unidade(self):
        id_unidade = self._ler_texto_obrigatorio("ID da Unidade (ex: HGU02): ").upper()
        if id_unidade in self.unidades:
            print(f"[Erro] Já existe uma unidade com o ID '{id_unidade}'.")
            return
        nome = self._ler_texto_obrigatorio("Nome da Unidade: ")
        municipio = self._ler_texto_obrigatorio("Município: ")
        tipo = self._ler_texto_obrigatorio("Tipo (Hospital / Centro de Saúde / Posto Médico): ")

        self.unidades[id_unidade] = UnidadeSaude(id_unidade, nome, municipio, tipo)
        self._guardar_dados()
        print("Unidade registada com sucesso!")

    def _listar_unidades(self):
        print("\nUnidades de Saúde Registadas:")
        if not self.unidades:
            print("  Nenhuma unidade registada.")
        else:
            for u in self.unidades.values():
                print(f"  {u}")

    def _atualizar_unidade(self):
        id_unidade = self._ler_texto_obrigatorio("ID da Unidade a atualizar: ").upper()
        unidade = self.unidades.get(id_unidade)
        if not unidade:
            print("[Erro] Unidade não encontrada.")
            return

        print(f"A editar: {unidade} (Prima Enter para manter o valor atual)")
        novo_nome = input(f"Novo Nome [{unidade.nome}]: ").strip()
        novo_municipio = input(f"Novo Município [{unidade.municipio}]: ").strip()
        novo_tipo = input(f"Novo Tipo [{unidade.tipo}]: ").strip()

        if novo_nome:
            unidade.nome = novo_nome
        if novo_municipio:
            unidade.municipio = novo_municipio
        if novo_tipo:
            unidade.tipo = novo_tipo

        self._guardar_dados()
        print("Dados da unidade atualizados com sucesso!")

    def _eliminar_unidade(self):
        id_unidade = self._ler_texto_obrigatorio("ID da Unidade a eliminar: ").upper()
        if id_unidade not in self.unidades:
            print("[Erro] Unidade não encontrada.")
            return

        # Integridade referencial: verifica se existem consultas ligadas à unidade
        associados = [r for r in self.registos if r.id_unidade == id_unidade]
        if associados:
            print(f"[Bloqueio] Não é possível eliminar: existem {len(associados)} registo(s) clínico(s) associados a esta unidade.")
            return

        if self._confirmar_acao(f"Tem a certeza que deseja eliminar '{self.unidades[id_unidade].nome}'?"):
            del self.unidades[id_unidade]
            self._guardar_dados()
            print("Unidade eliminada com sucesso.")

    # =========================================================================
    # CRUD 2: UTENTES / PACIENTES
    # =========================================================================
    def menu_pacientes(self):
        while True:
            print("\n--- GESTÃO DE UTENTES / PACIENTES ---")
            print("1. Registar Novo Utente (Create)")
            print("2. Listar Todos os Utentes (Read)")
            print("3. Pesquisar Utente por ID ou Nome (Read)")
            print("4. Atualizar Dados do Utente (Update)")
            print("5. Eliminar Utente (Delete)")
            print("0. Voltar ao Menu Principal")
            op = input("Opção: ").strip()

            if op == "1":
                self._criar_paciente()
            elif op == "2":
                self._listar_pacientes()
            elif op == "3":
                self._pesquisar_paciente()
            elif op == "4":
                self._atualizar_paciente()
            elif op == "5":
                self._eliminar_paciente()
            elif op == "0":
                break
            else:
                print("[Aviso] Opção inválida.")

    def _criar_paciente(self):
        id_paciente = self._ler_texto_obrigatorio("ID/Número de Registo do Utente (ex: P002): ").upper()
        if id_paciente in self.pacientes:
            print(f"[Erro] O utente '{id_paciente}' já está registado.")
            return
        nome = self._ler_texto_obrigatorio("Nome Completo: ")
        data_nascimento = self._ler_data_valida("Data de Nascimento (DD/MM/AAAA): ")
        genero = self._ler_texto_obrigatorio("Género (Masculino/Feminino): ")
        nif = input("NIF (opcional): ").strip() or "N/A"

        self.pacientes[id_paciente] = Paciente(id_paciente, nome, data_nascimento, genero, nif)
        self._guardar_dados()
        print("Utente registado com sucesso!")

    def _listar_pacientes(self):
        print("\nUtentes Registados:")
        if not self.pacientes:
            print("  Nenhum utente registado.")
        else:
            for p in self.pacientes.values():
                print(f"  {p}")

    def _pesquisar_paciente(self):
        termo = self._ler_texto_obrigatorio("Introduza o ID ou parte do Nome do utente: ").lower()
        encontrados = [
            p for p in self.pacientes.values()
            if termo in p.id_paciente.lower() or termo in p.nome.lower()
        ]
        if not encontrados:
            print("Nenhum utente encontrado com esse critério.")
        else:
            for p in encontrados:
                print(f"  {p}")

    def _atualizar_paciente(self):
        id_paciente = self._ler_texto_obrigatorio("ID do Utente a atualizar: ").upper()
        paciente = self.pacientes.get(id_paciente)
        if not paciente:
            print("[Erro] Utente não encontrado.")
            return

        print(f"A editar: {paciente} (Prima Enter para manter o valor atual)")
        novo_nome = input(f"Novo Nome [{paciente.nome}]: ").strip()
        nova_data = self._ler_data_valida(f"Nova Data Nascimento [{paciente.data_nascimento}]: ", permitir_vazio=True)
        novo_genero = input(f"Novo Género [{paciente.genero}]: ").strip()
        novo_nif = input(f"Novo NIF [{paciente.nif}]: ").strip()

        if novo_nome:
            paciente.nome = novo_nome
        if nova_data:
            paciente.data_nascimento = nova_data
        if novo_genero:
            paciente.genero = novo_genero
        if novo_nif:
            paciente.nif = novo_nif

        self._guardar_dados()
        print("Dados do utente atualizados com sucesso!")

    def _eliminar_paciente(self):
        id_paciente = self._ler_texto_obrigatorio("ID do Utente a eliminar: ").upper()
        if id_paciente not in self.pacientes:
            print("[Erro] Utente não encontrado.")
            return

        historico = [r for r in self.registos if r.id_paciente == id_paciente]
        if historico:
            print(f"[Aviso] Este utente possui {len(historico)} registo(s) no histórico clínico.")
            if not self._confirmar_acao("Deseja eliminar o utente E todo o seu histórico clínico?"):
                print("Operação cancelada.")
                return
            self.registos = [r for r in self.registos if r.id_paciente != id_paciente]
        else:
            if not self._confirmar_acao(f"Tem a certeza que deseja eliminar '{self.pacientes[id_paciente].nome}'?"):
                return

        del self.pacientes[id_paciente]
        self._guardar_dados()
        print("Utente eliminado com sucesso.")

    # =========================================================================
    # CRUD 3: HISTÓRICO CLÍNICO / ATENDIMENTOS (INTEROPERABILIDADE)
    # =========================================================================
    def menu_registos(self):
        while True:
            print("\n--- GESTÃO DE HISTÓRICO CLÍNICO (INTEROPERABILIDADE) ---")
            print("1. Registar Novo Atendimento / Consulta (Create)")
            print("2. Consultar Histórico Clínico de um Utente (Read)")
            print("3. Atualizar Diagnóstico / Tratamento (Update)")
            print("4. Eliminar Registo Clínico (Delete)")
            print("0. Voltar ao Menu Principal")
            op = input("Opção: ").strip()

            if op == "1":
                self._criar_consulta()
            elif op == "2":
                self._consultar_historico()
            elif op == "3":
                self._atualizar_consulta()
            elif op == "4":
                self._eliminar_consulta()
            elif op == "0":
                break
            else:
                print("[Aviso] Opção inválida.")

    def _gerar_proximo_id_registo(self):
        if not self.registos:
            return "R001"
        numeros = [int(r.id_registo[1:]) for r in self.registos if r.id_registo.startswith("R") and r.id_registo[1:].isdigit()]
        proximo = max(numeros) + 1 if numeros else len(self.registos) + 1
        return f"R{proximo:03d}"

    def _criar_consulta(self):
        if not self.pacientes or not self.unidades:
            print("[Erro] É necessário ter pelo menos um utente e uma unidade registados.")
            return

        id_paciente = self._ler_texto_obrigatorio("ID do Utente: ").upper()
        if id_paciente not in self.pacientes:
            print(f"[Erro] Utente '{id_paciente}' não encontrado.")
            return

        id_unidade = self._ler_texto_obrigatorio("ID da Unidade de Saúde: ").upper()
        if id_unidade not in self.unidades:
            print(f"[Erro] Unidade '{id_unidade}' não encontrada.")
            return

        id_registo = self._gerar_proximo_id_registo()
        medico = self._ler_texto_obrigatorio("Médico Responsável: ")
        data = self._ler_data_valida("Data do Atendimento (DD/MM/AAAA): ")
        diagnostico = self._ler_texto_obrigatorio("Diagnóstico Clínico: ")
        tratamento = self._ler_texto_obrigatorio("Tratamento / Prescrição: ")

        self.registos.append(
            RegistoClinico(id_registo, id_paciente, id_unidade, medico, data, diagnostico, tratamento)
        )
        self._guardar_dados()
        print(f"Atendimento registado e partilhado na rede provincial! (ID: {id_registo})")

    def _consultar_historico(self):
        id_paciente = self._ler_texto_obrigatorio("Introduza o ID do Utente: ").upper()
        paciente = self.pacientes.get(id_paciente)
        if not paciente:
            print(f"[Erro] Utente '{id_paciente}' não encontrado.")
            return

        print(f"\nDados do Utente: {paciente}")
        print("-" * 60)
        encontrados = [r for r in self.registos if r.id_paciente == id_paciente]
        if not encontrados:
            print("  Nenhum registo clínico encontrado para este utente.")
        else:
            for reg in encontrados:
                unidade_nome = self.unidades[reg.id_unidade].nome if reg.id_unidade in self.unidades else reg.id_unidade
                print(f"• Unidade: {unidade_nome} ({reg.id_unidade})")
                print(reg)
                print("-" * 50)

    def _atualizar_consulta(self):
        id_registo = self._ler_texto_obrigatorio("Introduza o ID do Registo Clínico (ex: R001): ").upper()
        registo = next((r for r in self.registos if r.id_registo == id_registo), None)
        if not registo:
            print("[Erro] Registo clínico não encontrado.")
            return

        print(f"A editar registo de {registo.data} (Prima Enter para manter o valor atual)")
        novo_medico = input(f"Médico [{registo.medico}]: ").strip()
        novo_diag = input(f"Diagnóstico [{registo.diagnostico}]: ").strip()
        novo_trat = input(f"Tratamento [{registo.tratamento}]: ").strip()

        if novo_medico:
            registo.medico = novo_medico
        if novo_diag:
            registo.diagnostico = novo_diag
        if novo_trat:
            registo.tratamento = novo_trat

        self._guardar_dados()
        print("Registo clínico atualizado com sucesso!")

    def _eliminar_consulta(self):
        id_registo = self._ler_texto_obrigatorio("Introduza o ID do Registo Clínico a eliminar: ").upper()
        registo = next((r for r in self.registos if r.id_registo == id_registo), None)
        if not registo:
            print("[Erro] Registo clínico não encontrado.")
            return

        if self._confirmar_acao(f"Confirma a eliminação definitiva do registo '{id_registo}'?"):
            self.registos.remove(registo)
            self._guardar_dados()
            print("Registo clínico eliminado com sucesso.")

    # =========================================================================
    # MENU PRINCIPAL
    # =========================================================================
    def executar(self):
        while True:
            try:
                print("\n========================================================")
                print(" SISTEMA INTEGRADO DE INFORMAÇÃO - DIREÇÃO SAÚDE UÍGE")
                print("========================================================")
                print("1. Gestão de Unidades de Saúde (CRUD)")
                print("2. Gestão de Utentes / Pacientes (CRUD)")
                print("3. Gestão de Histórico Clínico / Consultas (CRUD)")
                print("0. Sair")

                opcao = input("Escolha uma opção: ").strip()

                if opcao == "1":
                    self.menu_unidades()
                elif opcao == "2":
                    self.menu_pacientes()
                elif opcao == "3":
                    self.menu_registos()
                elif opcao == "0":
                    print("Dados sincronizados. A encerrar o sistema...")
                    break
                else:
                    print("[Aviso] Opção inválida! Escolha entre 0 e 3.")
            except KeyboardInterrupt:
                print("\n[Sistema] Interrupção detetada. Dados guardados. A sair...")
                break
            except Exception as e:
                print(f"[Erro Inesperado] Ocorreu uma falha: {e}")


if __name__ == "__main__":
    sistema = SistemaIntegradoSaude()
    sistema.executar()
    sistema = SistemaIntegradoSaude()
