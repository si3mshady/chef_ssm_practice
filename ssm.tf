resource "aws_ssm_document" "install-chef-workstation" {
  name          = "updateAndInstallChefWs"
  document_type = "Command"
  document_format = "YAML"
  content = file("ssm_cmds.yml") 
}

output "ssm-metadata" {
  value = aws_ssm_document.install-chef-workstation

}