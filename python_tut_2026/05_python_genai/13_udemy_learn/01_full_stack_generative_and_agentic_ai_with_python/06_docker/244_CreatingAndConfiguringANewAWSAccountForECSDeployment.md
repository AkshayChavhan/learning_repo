# AWS Setup — Account, CLI, and Linking Your Laptop

Before deploying to AWS ECS you need three things: an **AWS account**, the **AWS CLI** on
your laptop, and a **user with access keys** so the CLI can act on your account. This note
is the checklist.

---

## 1. Create the account

- Go to aws.amazon.com and sign up. Free tier.
- Card verification charges about ₹2 (refundable).
- Expected learning cost for this section: under $1, roughly ₹50. Worth it.
- After signing in, pick the **region** closest to you (top-right). Mumbai = `ap-south-1`.

| You are in | Region code |
|---|---|
| India | `ap-south-1` (Mumbai) |
| US East | `us-east-1` |
| Europe | `eu-west-1` (Ireland) |

---

## 2. Install the AWS CLI

Search "AWS CLI install" → official docs → *Install or update the latest version*.

| OS | How |
|---|---|
| macOS | download the `.pkg` and run it, or the `curl` + `sudo installer` commands from the docs |
| Linux | `curl` the zip, unzip, `sudo ./aws/install` |
| Windows | download the `.msi`, run it |

Verify:

```bash
aws --version
```

```text
aws-cli/2.15.x Python/3.11.x Darwin/23.x source/arm64
```

Any version number = installed.

---

## 3. Create a user for the CLI (IAM)

The CLI needs an identity. You make one in **IAM** (Identity and Access Management).

| Step | Where | What to choose |
|---|---|---|
| 1 | AWS console → search **IAM** → Users → **Create user** | name: `piyushk` (anything) |
| 2 | "Provide user access to the Management Console?" | **No**. This user is CLI-only |
| 3 | Permissions → **Attach policies directly** | `AdministratorAccess` (for learning) |
| 4 | Review → **Create user** | |

> In a real job, give only the permissions the user needs (ECS, ECR…). Admin is a shortcut
> for the course.

---

## 4. Create access keys

| Step | Where |
|---|---|
| 1 | IAM → Users → click your user → **Security credentials** tab |
| 2 | scroll to **Access keys** → **Create access key** |
| 3 | use case: **Command Line Interface (CLI)** → tick "I understand" → Next → Create |
| 4 | copy the **Access key ID** and the **Secret access key**. The secret is shown **once** |

Treat the secret like a password. Never commit it, never paste it in a chat.

---

## 5. Link the CLI to the account

```bash
aws configure
```

```text
AWS Access Key ID [None]:     AKIA................
AWS Secret Access Key [None]: ....................................
Default region name [None]:   ap-south-1
Default output format [None]: json
```

| Prompt | What to enter |
|---|---|
| Access Key ID | from step 4 |
| Secret Access Key | from step 4 |
| Default region | your region code, e.g. `ap-south-1` |
| Output format | `json` |

If you get a permission error writing the config, run it with `sudo` or fix ownership of
`~/.aws` (see gotchas).

### What it created

```bash
ls ~/.aws
```

```text
config        ← region + output format
credentials   ← access key + secret
```

```text
# ~/.aws/credentials
[default]
aws_access_key_id = AKIA...
aws_secret_access_key = ...

# ~/.aws/config
[default]
region = ap-south-1
output = json
```

Every `aws` command from now on runs as this user.

---

## 6. Prove it works

```bash
aws iam get-user
```

```json
{
    "User": {
        "UserName": "piyushk",
        "UserId": "AIDA...",
        "Arn": "arn:aws:iam::123456789012:user/piyushk",
        "CreateDate": "2026-10-13T10:00:00+00:00"
    }
}
```

| Field | Meaning |
|---|---|
| `UserName` | the IAM user you created |
| `Arn` | Amazon Resource Name: the unique id of anything in AWS |
| the 12-digit number in the ARN | your **account id** |

Your laptop now talks to your AWS account.

---

## Gotchas

- **`aws configure` needed `sudo`?** That means `~/.aws` is owned by root from an earlier
  install. Fix once: `sudo chown -R $(whoami) ~/.aws`, then rerun without `sudo`.
- **Lost the secret key?** It can't be shown again. Delete that key in IAM and create a new one.
- **Wrong region later?** Edit `~/.aws/config` or rerun `aws configure`.
- **Delete the user when done** with the course. The instructor deletes his after recording.

---

## Remember

| Term | One line |
|---|---|
| **region** | the AWS data centre you use; pick the nearest (`ap-south-1` = Mumbai) |
| **AWS CLI** | the `aws` command; `aws --version` to check |
| **IAM** | where users and permissions live |
| **IAM user** | an identity for the CLI; console access off, admin policy for learning |
| **access key + secret** | the user's credentials; secret shown once |
| **`aws configure`** | stores them in `~/.aws/credentials` and `~/.aws/config` |
| **`aws iam get-user`** | confirms which user the CLI is using |
| **ARN** | unique name of any AWS resource, contains your account id |

**Next:** ECR (where images go) and ECS (where containers run).
