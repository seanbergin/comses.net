# Generated by Django 2.1.2 on 2018-10-25 03:52

import core.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0003_codebaseimage_file_hash"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="codebase",
            options={},
        ),
        migrations.AlterModelOptions(
            name="codebaserelease",
            options={},
        ),
        migrations.AlterModelOptions(
            name="peerreviewinvitation",
            options={},
        ),
        migrations.AddField(
            model_name="peerreviewerfeedback",
            name="last_modified",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="peerreview",
            name="assigned_reviewer_email",
            field=models.EmailField(
                blank=True,
                help_text="Assigned reviewer email used for non-CoMSES members",
                max_length=254,
            ),
        ),
        migrations.AlterField(
            model_name="peerreviewerfeedback",
            name="notes_to_author",
            field=core.fields.MarkdownField(
                blank=True,
                help_text="Editor's notes to be sent to the model author, manually compiled from other reviewer comments.",
                rendered_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="peerreviewerfeedback",
            name="reviewer_submitted",
            field=models.BooleanField(
                default=False,
                help_text="true when reviewer has formally submit feedback, protecting the data from further edits",
            ),
        ),
        migrations.AlterField(
            model_name="peerrevieweventlog",
            name="action",
            field=models.CharField(
                choices=[
                    ("invitation_sent", "Reviewer has been invited"),
                    ("invitation_resent", "Reviewer invitation has been resent"),
                    ("invitation_accepted", "Reviewer has accepted invitation"),
                    ("invitation_declined", "Reviewer has declined invitation"),
                    ("reviewer_feedback_submitted", "Reviewer has given feedback"),
                    ("author_resubmitted", "Author has resubmitted release for review"),
                    ("review_status_updated", "Editor manually changed review status"),
                    (
                        "revisions_requested",
                        "Editor has requested revisions to this release",
                    ),
                    (
                        "release_certified",
                        "Editor has taken reviewer feedback into account and certified this release as peer reviewed",
                    ),
                ],
                help_text="status action requested.",
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name="peerrevieweventlog",
            name="review",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="event_set",
                to="library.PeerReview",
            ),
        ),
        migrations.AlterField(
            model_name="peerreviewinvitation",
            name="accepted",
            field=models.NullBooleanField(
                choices=[
                    (None, "Waiting for response"),
                    (False, "Decline invitation"),
                    (True, "Accept invitation"),
                ],
                help_text="Accept or decline a peer review invitation",
                verbose_name="Status of this invitation",
            ),
        ),
        migrations.AlterField(
            model_name="peerreviewinvitation",
            name="candidate_reviewer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="peer_review_invitation_set",
                to="core.MemberProfile",
            ),
        ),
        migrations.AlterField(
            model_name="peerreviewinvitation",
            name="review",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="invitation_set",
                to="library.PeerReview",
            ),
        ),
    ]
